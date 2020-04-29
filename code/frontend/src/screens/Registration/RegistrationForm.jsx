import React from "react";
import { useForm } from "react-hook-form";
import { useHistory } from "react-router-dom";

import { Context as AppointmentContext } from "../../contexts/appointmentContext";
import { ROUTE_SEAT_DETAILS } from "../../App";
import { Form, Field, NextButton } from "../../UI";
import * as utils from "../../utils";

export default function RegistrationForm({ locationOptions }) {
  const history = useHistory();
  const {
    state: { appointment },
    updateAppointment,
  } = React.useContext(AppointmentContext);
  const { register, handleSubmit, setError, errors, setValue } = useForm();

  function onLicencePlateChange(event) {
    setValue("licence_plate", event.target.value.toUpperCase());
  }

  const onSubmit = async (values) => {
    if (!appointment.url) {
      alert("No appointment to update");
      return;
    }

    const response = await updateAppointment(appointment.url, values);
    utils.handleResponse({
      response,
      setError,
      history,
      redirectRoute: ROUTE_SEAT_DETAILS,
    });
  };

  return (
    <Form onSubmit={handleSubmit(onSubmit)}>
      <Field
        register={register}
        name="location"
        label="Tesztelőállomás kiválasztása"
        type="select"
        errors={errors}
        options={locationOptions}
        selectOptionText="Kiválasztás"
      />
      <Field
        register={register}
        name="licence_plate"
        label="Rendszám"
        type="text"
        errors={errors}
        onChange={onLicencePlateChange}
        placeholder="ABC-123"
        helpText="Kérjük figyelmesen töltse ki ezeket az adatokat, a későbbekben nem tudja módosítani."
      />
      <NextButton type="submit" />
    </Form>
  );
}
