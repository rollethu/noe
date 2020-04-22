import React from "react";
import { View, Caption, Text, LinkButton } from "../UI";
import { ROUTE_START } from "../App";

export default function EmailVerificationFailure({ error }) {
  return (
    <View>
      <Caption
        onDoubleClick={(e) => {
          alert(JSON.stringify(error));
        }}
        center
      >
        Sikertelen megerősítés
      </Caption>
      <Text>
        A megadott e-mail címére elküldtük a megerősítő linket, amelyre
        kattintva visszatérhet a regisztrációs folyamathoz.
      </Text>
      <LinkButton to={ROUTE_START} toCenter>
        Új regisztráció
      </LinkButton>
    </View>
  );
}
