import React from "react";

import StartForm from "./StartForm";
import StartSVG from "../../assets/main.svg";
import { View, Caption, Image, Pill } from "../../UI";

export default function Start() {
  return (
    <View>
      <Caption center>Áthajtásos koronavírus (COVID-19) teszt</Caption>
      <Image src={StartSVG} />
      <Pill
        text="Tájékoztató a tesztelésről"
        info
        to="https://tesztallomas.hu"
      />
      <StartForm />
    </View>
  );
}
