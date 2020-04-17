from rest_framework import viewsets

from . import models as m
from . import serializers as s


class SurveyQuestionViewSet(viewsets.ModelViewSet):
    queryset = m.SurveyQuestion.objects.filter(is_active=True)
    serializer_class = s.SurveyQuestionSerializer


class SurveyAnswerViewSet(viewsets.ModelViewSet):
    queryset = m.SurveyAnswer.objects.all()
    serializer_class = s.SurveyAnswerSerializer
