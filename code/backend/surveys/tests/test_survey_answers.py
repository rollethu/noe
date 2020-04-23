import pytest
from rest_framework import status
from rest_framework.reverse import reverse

from surveys import models as m


@pytest.fixture
def survey_question():
    return m.SurveyQuestion.objects.create(
        question="First question", is_active=True, is_required=True, answer_datatype="string"
    )


@pytest.fixture
def survey_question2():
    return m.SurveyQuestion.objects.create(
        question="Second question", is_active=True, is_required=True, answer_datatype="string"
    )


@pytest.mark.django_db
def test_create_multiple_answers(api_client, survey_question, survey_question2, seat):
    question1_url = reverse("surveyquestion-detail", kwargs={"pk": survey_question.pk})
    question2_url = reverse("surveyquestion-detail", kwargs={"pk": survey_question2.pk})
    seat_url = reverse("seat-detail", kwargs={"pk": seat.pk})

    rv = api_client.post(
        reverse("surveyanswer-list"),
        [
            {"question": question1_url, "seat": seat_url, "answer": "Test answer 1"},
            {"question": question2_url, "seat": seat_url, "answer": "Test answer 2"},
        ],
        format="json",
    )
    assert rv.status_code == status.HTTP_201_CREATED, rv.data
    assert m.SurveyAnswer.objects.count() == 2

    first_answer = m.SurveyAnswer.objects.first()
    second_answer = m.SurveyAnswer.objects.last()

    assert first_answer.question == survey_question
    assert first_answer.seat == seat
    assert first_answer.answer == "Test answer 1"

    assert second_answer.question == survey_question2
    assert second_answer.seat == seat
    assert second_answer.answer == "Test answer 2"


@pytest.mark.django_db
def test_answer_for_required_question(api_client, survey_question, survey_question2, seat):
    question1_url = reverse("surveyquestion-detail", kwargs={"pk": survey_question.pk})
    question2_url = reverse("surveyquestion-detail", kwargs={"pk": survey_question2.pk})
    seat_url = reverse("seat-detail", kwargs={"pk": seat.pk})

    survey_question.is_required = True
    survey_question2.is_required = True
    survey_question.save()
    survey_question2.save()

    rv = api_client.post(
        reverse("surveyanswer-list"),
        [
            {"question": question1_url, "seat": seat_url, "answer": ""},
            {"question": question2_url, "seat": seat_url, "answer": ""},
        ],
        format="json",
    )
    assert rv.status_code == status.HTTP_400_BAD_REQUEST
    assert question1_url in rv.data
    assert question2_url in rv.data
