import React from "react";

import { Context as AppointmentContext } from "../contexts/appointmentContext";
import VerificationSVG from "../assets/verification.svg";
import { View, Caption, Text, Image } from "../UI";

export default function EmailVerification() {
  const {
    state: { emailVerification },
    resendEmailVerification,
  } = React.useContext(AppointmentContext);

  function onResendClick() {
    resendEmailVerification(emailVerification.uuid);
  }

  return (
    <View>
      <Caption center>Erősítse meg adatait</Caption>
      <Image src={VerificationSVG} />
      <Text>
        A megadott e-mail címére elküldtük a megerősítő linket, amelyre
        kattintva visszatérhet a regisztrációs folyamathoz.
      </Text>
      <Text center onClick={onResendClick} semiLight>
        Nem érkezett meg a link? <strong>Újraküldöm</strong>
      </Text>
    </View>
  );
}
