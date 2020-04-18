import React from "react";

import { Context as SurveyContext } from "../../contexts/surveyContext";
import ProgressBarSVG from "../../assets/progressbar_3.svg";
import { View, Caption, Image, Text } from "../../UI";
import SurveyForm from "./SurveyForm";

export default function Survey() {
  const {
    state: { surveyQuestions },
    fetchSurveyQuestions,
  } = React.useContext(SurveyContext);

  React.useEffect(() => {
    fetchSurveyQuestions();
  }, []);

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
      <SurveyForm surveyQuestions={surveyQuestions} />
    </View>
  );
}
