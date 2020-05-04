from urllib.parse import urlparse

from django.urls import resolve
from rest_framework import status
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.response import Response

from project_noe.views import NoReadModelViewSet
from appointments import auth
from appointments import permissions
from . import models as m
from . import serializers as s


class SurveyQuestionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = m.SurveyQuestion.objects.filter(is_active=True)
    serializer_class = s.SurveyQuestionSerializer


class SurveyAnswerViewSet(mixins.CreateModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):
    queryset = m.SurveyAnswer.objects.all()
    serializer_class = s.SurveyAnswerSerializer
    authentication_classes = [auth.AppointmentAuthentication]
    permission_classes = [permissions.AppointmentPermission]

    def check_same_appointment(self, request, view, obj):
        return request.auth == obj.seat.appointment

    def get_one_object_of_many(self, url):
        uuid = resolve(urlparse(url).path).kwargs["pk"]
        try:
            return m.SurveyAnswer.objects.get(uuid=uuid)
        except m.SurveyAnswer.DoesNotExist():
            return None

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def put(self, request, *args, **kwargs):
        answers = []
        for data in request.data:
            answer = self.get_one_object_of_many(data["url"])
            data["pk"] = answer.pk
            answers.append(answer)

        answers = [a for a in answers if a is not None]
        serializer = self.get_serializer(answers, data=request.data, partial=False, many=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
