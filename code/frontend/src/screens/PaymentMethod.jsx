import React from "react";
import { Redirect } from "react-router-dom";

import { ROUTE_APPOINTMENT_SUCCESS } from "../App";
import { Context as AppointmentContext } from "../contexts/appointmentContext";
import { View, Caption, Text, Button, HighlightText } from "../UI";

export default function PaymentMethod() {
  const [redirectTo, setRedirectTo] = React.useState(null);
  const { state, updateAppointment } = React.useContext(AppointmentContext);

  const total = "__WRONG__ FT";

  async function onNextClick() {
    let appointmentUrl = state.appointmentUrl;
    if (process.env.NODE_ENV === "development") {
      appointmentUrl =
        "http://localhost:8000/api/appointments/54d027ec-3f32-49d8-91d1-d5a1ea2ad5c8/";
    }
    if (!appointmentUrl) {
      alert("No appointment to update");
    }

    const values = { is_registration_completed: true };
    const response = await updateAppointment(appointmentUrl, values);
    if (response.error) {
      if (!response.errors) {
        alert("Váratlan hiba történt.");
      }
    } else {
      setRedirectTo(ROUTE_APPOINTMENT_SUCCESS);
    }
  }

  if (redirectTo) {
    return <Redirect to={redirectTo} />;
  }

  return (
    <View>
      <Caption>Fizetési mód választás</Caption>
      <Text>Válassza ki a kívánt fizetési módot.</Text>
      <HighlightText toCenter>Fizetendő összeg: {total}</HighlightText>
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
