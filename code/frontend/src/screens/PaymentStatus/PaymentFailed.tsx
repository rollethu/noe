import React from "react";

import { View, LinkButton } from "../../UI";
import { ROUTE_PAYMENT_METHODS } from "../../App";
import ErrorContent, { SimplePayEvent } from "./ErrorContent";

export default function PaymentFailed(props) {
  const errorType = props.location.search.error_type as SimplePayEvent;
  return (
    <View>
      <ErrorContent errorType={errorType} />
      {/*
// @ts-ignore */}
      <LinkButton toCenter to={ROUTE_PAYMENT_METHODS}>
        Újrapróbálom
      </LinkButton>
    </View>
  );
}
