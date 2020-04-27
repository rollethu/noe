import React from "react";
import { useHistory } from "react-router-dom";

import { Context as SeatContext } from "../../contexts/seatContext";
import { Context as SurveyContext } from "../../contexts/surveyContext";
import ProgressBarSVG from "../../assets/progressbar_3.svg";
import { View, Caption, Image, Text } from "../../UI";
import SurveyForm from "./SurveyForm";
import * as utils from "../../utils";
import * as surveyUtils from "./utils";

export default function Survey() {
  const history = useHistory();
  const {
    state: { surveyQuestions, surveyAnswersForActiveSeat },
    sendSurveyAnswers,
    updateSurveyAnswers,
    setActiveSurveyAnswers,
    fetchSurveyQuestions,
  } = React.useContext(SurveyContext);
  const {
    state: { activeSeat },
    setActiveSeat,
  } = React.useContext(SeatContext);

  const submitMode = surveyUtils.getSubmitMode(surveyAnswersForActiveSeat);

  React.useEffect(() => {
    fetchSurveyQuestions();
  }, []);

  const onSubmit = (values, setError) => {
    if (!activeSeat) {
      alert("No active seat");
      return;
    }

    if (submitMode === surveyUtils.SUBMIT_MODE_CREATE) {
      onCreateSubmit(values, setError);
    } else {
      onUpdateSubmit(values, setError);
    }
  };

  async function onCreateSubmit(values, setError) {
    const processedAnswers = surveyUtils.processCreateValues(
      values,
      activeSeat,
      surveyQuestions
    );
    const response = await sendSurveyAnswers(processedAnswers);
    response.errors = surveyUtils.matchQuestionErrors(
      response.errors,
      surveyQuestions
    );
    utils.handleResponse({
      response,
      setError,
      history,
      redirectRoute: surveyUtils.getRedirectRoute(submitMode),
    });

    if (!response.error) {
      setActiveSeat(null);
      setActiveSurveyAnswers(null);
    }
  }

  async function onUpdateSubmit(values, setError) {
    const processedAnswers = surveyUtils.processUpdateValues(
      values,
      surveyAnswersForActiveSeat
    );

    const response = await updateSurveyAnswers(processedAnswers);
    response.errors = surveyUtils.matchAnswerErrors(
      response.errors,
      surveyAnswersForActiveSeat
    );
    utils.handleResponse({
      response,
      setError,
      history,
      redirectRoute: surveyUtils.getRedirectRoute(submitMode),
    });

    if (!response.error) {
      setActiveSeat(null);
      setActiveSurveyAnswers(null);
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
      <SurveyForm
        submitMode={submitMode}
        surveyQuestions={surveyQuestions}
        surveyAnswersForActiveSeat={surveyAnswersForActiveSeat}
        onSubmit={onSubmit}
      />
    </View>
  );
}
