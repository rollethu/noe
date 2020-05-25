import React from "react";
import { useHistory, useLocation } from "react-router-dom";

import PaymentPendingSVG from "../../assets/payment-pending.svg";
import { View, Caption, Image, Text } from "../../UI";
import { Context as AppointmentContext } from "../../contexts/appointmentContext";
import { ROUTE_APPOINTMENT_SUCCESS, ROUTE_PAYMENT_FAILED } from "../../App";
import * as consts from "./consts";
import { usePopStateFromLocalStorage } from "./hooks";

export default function PaymentStatus() {
  usePopStateFromLocalStorage();
  const history = useHistory();
  const location = useLocation();
  const params = new URLSearchParams(location.search);

  const simplePayTransactionId = params.get(consts.SIMPLEPAY_TRANSACTION_ID);

  const { fetchPaymentStatus } = React.useContext(AppointmentContext);
  let pollId = null;

  React.useEffect(() => {
    pollId = setInterval(() => {
      doPoll();
    }, 3000);

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
      history.push(ROUTE_APPOINTMENT_SUCCESS, { simplePayTransactionId });
    } else if (paymentStatus === "PENDING") {
      return; // continue polling
    } else {
      clearInterval(pollId);
      history.push("/payment-failed");
    }
  }

  return (
    <View>
      <Caption center>Fizetés folyamatban</Caption>
      <Image src={PaymentPendingSVG} />
      {/*
// @ts-ignore */}
      <Text>Tranzakció folyamatban, ez eltarthat pár percig. Kérjük szíves türelmét.</Text>
    </View>
  );
}
