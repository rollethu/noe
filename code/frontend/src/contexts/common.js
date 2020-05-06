import * as consts from "./consts";

export const resetState = (dispatch) => () => {
  dispatch({ type: consts.RESET_STATE });
};
