import React from "react";

import SeatDetailsForm from "./SeatDetailsForm";
import ProgressBarSVG from "../../assets/progressbar_2.svg";
import { View, Caption, Image, Text } from "../../UI";

export default function SeatDetails() {
  return (
    <View>
      <Image src={ProgressBarSVG} />
      <Caption>Személyes adatok</Caption>
      <Text>
        Töltse ki az alábbi mezőket. Kérjük, valós adatokat adjon meg.
      </Text>
      <SeatDetailsForm />
    </View>
  );
}
