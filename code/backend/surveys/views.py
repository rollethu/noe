from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response

from . import models as m
from . import serializers as s


class SurveyQuestionViewSet(viewsets.ModelViewSet):
    queryset = m.SurveyQuestion.objects.filter(is_active=True)
    serializer_class = s.SurveyQuestionSerializer


class SurveyAnswerViewSet(viewsets.ModelViewSet):
    queryset = m.SurveyAnswer.objects.all()
    serializer_class = s.SurveyAnswerSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
