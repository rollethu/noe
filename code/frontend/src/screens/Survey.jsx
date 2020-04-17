import React from "react";
import { useForm } from "react-hook-form";
import { useHistory } from "react-router-dom";

import { Context as SurveyContext } from "../contexts/surveyContext";
import { Context as SeatContext } from "../contexts/seatContext";
import ProgressBarSVG from "../assets/progressbar_3.svg";
import { View, Caption, Image, Text, Form, Field, Button } from "../UI";
import { ROUTE_ADD_SEAT } from "../App";

export default function Survey() {
  const history = useHistory();
  const {
    state: { surveyQuestions },
    fetchSurveyQuestions,
    sendSurveyAnswers,
  } = React.useContext(SurveyContext);
  let {
    state: { activeSeat },
  } = React.useContext(SeatContext);
  const { register, handleSubmit, errors } = useForm();

  React.useEffect(() => {
    fetchSurveyQuestions();
  }, []);

  async function onSubmit(answers) {
    activeSeat = {
      url:
        "http://localhost:8000/api/seats/6c756135-61c8-477c-ba05-aa38252e5853/",
    };
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
    if (!response.error) {
      history.push(ROUTE_ADD_SEAT);
    }
  }

  if (surveyQuestions === null) {
    return (
      <View>
        <Text>Loading</Text>
      </View>
    );
  }

  return (
    <View>
      <Image src={ProgressBarSVG} />
      <Caption>Kérdőív</Caption>
      <Text>
        Töltse ki az alábbi kérdőívet. Kérjük, valós adatokat adjon meg.
      </Text>
      <Form onSubmit={handleSubmit(onSubmit)}>
        {surveyQuestions.map((question) => (
          <Field
            key={question.url}
            register={register}
            label={question.question}
            errors={errors}
            name={question.url}
          />
        ))}
        <Button type="submit">Tovább</Button>
      </Form>
    </View>
  );
}
