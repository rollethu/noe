import * as consts from "./consts";

export const resetState = (dispatch) => () => {
  dispatch({ type: consts.RESET_STATE });
};

export const setState = (dispatch) => (newState) => {
  dispatch({ type: consts.SET_STATE, payload: newState });
};
