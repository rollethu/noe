import axios from "axios";

import createContext from "./createContext";
import * as consts from "./consts";

const initialState = {
  locations: null,
};

const locationReducer = (state, action) => {
  switch (action.type) {
    case consts.SET_LOCATIONS:
      return {
        locations: action.payload,
      };
    default:
      return state;
  }
};

const fetchLocations = (dispatch) => async () => {
  try {
    const response = await axios.get(consts.LOCATION_LIST_URL);
    dispatch({ type: consts.SET_LOCATIONS, payload: response.data });
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
  locationReducer,
  {
    fetchLocations,
  },
  initialState
);
