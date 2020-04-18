import React from "react";
import { useForm } from "react-hook-form";
import { useHistory } from "react-router-dom";

import { Context as SurveyContext } from "../../contexts/surveyContext";
import { Context as SeatContext } from "../../contexts/seatContext";
import { Form, Field, Button } from "../../UI";
import { ROUTE_ADD_SEAT } from "../../App";
import * as utils from "../../utils";

function getFieldTypeFromSurveyAnswerType(question) {
  switch (question.answer_datatype) {
    case "boolean":
      return "survey-toggle";
    case "integer":
      return "number";
    // including `string`
    default:
      return "text";
  }
}

export default function SurveyForm() {
  const history = useHistory();
  const { register, handleSubmit, errors, setError } = useForm();
  const {
    state: { activeSeat },
  } = React.useContext(SeatContext);
  const {
    state: { surveyQuestions },
    sendSurveyAnswers,
  } = React.useContext(SurveyContext);

  async function onSubmit(answers) {
    if (!activeSeat) {
      alert("No active seat");
      return;
    }

    const processedAnswers = Object.keys(answers).map((questionUrl) => ({
      question: questionUrl,
      answer: answers[questionUrl],
      seat: activeSeat.url,
    }));

    const response = await sendSurveyAnswers(processedAnswers);
    utils.handleResponse({
      response,
      setError,
      history,
      ROUTE_ADD_SEAT,
    });
  }

  return (
    <Form onSubmit={handleSubmit(onSubmit)}>
      {surveyQuestions.map((question) => (
        <Field
          key={question.url}
          register={register}
          label={question.question}
          errors={errors}
          name={question.url}
          type={getFieldTypeFromSurveyAnswerType(question)}
        />
      ))}
      <Button type="submit">Tovább</Button>
    </Form>
  );
}
