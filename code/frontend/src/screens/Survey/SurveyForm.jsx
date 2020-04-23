import React from "react";
import { useForm } from "react-hook-form";

import { Form, Field, NextButton, Toggle, InputGroup, Label } from "../../UI";
import { ROUTE_ADD_SEAT } from "../../App";
import * as utils from "../../utils";

const toggleOptions = [
  { value: "yes", text: "Igen" },
  { value: "no", text: "Nem" },
];

function getFieldTypeFromSurveyAnswerType(question) {
  switch (question.answer_datatype) {
    case "BOOLEAN":
      return "survey-toggle";
    case "INTEGER":
      return "number";
    // including `STRING`
    default:
      return "text";
  }
}

const SUBMIT_MODE_CREATE = "CREATE";
const SUBMIT_MODE_UPDATE = "UPDATE";

function getSubmitMode(surveyAnswersForActiveSeat) {
  return surveyAnswersForActiveSeat === null
    ? SUBMIT_MODE_CREATE
    : SUBMIT_MODE_UPDATE;
}

function getFormData(submitMode, surveyQuestions, surveyAnswersForActiveSeat) {
  if (submitMode === SUBMIT_MODE_CREATE) {
    return getFormDataForCreation(surveyQuestions);
  }

  return getFormDataForUpdate(surveyQuestions, surveyAnswersForActiveSeat);
}

function getFormDataForCreation(surveyQuestions) {
  return surveyQuestions.map((question) => {
    const fieldType = getFieldTypeFromSurveyAnswerType(question);
    return {
      label: question.question,
      name: question.url, // To create answers based on the question url
      type: fieldType,
      defaultValue: fieldType === "survey-toggle" ? "no" : "",
    };
  });
}

function getFormDataForUpdate(surveyQuestions, surveyAnswersForActiveSeat) {
  return surveyQuestions.map((question) => {
    const existingAnswer = surveyAnswersForActiveSeat.filter(
      (answer) => answer.question === question.url
    )[0];
    return {
      label: question.question,
      name: existingAnswer.url, // To update existing answers based on their urls
      type: getFieldTypeFromSurveyAnswerType(question),
      defaultValue: existingAnswer.answer,
    };
  });
}

export default function SurveyForm({
  surveyQuestions,
  surveyAnswersForActiveSeat,
  sendSurveyAnswers,
  updateSurveyAnswers,
  setActiveSurveyAnswers,
  activeSeat,
  setActiveSeat,
  history,
}) {
  const { register, handleSubmit, errors, setError } = useForm();
  const submitMode = getSubmitMode(surveyAnswersForActiveSeat);
  const formData = getFormData(
    submitMode,
    surveyQuestions,
    surveyAnswersForActiveSeat
  );

  const onSubmit = (values) => {
    if (!activeSeat) {
      alert("No active seat");
      return;
    }

    if (submitMode === SUBMIT_MODE_CREATE) {
      onCreateSubmit(values);
    } else {
      onUpdateSubmit(values);
    }

    setActiveSeat(null);
    setActiveSurveyAnswers(null);
  };

  async function onCreateSubmit(values) {
    const processedAnswers = Object.keys(values).map((questionUrl) => ({
      question: questionUrl,
      answer: values[questionUrl],
      seat: activeSeat.url,
    }));
    const response = await sendSurveyAnswers(processedAnswers);
    utils.handleResponse({
      response,
      setError,
      history,
      redirectRoute: ROUTE_ADD_SEAT,
    });
  }

  async function onUpdateSubmit(values) {
    const processedAnswers = Object.keys(values).map((answerUrl) => ({
      url: answerUrl,
      answer: values[answerUrl],
      seat: activeSeat.url,
      question: surveyAnswersForActiveSeat.filter(
        (answer) => answer.url === answerUrl
      )[0].question,
    }));
    const response = await updateSurveyAnswers(processedAnswers);
    utils.handleResponse({
      response,
      setError,
      history,
      redirectRoute: ROUTE_ADD_SEAT,
    });
  }

  return (
    <Form onSubmit={handleSubmit(onSubmit)}>
      {formData.map((field) => {
        // May be a question (create) or an answer (update)
        if (field.type === "survey-toggle") {
          return (
            <InputGroup key={field.name}>
              <Label>{field.label}</Label>
              <Toggle
                register={register}
                options={toggleOptions}
                name={field.name} // question url for creation, answer url for update
                defaultValue={field.defaultValue}
              />
            </InputGroup>
          );
        }
        return (
          <Field
            key={field.name}
            register={register}
            label={field.label}
            errors={errors}
            name={field.name} // question url for creation, answer url for update
            type={field.type}
            defaultValue={field.defaultValue}
          />
        );
      })}
      <NextButton type="submit" />
    </Form>
  );
}
