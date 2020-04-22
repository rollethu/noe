import React from "react";
import { useHistory } from "react-router-dom";

import { Context as SeatContext } from "../../contexts/seatContext";
import { Context as SurveyContext } from "../../contexts/surveyContext";
import ProgressBarSVG from "../../assets/progressbar_3.svg";
import { View, Caption, Image, Text } from "../../UI";
import SurveyForm from "./SurveyForm";

export default function Survey() {
  const history = useHistory();
  const {
    state: { surveyQuestions, activeSurvey },
    sendSurveyAnswers,
    updateSurveyAnswers,
    setActiveSurveyAnswers,
    fetchSurveyQuestions,
  } = React.useContext(SurveyContext);
  const {
    state: { activeSeat },
    setActiveSeat,
  } = React.useContext(SeatContext);

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
      <SurveyForm
        surveyQuestions={surveyQuestions}
        activeSurvey={activeSurvey}
        sendSurveyAnswers={sendSurveyAnswers}
        updateSurveyAnswers={updateSurveyAnswers}
        setActiveSurveyAnswers={setActiveSurveyAnswers}
        activeSeat={activeSeat}
        setActiveSeat={setActiveSeat}
        history={history}
      />
    </View>
  );
}
