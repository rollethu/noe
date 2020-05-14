import React from "react";
import { View } from "../../UI";

import { Context as AppointmentContext } from "../../contexts/appointmentContext";
import { Context as SeatContext } from "../../contexts/seatContext";
import { Context as surveyContext } from "../../contexts/surveyContext";
import { ROUTE_APPOINTMENT_SUCCESS } from "../../App";
import { useHistory } from "react-router-dom";

export default function PaymentStatus() {
  const { history } = useHistory();
  let pollId = null;

  React.useEffect(() => {
    pollId = setTimeout(() => {
      doPoll();
    }, 3000);
    return () => {
      clearInterval(pollId);
    };
  });

  async function doPoll() {
    // const response = await fetchPaymentStatus();
    const response = null;

    if (response.error) {
      history.push("/payment-failed");
      return;
    }

    clearInterval(pollId);
    const { payment_status: paymentStatus } = response.data;
    if (paymentStatus === "SUCCESS") {
      history.push(ROUTE_APPOINTMENT_SUCCESS);
    } else if (paymentStatus === "PENDING") {
      return; // let the poll continue
    } else {
      history.push("/payment-failed");
    }
  }

  return <View>Payment Status Page</View>;
}
