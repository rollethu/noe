import React from "react";
import { useLocation } from "react-router-dom";

import { View, LinkButton } from "../../UI";
import { ROUTE_PAYMENT_METHODS } from "../../App";
import ErrorContent, { SimplePayEvent } from "./ErrorContent";

const SIMPLEPAY_TRANSACTION_EVENT = "simplepay_transaction_event";
const SIMPLEPAY_TRANSACTION_ID = "simplepay_transaction_id";

export default function PaymentFailed(props) {
  const location = useLocation();
  const params = new URLSearchParams(location.search);

  const simplePayEvent = params.get(SIMPLEPAY_TRANSACTION_EVENT) as SimplePayEvent;
  const simplePayTransactionId = params.get(SIMPLEPAY_TRANSACTION_ID) as string;

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
