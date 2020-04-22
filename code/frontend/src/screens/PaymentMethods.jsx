import React from "react";
import { useHistory } from "react-router-dom";
import axios from "axios";

import * as consts from "../contexts/consts";
import ProgressBarSVG from "../assets/progressbar_5.svg";
import { ROUTE_APPOINTMENT_SUCCESS } from "../App";
import { Context as AppointmentContext } from "../contexts/appointmentContext";
import {
  View,
  Caption,
  Text,
  Button,
  HighlightText,
  Image,
  NextButton,
} from "../UI";

export default function PaymentMethods() {
  const history = useHistory();
  const {
    state: { appointment },
    updateAppointment,
    fetchPrice,
  } = React.useContext(AppointmentContext);

  React.useEffect(() => {
    fetchPrice({
      appointment: appointment.url,
      payment_method_type: "ON_SITE",
    });
  }, [appointment?.total_price]);

  let total = "Ár nem elérhető!";
  if (
    appointment.total_price !== undefined &&
    appointment.currency !== undefined
  ) {
    const currency =
      appointment.currency === "HUF" ? "Ft" : appointment.currency;
    total = `${appointment.total_price} ${currency}`;
  }

  async function onNextClick() {
    if (!appointment.url) {
      alert("No appointment to update");
      return;
    }

    // Updates Appointment's all Seats's Payments's payment_method_type
    const requestData = {
      appointment: appointment.url,
      payment_method_type: "ON_SITE",
      total_price: appointment.total_price,
      currency: appointment.currency,
    };
    // We don't do anything if this request fails
    // This must change in the future
    await axios.post(consts.PAY_APPOINTMENT_URL, requestData);

    const values = { is_registration_completed: true };
    const response = await updateAppointment(appointment.url, values);
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
      <NextButton toCenter onClick={onNextClick} />
    </View>
  );
}
