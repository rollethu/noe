import React from "react";

import { Context as AppointmentContext } from "../contexts/appointmentContext";
import VerificationSVG from "../assets/verification.svg";
import { View, Caption, Text, Image } from "../UI";

export default function EmailVerification() {
  const [resendSuccess, setResendSuccess] = React.useState(null);
  const {
    state: { emailVerification },
    resendEmailVerification,
  } = React.useContext(AppointmentContext);

  async function onResendClick() {
    const response = await resendEmailVerification(emailVerification.uuid);
    if (!response.error) {
      setResendSuccess(true);
    }
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
      {resendSuccess && (
        <Text>
          E-mail újraküldése sikeres. Amennyiben nem találja perceken belül
          levelét, nézze meg a "Spam/Levélszemét" mappában is. Ha nem érkezett
          meg az üzenet, kérjük írjon nekünk a info@tesztallomas.hu e-mail
          címre.
        </Text>
      )}
    </View>
  );
}
