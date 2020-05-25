import React from "react";

import PaymentFailedSVG from "../../assets/payment-failed.svg";
import { Caption, Image, Text } from "../../UI";

export enum SimplePayEvent {
  FAIL = "FAIL",
  TIMEOUT = "TIMEOUT",
  CANCEL = "CANCEL",
}

interface SimplePayError {
  caption: string;
  errorMessage: string;
}

type ErrorContentProps = {
  errorType: SimplePayEvent;
};

export default function ErrorContent({ errorType }: ErrorContentProps) {
  const simplePayError: SimplePayError = { caption: "", errorMessage: "" };
  switch (errorType) {
    case SimplePayEvent.FAIL:
      simplePayError.caption = "Sikertelen fizetés";
      simplePayError.errorMessage = "";
      break;
    case SimplePayEvent.TIMEOUT:
      simplePayError.caption = "Időtúllépés";
      simplePayError.errorMessage =
        "Ön túllépte a tranzakció elindításának lehetséges maximális idejét. A ‘Vissza’ gombra tappolva visszairányítjuk a Fizetési mód kiválasztásához.";
      break;
    case SimplePayEvent.CANCEL:
      simplePayError.caption = "Megszakított fizetés";
      simplePayError.errorMessage =
        "Ön megszakította a fizetést. A ‘Vissza’ gombra tappolva visszairányítjuk a Fizetési mód kiválasztásához.";
      break;
  }

  return (
    <>
      <Caption>{simplePayError.caption}</Caption>
      <Image src={PaymentFailedSVG} />
      {/*
// @ts-ignore */}
      <Text>{simplePayError.errorMessage}</Text>
    </>
  );
}
