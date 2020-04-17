import React from "react";

import { View, Caption, Text, Image } from "../UI";

const TXT_CAPTION = "Erősítse meg adatait";
const TXT_DESCRIPTION =
  "A megadott e-mail címére elüldtük a megerősítő linket, amelyre kattintva visszatérhet a regisztrációs folyamathoz.";

export default function EmailVerification() {
  return (
    <View>
      <Caption center>{TXT_CAPTION}</Caption>
      <Image src="https://via.placeholder.com/150" />
      <Text>{TXT_DESCRIPTION}</Text>
      <Text center>
        Nem érkezett meg a link? <strong>Újraküldöm</strong>
      </Text>
    </View>
  );
}
