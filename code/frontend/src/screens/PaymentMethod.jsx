import React from "react";
import { useHistory } from "react-router-dom";

import ProgressBarSVG from "../assets/progressbar_5.svg";
import { ROUTE_APPOINTMENT_SUCCESS } from "../App";
import { Context as AppointmentContext } from "../contexts/appointmentContext";
import { View, Caption, Text, Button, HighlightText, Image } from "../UI";

export default function PaymentMethod() {
  const history = useHistory();
  const {
    state: { appointment },
    updateAppointment,
  } = React.useContext(AppointmentContext);

  const total = "__WRONG__ FT";

  async function onNextClick() {
    let appointmentUrl = appointment.url;
    if (process.env.NODE_ENV === "development") {
      appointmentUrl =
        "http://localhost:8000/api/appointments/54d027ec-3f32-49d8-91d1-d5a1ea2ad5c8/";
    }
    if (!appointmentUrl) {
      alert("No appointment to update");
      return;
    }

    const values = { is_registration_completed: true };
    const response = await updateAppointment(appointmentUrl, values);
    if (response.error) {
      if (!response.errors) {
        alert("Váratlan hiba történt.");
      }
    } else {
      history.push(ROUTE_APPOINTMENT_SUCCESS);
    }
  }

  return (
    <View>
      <Image src={ProgressBarSVG} />
      <Caption>Fizetési mód választás</Caption>
      <HighlightText toCenter>Fizetendő összeg: {total}</HighlightText>
      <Text>Válassza ki a kívánt fizetési módot.</Text>
      <Button toCenter inverse>
        Fizetés a helyszínen bankkártyával
      </Button>
      <Button toCenter inverse disabled>
        Hamarosan: Online fizetés
      </Button>
      <Button toCenter onClick={onNextClick}>
        Tovább
      </Button>
    </View>
  );
}
