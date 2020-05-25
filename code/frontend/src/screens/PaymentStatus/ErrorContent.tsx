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
      simplePayError.errorMessage = `SimplePay tranzakció azonosító: ${simplePayTransactionId} Kérjük, ellenőrizze a tranzakció során megadott adatok helyességét és próbálja újra! Amennyiben minden adatot helyesen adott meg, a visszautasítás okának kivizsgálása érdekében kérjük, szíveskedjen kapcsolatba lépni kártyakibocsátó bankjával.`;
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
    default:
      simplePayError.caption = "Ismeretlen hiba történt";
      simplePayError.image = PaymentFailedSVG;
  }

  return (
    <>
      <Caption center>{simplePayError.caption}</Caption>
      <Image src={simplePayError.image} />
      {/*
// @ts-ignore */}
      <Text center>{simplePayError.errorMessage}</Text>
    </>
  );
}
