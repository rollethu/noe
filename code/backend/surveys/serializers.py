from collections import ChainMap

from django.utils.translation import gettext as _
from rest_framework.exceptions import ValidationError
from rest_framework import serializers

from . import models as m


class SurveyQuestionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = m.SurveyQuestion
        fields = "__all__"


class SurveyAnswerListSerializer(serializers.ListSerializer):
    def create(self, validated_data):
        answers = make_all(validated_data)
        return m.SurveyAnswer.objects.bulk_create(answers)

    def make_all(self, validated_data):
        answers = []
        errors = []
        for i, item in enumerate(validated_data):
            try:
                answers.append(self.make_one(i, item))
            except ValidationError as error:
                errors.append(error)

        if errors:
            raise ValidationError(dict(ChainMap(*[e.detail for e in errors])))

        return answers

    def make_one(self, i, validated_data):
        self.validate_required_question(i, validated_data)
        return m.SurveyAnswer(**validated_data)

    def update(self, instance, validated_data):
        self.validate_required_question(validated_data)
        return super().update(instance, validated_data)

    def validate_required_question(self, i, validated_data):
        question = validated_data["question"]
        answer = validated_data["answer"]

        if question.is_required and answer in ["", None]:
            raise ValidationError({self.initial_data[i]["question"]: _("This field is required.")})


class SurveyAnswerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = m.SurveyAnswer
        fields = "__all__"
        list_serializer_class = SurveyAnswerListSerializer
