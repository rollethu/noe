import axios from "axios";

import createContext from "./createContext";
import * as consts from "./consts";

const initialState = {
  appointment: {
    url:
      "http://localhost:8000/api/appointments/35bd70e1-831b-41b4-812c-b0b45b4abd0f/",
    email: null,
    isEmailVerified: null,
  },
  emailVerification: {
    error: null,
  },
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
    case consts.SET_TOKEN_VERIFICATION:
      return {
        ...state,
        emailVerification: {
          ...state.emailVerification,
          ...action.payload,
        },
      };
    case consts.SET_APPOINTMENT_PRICE:
      return {
        ...state,
        appointment: {
          ...state.appointment,
          ...action.payload,
        },
      };
    default:
      return state;
  }
};

const createAppointment = (dispatch) => async (values) => {
  try {
    const response = await axios.post(consts.APPOINTMENT_LIST_URL, values);
    dispatch({
      type: consts.SET_TOKEN_VERIFICATION,
      payload: { uuid: response.data.email_verification_uuid },
    });
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
    dispatch({
      type: consts.SET_TOKEN_VERIFICATION,
      payload: { error: null },
    });
  } catch (error) {
    dispatch({
      type: consts.SET_APPOINTMENT,
      payload: {
        isEmailVerified: false,
      },
    });
    dispatch({
      type: consts.SET_TOKEN_VERIFICATION,
      payload: { error: error.response.data },
    });
  }
};

const resendEmailVerification = (dispatch) => async (uuid) => {
  try {
    await axios.post(consts.RESEND_EMAIL_VERIFICATION_URL, {
      uuid,
    });
  } catch (error) {}
};

const fetchPrice = (dispatch) => async (values) => {
  try {
    const response = await axios.post(consts.GET_PRICE_URL, values);
    dispatch({
      type: consts.SET_APPOINTMENT_PRICE,
      payload: {
        total_price: response.data.total_price,
        currency: response.data.currency,
      },
    });
    response.error = false;
    return response;
  } catch (error) {
    const response = error.response;
    response.error = true;
    return response;
  }
};

export const { Provider, Context } = createContext(
  appointmentReducer,
  {
    createAppointment,
    updateAppointment,
    verifyToken,
    resendEmailVerification,
    fetchPrice,
  },
  initialState
);
