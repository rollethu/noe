import React from "react";
import { useForm } from "react-hook-form";
import { useHistory } from "react-router-dom";

import { Context as AppointmentContext } from "../../contexts/appointmentContext";
import { ROUTE_SEAT_DETAILS } from "../../App";
import { Form, Field, Button } from "../../UI";
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

    values.normalized_licence_plate = utils.normalizeLicencePlate(
      values.licence_plate
    );

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
        label="Helyszín"
        type="select"
        errors={errors}
        options={locationOptions}
      />
      <Field
        register={register}
        name="licence_plate"
        label="Rendszám"
        type="text"
        errors={errors}
        onChange={onLicencePlateChange}
      />
      <Button type="submit">Tovább</Button>
    </Form>
  );
}
