import axios from "axios";

import createContext from "./createContext";
import * as consts from "./consts";
import * as common from "./common";

export const initialState = {
  appointment: {
    url: null,
    email: null,
    isEmailVerified: null,
  },
  emailVerification: {
    error: null,
  },
  productID: null,
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
    case consts.SET_PRODUCT:
      return {
        ...state,
        productID: action.payload,
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

export const verifyToken = (dispatch) => async (token) => {
  try {
    const response = await axios.post(consts.VERIFY_EMAIL_URL, {
      token,
    });
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
    const response = await axios.post(consts.RESEND_EMAIL_VERIFICATION_URL, {
      uuid,
    });
    response.error = false;
    return response;
  } catch (error) {
    const { response } = error;
    if (response === undefined) {
      return { error: true };
    }
    response.error = true;
    return response;
  }
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

const setProduct = (dispatch) => (productID) => {
  dispatch({ type: consts.SET_PRODUCT, payload: productID });
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
    resetState: common.resetState,
    setState: common.setState,
  },
  initialState
);
