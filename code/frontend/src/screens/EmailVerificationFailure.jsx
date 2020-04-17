import React from "react";
import { View, Caption, Text } from "../UI";

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
        A megadott e-mail címére elüldtük a megerősítő linket, amelyre kattintva
        visszatérhet a regisztrációs folyamathoz.
      </Text>
      <Text center>
        Nem érkezett meg a link? <strong>Újraküldöm</strong>
      </Text>
    </View>
  );
}
