import axios from "axios";

import createContext from "./createContext";
import * as consts from "./consts";

const initialState = {
  surveyQuestions: null,
};

const surveyReducer = (state, action) => {
  switch (action.type) {
    case consts.SET_SURVEY_QUESTIONS:
      return {
        surveyQuestions: action.payload,
      };
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

const sendSurveyAnswers = (dispatch) => async (values) => {
  try {
    const response = await axios.post(consts.SURVEY_ANSWER_LIST_URL, values);
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

export const { Provider, Context } = createContext(
  surveyReducer,
  {
    fetchSurveyQuestions,
    sendSurveyAnswers,
  },
  initialState
);
