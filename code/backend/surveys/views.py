from rest_framework import viewsets

from . import models as m
from . import serializer as s


class SurveyQuestionViewSet(viewsets.ModelViewSet):
  queryset = m.SurveyQuestion.objects.all()
  serializer_class = s.SurveyQuestionSerializer


class SurveyAnswerViewSet(viewsets.ModelViewSet):
  queryset = m.SurveyAnswer.objects.all()
  serializer_class = s.SurveyAnswerSerializer