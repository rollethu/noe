import React from "react";

import ProgressBarSVG from "../../assets/progressbar_4.svg";
import { View, Caption, Text, Image } from "../../UI";
import TimeForm from "./TimeForm";

export default function Time() {
  return (
    <View>
      <Image src={ProgressBarSVG} />
      <Caption>Időpont foglalás</Caption>
      <Text>
        Válassza ki a mintavétel időpontját. A forgalmi rend fenntartása
        érdekében kérjük, hogy max. 10 perccel korábban érkezzen a helyszínre.
      </Text>
      <TimeForm />
    </View>
  );
}
