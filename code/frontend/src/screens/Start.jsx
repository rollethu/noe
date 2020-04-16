import React from "react";

import { View, Caption } from "../UI";

const TXT_CAPTION_TEXT = "Áthajtásos koronavírus (COVID-19) teszt";

export default function Start() {
  return (
    <View>
      <Caption center>{TXT_CAPTION_TEXT}</Caption>
    </View>
  );
}
