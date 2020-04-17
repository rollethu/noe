import axios from "axios";

import createContext from "./createContext";
import * as consts from "./consts";

const initialState = {
  seats: [],
};

const seatReducer = (state, action) => {
  switch (action.type) {
    case consts.SET_SEATS:
      return {
        ...state,
        seats: [...state.seats, ...action.payload],
      };
    case consts.ADD_SEAT:
      return {
        ...state,
        seats: [...state.seats, action.payload],
      };
    default:
      return state;
  }
};

const createSeat = (dispatch) => async (values) => {
  try {
    const response = await axios.post(consts.SEAT_LIST_URL, values);
    dispatch({ type: consts.ADD_SEAT, payload: response.data });
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
