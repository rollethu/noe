import axios from "axios";

import createContext from "./createContext";
import * as consts from "./consts";

const initialState = {
  appointmentUrl: null,
};

const appointmentReducer = (state, action) => {
  switch (action.type) {
    case consts.CREATE_APPOINTMENT:
      return { appointmentUrl: action.payload.url };
    default:
      return state;
  }
};

const createAppointment = (dispatch) => async (values) => {
  try {
    const response = await axios.post(consts.APPOINTMENT_LIST_URL, values);
    dispatch({ type: consts.CREATE_APPOINTMENT, payload: response.data });
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
  appointmentReducer,
  {
    createAppointment,
  },
  initialState
);
