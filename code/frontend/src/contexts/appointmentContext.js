import axios from "axios";

import createContext from "./createContext";
import * as consts from "./consts";

const initialState = {
  appointment: {
    url: null,
    email: null,
    isEmailVerified: null,
  },
  tokenVerificationError: null,
};

const appointmentReducer = (state, action) => {
  switch (action.type) {
    case consts.SET_APPOINTMENT:
      return {
        ...state,
        appointment: {
          ...state.appointment,
          ...action.payload,
        },
      };
    case consts.SET_TOKEN_VERIFICATION_ERROR:
      return {
        ...state,
        ...action.payload,
      };
    default:
      return state;
  }
};

const createAppointment = (dispatch) => async (values) => {
  try {
    const response = await axios.post(consts.APPOINTMENT_LIST_URL, values);
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

const updateAppointment = (dispatch) => async (url, values) => {
  try {
    const response = await axios.patch(url, values);
    response.error = false;
    dispatch({ type: consts.SET_APPOINTMENT, payload: response.data });
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

const verifyToken = (dispatch) => async (token) => {
  try {
    const response = await axios.post(consts.VERIFY_EMAIL_URL, {
      token,
    });
    dispatch({
      type: consts.SET_APPOINTMENT,
      payload: {
        url: response.data.appointment_url,
        email: response.data.appointment_email,
        isEmailVerified: true,
      },
    });
  } catch (error) {
    dispatch({
      type: consts.SET_APPOINTMENT,
      payload: {
        isEmailVerified: false,
      },
    });
    dispatch({
      type: consts.SET_TOKEN_VERIFICATION_ERROR,
      payload: {
        tokenVerificationError: error.response.data,
      },
    });
  }
};

export const { Provider, Context } = createContext(
  appointmentReducer,
  {
    createAppointment,
    updateAppointment,
    verifyToken,
  },
  initialState
);
