from collections import ChainMap

from django.utils.translation import gettext as _
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.reverse import reverse

from . import models as m


class SurveyQuestionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = m.SurveyQuestion
        fields = "__all__"


class SurveyAnswerListSerializer(serializers.ListSerializer):
    def create(self, validated_data):
        answers = []
        answers = self.make_all(validated_data)
        return answers

    def update(self, instance, validated_data):
        answer_mapping = {answer.pk: answer for answer in instance}
        data_mapping = {item["pk"]: item for item in validated_data}

        ret = []
        errors = []

        # Updates all answers that are correct
        # and raises an error for each answer that is incorrect
        # we are OK with this approach.
        for answer_pk, data in data_mapping.items():
            data.pop("pk", None)
            answer = answer_mapping.get(answer_pk, None)

            # answer is None if new answer is sent in (without pk or url)
            if answer is None:
                continue  # we don't want to create during update

            try:
                ret.append(self.child.update(answer, data))
            except ValidationError as error:
                errors.append(error)

        if errors:
            raise ValidationError(dict(ChainMap(*[e.detail for e in errors])))

        return ret

    def make_all(self, validated_data):
        answers = []
        errors = []
        for item in validated_data:
            try:
                answers.append(self.child.create(item))
            except ValidationError as error:
                errors.append(error)

        if errors:
            raise ValidationError(dict(ChainMap(*[e.detail for e in errors])))

        return answers


class SurveyAnswerSerializer(serializers.HyperlinkedModelSerializer):
    pk = serializers.UUIDField(required=False)

    class Meta:
        model = m.SurveyAnswer
        fields = "__all__"
        list_serializer_class = SurveyAnswerListSerializer

    def create(self, validated_data):
        self.validate_required_question_in_creation(validated_data)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        self.validate_required_question_in_update(instance, validated_data)
        return super().update(instance, validated_data)

    def validate_seat(self, seat):
        if seat.appointment != self.context["request"].auth:
            raise ValidationError(_("Invalid seat"))
        return seat

    def validate_required_question_in_creation(self, validated_data):
        question = validated_data["question"]
        answer = validated_data["answer"]

        if question.is_required and answer in ["", None]:
            raise ValidationError(
                {
                    reverse("surveyquestion-detail", request=self.context["request"], kwargs={"pk": question.pk}): _(
                        "This field is required."
                    )
                }
            )

    def validate_required_question_in_update(self, instance, validated_data):
        question = instance.question
        if question.is_required and validated_data.get("answer") in ["", None]:
            raise ValidationError(
                {
                    reverse("surveyanswer-detail", request=self.context["request"], kwargs={"pk": instance.pk}): _(
                        "This field is required."
                    )
                }
            )
