import React from "react";
import { useLocation } from "react-router-dom";

import { View, LinkButton } from "../../UI";
import { ROUTE_PAYMENT_METHODS } from "../../App";
import ErrorContent, { SimplePayEvent } from "./ErrorContent";
import * as consts from "./consts";
import { usePopStateFromLocalStorage } from "./hooks";

export default function PaymentFailed() {
  usePopStateFromLocalStorage();
  const location = useLocation();
  const params = new URLSearchParams(location.search);

  const simplePayEvent = params.get(consts.SIMPLEPAY_TRANSACTION_EVENT) as SimplePayEvent;
  const simplePayTransactionId = params.get(consts.SIMPLEPAY_TRANSACTION_ID) as string;

  return (
    <View>
      <ErrorContent simplePayEvent={simplePayEvent} simplePayTransactionId={simplePayTransactionId} />
      {/*
      // @ts-ignore */}
      <LinkButton toCenter to={ROUTE_PAYMENT_METHODS}>
        Vissza
      </LinkButton>
    </View>
  );
}
