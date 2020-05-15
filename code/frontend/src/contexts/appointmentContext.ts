import axios from "axios";

import createContext from "./createContext";
import * as consts from "./consts";
import * as common from "./common";
import { AppointmentState } from "./interfaces";

export const initialState: AppointmentState = {
  appointment: {
    url: null,
    email: null,
    isEmailVerified: null,
  },
  emailVerification: {
    error: null,
  },
  productId: null,
};

const appointmentReducer = (state: AppointmentState, action) => {
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
    case consts.SET_PRODUCT:
      return {
        ...state,
        productId: action.payload,
      };
    case consts.RESET_STATE:
      return initialState;
    case consts.SET_STATE:
      return action.payload;
    default:
      return state;
  }
};

const createAppointment = (dispatch) => async (values) => {
  let response;

  try {
    response = await axios.post(consts.APPOINTMENT_LIST_URL, values);
  } catch (error) {
    return { error: true, errors: error?.response?.data || [] };
  }

  dispatch({
    type: consts.SET_TOKEN_VERIFICATION,
    payload: { uuid: response.data.email_verification_uuid },
  });
  return response;
};

const updateAppointment = (dispatch) => async (url, values) => {
  let response;

  try {
    response = await axios.patch(url, values);
  } catch (error) {
    return { error: true, errors: error?.response?.data || [] };
  }

  dispatch({ type: consts.SET_APPOINTMENT, payload: response.data });
  return response;
};

export const verifyToken = (dispatch) => async (token) => {
  let response;

  try {
    response = await axios.post(consts.VERIFY_EMAIL_URL, { token });
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
    return { error: true, errors: error?.response?.data || [] };
  }

  axios.defaults.headers.common["Authorization"] = `Apptoken ${token}`;
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
  return response;
};

const resendEmailVerification = (dispatch) => async (uuid) => {
  let response;

  try {
    response = await axios.post(consts.RESEND_EMAIL_VERIFICATION_URL, { uuid });
  } catch (error) {
    return { error: true, errors: error?.response?.data || [] };
  }

  return response;
};

const fetchPrice = (dispatch) => async (values) => {
  let response;

  try {
    response = await axios.post(consts.GET_PRICE_URL, values);
  } catch (error) {
    return { error: true, errors: error?.response?.data || [] };
  }

  dispatch({
    type: consts.SET_APPOINTMENT_PRICE,
    payload: {
      total_price: response.data.total_price,
      currency: response.data.currency,
    },
  });
  return response;
};

const setProduct = (dispatch) => (productId) => {
  dispatch({ type: consts.SET_PRODUCT, payload: productId });
};

const setState = (dispatch) => (newState) => {
  dispatch({ type: consts.SET_STATE, payload: newState });
};

export const { Provider, Context } = createContext(
  appointmentReducer,
  {
    createAppointment,
    updateAppointment,
    verifyToken,
    resendEmailVerification,
    fetchPrice,
    setProduct,
    setState,
    resetState: common.resetState,
  },
  initialState
);
