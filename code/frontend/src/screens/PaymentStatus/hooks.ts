import React from "react";

import { Context as AppointmentContext } from "../../contexts/appointmentContext";
import { Context as SeatContext } from "../../contexts/seatContext";
import { Context as surveyContext } from "../../contexts/surveyContext";
import * as contextUtils from "../../contexts/utils";

export function usePopStateFromLocalStorage() {
  const { setState: setAppointmentState } = React.useContext(AppointmentContext);
  const { setState: setSeatState } = React.useContext(SeatContext);
  const { setState: setSurveyState } = React.useContext(surveyContext);

  const setters = {
    setAppointmentState,
    setSeatState,
    setSurveyState,
  };

  React.useEffect(() => {
    contextUtils.loadStateFromLocalStorage(setters);
  }, []);
}
