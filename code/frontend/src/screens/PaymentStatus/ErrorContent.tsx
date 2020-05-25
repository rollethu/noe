import React from "react";

import PaymentFailedSVG from "../../assets/payment-failed.svg";
import PaymentCancelledSVG from "../../assets/payment-cancelled.svg";
import PaymentTimeoutSVG from "../../assets/payment-timeout.svg";
import { Caption, Image, Text } from "../../UI";

export enum SimplePayEvent {
  FAIL = "FAIL",
  TIMEOUT = "TIMEOUT",
  CANCEL = "CANCEL",
}

interface SimplePayError {
  caption: string;
  errorMessage: string;
  image: string;
}

type ErrorContentProps = {
  simplePayEvent: SimplePayEvent;
  simplePayTransactionId: string;
};

export default function ErrorContent({ simplePayEvent, simplePayTransactionId }: ErrorContentProps) {
  const simplePayError: SimplePayError = { caption: "", errorMessage: "", image: "" };
  switch (simplePayEvent) {
    case SimplePayEvent.FAIL:
      simplePayError.caption = "Sikertelen fizetés";
      simplePayError.errorMessage = "";
      simplePayError.image = PaymentFailedSVG;
      break;
    case SimplePayEvent.TIMEOUT:
      simplePayError.caption = "Időtúllépés";
      simplePayError.errorMessage =
        "Ön túllépte a tranzakció elindításának lehetséges maximális idejét. A 'Vissza gombra tappolva visszairányítjuk a Fizetési mód kiválasztásához.";
      simplePayError.image = PaymentTimeoutSVG;
      break;
    case SimplePayEvent.CANCEL:
      simplePayError.caption = "Megszakított fizetés";
      simplePayError.errorMessage =
        "Ön megszakította a fizetést. A 'Vissza' gombra tappolva visszairányítjuk a Fizetési mód kiválasztásához.";
      simplePayError.image = PaymentCancelledSVG;
      break;
  }

  return (
    <>
      <Image src={PaymentFailedSVG} />
      <Caption center>{simplePayError.caption}</Caption>
      {/*
// @ts-ignore */}
      <Text center>{simplePayError.errorMessage}</Text>
    </>
  );
}
