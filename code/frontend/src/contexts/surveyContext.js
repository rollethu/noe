import axios from "axios";

import createContext from "./createContext";
import * as consts from "./consts";
import * as utils from "./utils";

/*
Example `surveyAnswers`:
{
  http://seatUrl1: [
    {answer1 details},
    {answer2 details}
  ]
}
*/

const initialState = {
  surveyQuestions: null,
  surveyAnswers: {},
  activeSurvey: null, // To update existing survey questions
};

const surveyReducer = (state, action) => {
  let newState;
  switch (action.type) {
    case consts.SET_SURVEY_QUESTIONS:
      return {
        ...state,
        surveyQuestions: action.payload,
      };
    case consts.SET_NEW_SURVEY_ANSWERS:
      newState = {
        ...state,
        surveyAnswers: {
          ...state.surveyAnswers,
          ...action.payload, // {seatUrl: [{Answer Details}, {Answer Details}]}
        },
      };
      return newState;
    case consts.SET_ACTIVE_SURVEY_ANSWERS:
      newState = {
        ...state,
        activeSurvey: state.surveyAnswers[action.payload.seat],
      };
      return newState;
    default:
      return state;
  }
};

const fetchSurveyQuestions = (dispatch) => async () => {
  const response = await utils.handleRequest(() =>
    axios.get(consts.SURVEY_QUESTION_LIST_URL)
  );

  if (!response.error) {
    dispatch({ type: consts.SET_SURVEY_QUESTIONS, payload: response.data });
  }

  return response;
};

function groupAnswersBySeat(answers) {
  if (answers.length === 0) {
    return {};
  }

  const seat = answers[0].seat; // all answers must have the same Seat
  return { [seat]: answers }; // Overrides existing keys (when updates)
}

export const sendSurveyAnswers = (dispatch) => async (values) => {
  const response = await utils.handleRequest(() =>
    axios.post(consts.SURVEY_ANSWER_LIST_URL, values)
  );

  if (!response.error) {
    dispatch({
      type: consts.SET_NEW_SURVEY_ANSWERS,
      payload: groupAnswersBySeat(response.data),
    });
  }

  return response;
};

export const updateSurveyAnswers = (dispatch) => async (surveyAnswerList) => {
  try {
    // const response = await axios.patch(consts.SURVEY_ANSWER_LIST_URL, surveyAnswerList);
    // dispatch({ type: consts.ADD_SURVEY_ANSWERS, payload: response.data });
    // dispatch({ type: consts.SET_NEW_SURVEY_ANSWERS, payload: surveyAnswerList });
    dispatch({
      type: consts.SET_NEW_SURVEY_ANSWERS,
      payload: groupAnswersBySeat(surveyAnswerList),
    });
    return { error: false };
    // response.error = false;
    // return response;
  } catch (error) {
    const { response } = error;
    if (!response) {
      return {
        error: true,
      };
    }
    response.error = true;
    response.errors = response.data;
    return response;
  }
};

const setActiveSurveyAnswers = (dispatch) => (seat) => {
  const newValue = seat === null ? null : seat.url;
  dispatch({
    type: consts.SET_ACTIVE_SURVEY_ANSWERS,
    payload: { seat: newValue },
  });
};

export const { Provider, Context } = createContext(
  surveyReducer,
  {
    fetchSurveyQuestions,
    sendSurveyAnswers,
    setActiveSurveyAnswers,
    updateSurveyAnswers,
  },
  initialState
);
