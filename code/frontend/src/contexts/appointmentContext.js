import axios from "axios";

import createContext from "./createContext";
import * as consts from "./consts";

const initialState = {
  appointmentUrl: null,
  appointmentEmail: null,
  isAppointmentEmailVerified: null,
};

const appointmentReducer = (state, action) => {
  switch (action.type) {
    case consts.SET_APPOINTMENT:
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

const verifyToken = (dispatch) => async (token) => {
  try {
    const response = await axios.post(consts.VERIFY_EMAIL_URL, {
      verification_token: token,
    });
    dispatch({
      type: consts.SET_APPOINTMENT,
      payload: {
        appointmentUrl: response.data.appointment_url,
        appointmentEmail: response.data.appointment_email,
        isAppointmentEmailVerified: true,
      },
    });
  } catch (error) {
    dispatch({
      type: consts.SET_APPOINTMENT,
      payload: {
        appointmentUrl: null,
        appointmentEmail: null,
        isAppointmentEmailVerified: false,
      },
    });
  }
};

export const { Provider, Context } = createContext(
  appointmentReducer,
  {
    createAppointment,
    verifyToken,
  },
  initialState
);
