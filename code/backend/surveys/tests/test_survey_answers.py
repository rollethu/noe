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
def test_answer_for_required_question(factory, api_client, survey_question, survey_question2, seat):
    request = factory.get("/")
    question1_url = reverse("surveyquestion-detail", request=request, kwargs={"pk": survey_question.pk})
    question2_url = reverse("surveyquestion-detail", request=request, kwargs={"pk": survey_question2.pk})
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


@pytest.mark.django_db
def test_multiple_answer_update(api_client, survey_question, survey_question2, seat):
    survey_question.is_required = True
    survey_question2.is_required = True
    survey_question.save()
    survey_question2.save()

    answer1 = m.SurveyAnswer.objects.create(question=survey_question, answer="OK", seat=seat)
    answer2 = m.SurveyAnswer.objects.create(question=survey_question2, answer="OK", seat=seat)

    answer1_url = reverse("surveyanswer-detail", kwargs={"pk": answer1.pk})
    answer2_url = reverse("surveyanswer-detail", kwargs={"pk": answer2.pk})

    rv = api_client.put(
        reverse("surveyanswer-list"),
        [{"url": answer1_url, "answer": "NOT OK"}, {"url": answer2_url, "answer": "NOT OK"},],
        format="json",
    )
    assert rv.status_code == status.HTTP_200_OK, rv.data

    answer1.refresh_from_db()
    answer2.refresh_from_db()

    assert answer1.answer == "NOT OK"
    assert answer2.answer == "NOT OK"


@pytest.mark.django_db
def test_mulitple_answer_update_errors(factory, api_client, survey_question, survey_question2, seat):
    request = factory.get("/")
    survey_question.is_required = True
    survey_question2.is_required = True
    survey_question.save()
    survey_question2.save()

    answer1 = m.SurveyAnswer.objects.create(question=survey_question, answer="OK", seat=seat)
    answer2 = m.SurveyAnswer.objects.create(question=survey_question2, answer="OK", seat=seat)

    answer1_url = reverse("surveyanswer-detail", request=request, kwargs={"pk": answer1.pk})
    answer2_url = reverse("surveyanswer-detail", request=request, kwargs={"pk": answer2.pk})

    rv = api_client.put(
        reverse("surveyanswer-list", request=request),
        [{"url": answer1_url, "answer": ""}, {"url": answer2_url, "answer": ""},],
        format="json",
    )
    assert rv.status_code == status.HTTP_400_BAD_REQUEST, rv.data
    assert answer1_url in rv.data
    assert answer2_url in rv.data
