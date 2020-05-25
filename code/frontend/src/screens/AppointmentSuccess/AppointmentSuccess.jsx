import React from "react";
import { useLocation } from "react-router-dom";

import AppointmentSuccessSVG from "../../assets/success.svg";
import { View, Caption, Text, Image } from "../../UI";
import { Context as AppointmentContext } from "../../contexts/appointmentContext";
import { Context as SeatContext } from "../../contexts/seatContext";
import { Context as SurveyContext } from "../../contexts/surveyContext";

export default function AppointmentSuccess() {
  const location = useLocation();
  const simplePayTransactionId = location?.state?.simplePayTransactionId;
  const { resetState: resetAppointmentState } = React.useContext(AppointmentContext);
  const { resetState: resetSeatState } = React.useContext(SeatContext);
  const { resetState: resetSurveyState } = React.useContext(SurveyContext);

  React.useEffect(() => {
    resetAppointmentState();
    resetSeatState();
    resetSurveyState();
  }, []);

  let captionText = "Sikeres regisztráció";
  let firstText = "Időpontfoglalása rögzítésre került.";
  if (simplePayTransactionId) {
    captionText = "Sikeres tranzakció";
    firstText = `SimplePay tranzakció azonosító: ${simplePayTransactionId}`;
  }

  return (
    <View>
      <Caption center>{captionText}</Caption>
      <Image src={AppointmentSuccessSVG} />
      <Text>
        {firstText}
        <br />A regisztráció részleteit és további információt a megadott e-mail címre küldött üzenetben talál. Kérjük
        időben érkezzen a csúszások elkerülése végett.
      </Text>
      <a href="https://tesztallomas.hu" target="_blank" className="Button ToCenter" rel="noopener noreferrer">
        Rendben
      </a>
    </View>
  );
}
