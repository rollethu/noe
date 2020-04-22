import React from "react";

import AppointmentSuccessSVG from "../assets/success.svg";
import { View, Caption, Text, Image, Button } from "../UI";

export default function AppointmentSuccess() {
  return (
    <View>
      <Caption center>Sikeres regisztráció</Caption>
      <Image src={AppointmentSuccessSVG} />
      <Text>
        Időpontfoglalása rögzítésre került. A regisztráció részleteit és további
        információt a megadott e-mail címre küldött üzenetben talál. Kérjük
        időben érkezzen a csúszások elkerülése végett.
      </Text>
      <a
        href="https://tesztallomas.hu"
        target="_blank"
        className="Button ToCenter"
      >
        Rendben
      </a>
    </View>
  );
}
