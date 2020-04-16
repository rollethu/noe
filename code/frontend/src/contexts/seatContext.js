import axios from "axios";

import createContext from "./createContext";
import * as consts from "./consts";

const initialState = {};

const seatReducer = (state, action) => {
  switch (action.type) {
    case consts.SET_SEATS:
      return {
        ...state,
        ...action.payload,
      };
    default:
      return state;
  }
};

const createSeat = (dispatch) => async (values) => {
  try {
    const response = await axios.post(consts.SEAT_LIST_URL, values);
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
  seatReducer,
  {
    createSeat,
  },
  initialState
);
