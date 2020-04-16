import React from "react";

import { View, Caption, Text, Image, Button } from "../UI";

export default function AppointmentSuccess() {
  return (
    <View>
      <Caption center>Sikeres Regisztráció</Caption>
      <Image src="https://via.placeholder.com/150" />
      <Text>
        Időpontfoglalása rögzítésre került. A regisztráció részleteit és további
        információt a megadott e-mail címre küldött üzenetben talál. Kérjük
        időben érkezzen a csúszások elkerülése végett.
      </Text>
      <Button toCenter>Rendben</Button>
    </View>
  );
}
