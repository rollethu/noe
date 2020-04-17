import React from "react";
import { useForm } from "react-hook-form";
import { Redirect } from "react-router-dom";
import moment from "moment";

import { ROUTE_CHECKOUT } from "../App";
import { Context as AppointmentContext } from "../contexts/appointmentContext";
import { View, Caption, Form, Field, Button, Text } from "../UI";

const TXT_SUBMIT_BUTTON = "Tovább";
const DATETIME_FORMAT = "YYYY-MM-DD HH:mm";

export default function Time() {
  const [redirectTo, setRedirectTo] = React.useState(null);
  const { register, handleSubmit, setError, errors } = useForm();
  const {
    state: { appointment },
    updateAppointment,
  } = React.useContext(AppointmentContext);

  const onSubmit = async (values) => {
    let appointmentUrl = appointment.url;
    if (process.env.NODE_ENV === "development") {
      appointmentUrl =
        "http://localhost:8000/api/appointments/54d027ec-3f32-49d8-91d1-d5a1ea2ad5c8/";
    }
    if (!appointmentUrl) {
      alert("No appointment to update");
    }

    const start = moment(
      values.date + " " + values.time,
      DATETIME_FORMAT
    ).toISOString();
    values.start = start;
    values.end = start;

    const response = await updateAppointment(appointmentUrl, values);
    if (response.error) {
      if (response.errors) {
        Object.keys(response.errors).map((fieldName) => {
          setError(fieldName, "", response.errors[fieldName]);
        });
      } else {
        alert("Váratlan hiba történt.");
      }
    } else {
      setRedirectTo(ROUTE_CHECKOUT);
    }
  };

  if (redirectTo) {
    return <Redirect to={redirectTo} />;
  }

  return (
    <View>
      <Caption>Időpont foglalás</Caption>
      <Text>
        Válassza ki a mintavétel időpontját. A forgalmi rend fenntartása
        érdekében kérjük, hogy max. 10 perccel korábban érkezzen a helyszínre.
      </Text>
      <Form onSubmit={handleSubmit(onSubmit)}>
        <Field
          register={register}
          name="date"
          label="Nap kiválasztása"
          type="date"
          errors={errors}
        />
        <Field
          register={register}
          name="time"
          label="Idősáv kiválasztása"
          type="time"
          errors={errors}
        />
        <Button type="submit">{TXT_SUBMIT_BUTTON}</Button>
      </Form>
    </View>
  );
}
