import React from "react";
import { View, Caption, Text, NextLinkButton } from "../UI";
import { ROUTE_REGISTRATION } from "../App";

export default function EmailVerificationSuccess() {
  return (
    <View>
      <Caption center>Sikeres megerősítés</Caption>
      <Text>
        Sikeres e-mail megerősítés. A Tovább gombra kattintva folytathatja a
        regisztrációt.
      </Text>
      <NextLinkButton to={ROUTE_REGISTRATION} toCenter />
    </View>
  );
}
