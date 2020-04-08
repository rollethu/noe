from rest_framework import serializers

from . import models as m


class SurveyQuestionSerializer(serializers.HyperlinkedModelSerializer):
  class Meta:
    model = m.SurveyQuestion
    fields = "__all__"