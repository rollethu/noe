import React from "react";

import ProgressBarSVG from "../assets/progressbar_3.svg";
import { View, Caption, Image } from "../UI";

export default function Survey() {
  return (
    <View>
      <Image src={ProgressBarSVG} />
      <Caption>Survey</Caption>
    </View>
  );
}
