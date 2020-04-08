from rest_framework import serializers

from . import models as m


class SurveyQuestionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = m.SurveyQuestion
        fields = "__all__"


class SurveyAnswerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = m.SurveyAnswer
        fields = "__all__"
