import React from "react";

import PaymentFailedSVG from "../../assets/payment-failed.svg";
import { View, Caption, Image, Text, LinkButton } from "../../UI";
import { ROUTE_PAYMENT_METHODS } from "../../App";

export default function PaymentFailed() {
  return (
    <View>
      <Caption center>Sikertelen fizetés</Caption>
      <Image src={PaymentFailedSVG} />
      {/*
// @ts-ignore */}
      <Text>Hiba lépett fel a tranzakció során. Kérjük ellenőrizze hálózati kapcsolatát és próbálja újra!</Text>
      {/*
// @ts-ignore */}
      <LinkButton toCenter to={ROUTE_PAYMENT_METHODS}>
        Újrapróbálom
      </LinkButton>
    </View>
  );
}
