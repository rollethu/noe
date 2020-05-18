import React from "react";

import AppointmentSuccessSVG from "../../assets/success.svg";
import { View, Caption, Text, Image } from "../../UI";
import { Context as AppointmentContext } from "../../contexts/appointmentContext";
import { Context as SeatContext } from "../../contexts/seatContext";
import { Context as SurveyContext } from "../../contexts/surveyContext";

export default function AppointmentSuccess() {
  const { resetState: resetAppointmentState } = React.useContext(AppointmentContext);
  const { resetState: resetSeatState } = React.useContext(SeatContext);
  const { resetState: resetSurveyState } = React.useContext(SurveyContext);

  React.useEffect(() => {
    resetAppointmentState();
    resetSeatState();
    resetSurveyState();
  }, []);

  return (
    <View>
      <Caption center>Sikeres regisztráció</Caption>
      <Image src={AppointmentSuccessSVG} />
      <Text>
        Időpontfoglalása rögzítésre került. A regisztráció részleteit és további információt a megadott e-mail címre
        küldött üzenetben talál. Kérjük időben érkezzen a csúszások elkerülése végett.
      </Text>
      <a href="https://tesztallomas.hu" target="_blank" className="Button ToCenter" rel="noopener noreferrer">
        Rendben
      </a>
    </View>
  );
}
