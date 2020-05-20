import React from "react";
import { View } from "../../UI";
import { useHistory } from "react-router-dom";

import { Context as AppointmentContext } from "../../contexts/appointmentContext";
import { Context as SeatContext } from "../../contexts/seatContext";
import { Context as surveyContext } from "../../contexts/surveyContext";
import * as contextUtils from "../../contexts/utils";
import { ROUTE_APPOINTMENT_SUCCESS, ROUTE_PAYMENT_FAILED } from "../../App";

export default function PaymentStatus() {
  const history = useHistory();
  const { setState: setAppointmentState, fetchPaymentStatus } = React.useContext(AppointmentContext);
  const { setState: setSeatState } = React.useContext(SeatContext);
  const { setState: setSurveyState } = React.useContext(surveyContext);
  let pollId = null;

  React.useEffect(() => {
    pollId = setInterval(() => {
      doPoll();
    }, 3000);
    const setters = {
      setAppointmentState,
      setSeatState,
      setSurveyState,
    };
    contextUtils.loadStateFromLocalStorage(setters);
    return () => {
      clearInterval(pollId);
    };
  }, []);

  async function doPoll() {
    const response = await fetchPaymentStatus();

    if (response.error) {
      history.push(ROUTE_PAYMENT_FAILED);
      return;
    }

    const { payment_status: paymentStatus } = response.data;
    if (paymentStatus === "SUCCESS") {
      clearInterval(pollId);
      history.push(ROUTE_APPOINTMENT_SUCCESS);
    } else if (paymentStatus === "PENDING") {
      return; // continue polling
    } else {
      clearInterval(pollId);
      history.push("/payment-failed");
    }
  }

  return <View>Payment Status Page</View>;
}
