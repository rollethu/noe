import axios from "axios";

import createContext from "./createContext";
import * as consts from "./consts";
import * as utils from "../utils";
import * as common from "./common";

const initialState = {
  timeSlots: null,
  selectedTimeSlot: null,
};

const timeSlotReducer = (state, action) => {
  switch (action.type) {
    case consts.SET_TIME_SLOTS:
      return { ...state, timeSlots: action.payload };
    case consts.SET_SELECTED_TIME_SLOT:
      return { ...state, selectedTimeSlot: action.payload };
    case consts.RESET_STATE:
      return initialState;
    default:
      return state;
  }
};

const fetchTimeSlots = (dispatch) => async (filters) => {
  const queryParams = utils.getQueryParamsFromObject(filters);
  try {
    const response = await axios.get(consts.TIME_SLOT_LIST_URL + queryParams);
    dispatch({ type: consts.SET_TIME_SLOTS, payload: response.data });
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

const fetchSelectedTimeSlot = (dispatch) => async (url) => {
  try {
    const response = await axios.get(url);
    dispatch({ type: consts.SET_SELECTED_TIME_SLOT, payload: response.data });
  } catch (error) {
    console.log("Error", error);
  }
};

export const { Provider, Context } = createContext(
  timeSlotReducer,
  {
    fetchTimeSlots,
    fetchSelectedTimeSlot,
    resetState: common.resetState,
  },
  initialState
);
