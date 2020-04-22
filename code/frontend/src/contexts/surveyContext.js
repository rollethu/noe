import axios from "axios";

import createContext from "./createContext";
import * as consts from "./consts";

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
  let newState, seat, answersGroupedBySeat;
  switch (action.type) {
    case consts.SET_SURVEY_QUESTIONS:
      return {
        ...state,
        surveyQuestions: action.payload,
      };
    case consts.ADD_SURVEY_ANSWERS:
      newState = {
        ...state,
        surveyAnswers: {
          ...state.surveyAnswers,
          ...action.payload, // {seatUrl: [{Answer Details}, {Answer Details}]}
        },
      };
      return newState;
    case consts.UPDATE_SURVEY_ANSWERS:
      seat = action.payload[0].seat; // all answers must have the same Seat
      answersGroupedBySeat = { [seat]: action.payload }; // Overrides existing answers
      newState = {
        ...state,
        surveyAnswers: {
          ...state.surveyAnswers,
          ...answersGroupedBySeat, // {seatUrl: [{Answer Details}, {Answer Details}]}
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
  try {
    const response = await axios.get(consts.SURVEY_QUESTION_LIST_URL);
    dispatch({ type: consts.SET_SURVEY_QUESTIONS, payload: response.data });
    response.error = false;
    return response;
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

function groupAnswersBySeat(answers) {
  if (answers.length === 0) {
    return {};
  }

  const seat = answers[0].seat; // all answers must have the same Seat
  return { [seat]: answers };
}

export const sendSurveyAnswers = (dispatch) => async (values) => {
  try {
    const response = await axios.post(consts.SURVEY_ANSWER_LIST_URL, values);
    const action = {
      type: consts.ADD_SURVEY_ANSWERS,
      payload: groupAnswersBySeat(response.data),
    };
    dispatch(action);
    response.error = false;
    return response;
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

const updateSurveyAnswers = (dispatch) => async (surveyAnswerList) => {
  try {
    // const response = await axios.patch(consts.SURVEY_ANSWER_LIST_URL, surveyAnswerList);
    // dispatch({ type: consts.ADD_SURVEY_ANSWERS, payload: response.data });
    dispatch({ type: consts.UPDATE_SURVEY_ANSWERS, payload: surveyAnswerList });
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
