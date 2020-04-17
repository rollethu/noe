import React from "react";

import { Context as AppointmentContext } from "../contexts/appointmentContext";
import VerificationSVG from "../assets/verification.svg";
import { View, Caption, Text, Image } from "../UI";

const TXT_CAPTION = "Erősítse meg adatait";
const TXT_DESCRIPTION =
  "A megadott e-mail címére elüldtük a megerősítő linket, amelyre kattintva visszatérhet a regisztrációs folyamathoz.";

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
      <Caption center>{TXT_CAPTION}</Caption>
      <Image src={VerificationSVG} />
      <Text>{TXT_DESCRIPTION}</Text>
      <Text center onClick={onResendClick}>
        Nem érkezett meg a link? <strong>Újraküldöm</strong>
      </Text>
    </View>
  );
}
