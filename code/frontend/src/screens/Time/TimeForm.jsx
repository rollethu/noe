import React from "react";
import { useForm } from "react-hook-form";
import { useHistory } from "react-router-dom";
import moment from "moment";

import { ROUTE_CHECKOUT } from "../../App";
import { Context as AppointmentContext } from "../../contexts/appointmentContext";
import { Form, Field, Button } from "../../UI";
import * as utils from "../../utils";

const DATETIME_FORMAT = "YYYY-MM-DD HH:mm";

export default function TimeForm() {
  const history = useHistory();
  const { register, handleSubmit, setError, errors } = useForm();
  const {
    state: { appointment },
    updateAppointment,
  } = React.useContext(AppointmentContext);

  const onSubmit = async (values) => {
    if (!appointment.url) {
      alert("No appointment to update");
      return;
    }

    values.start = moment(
      `${values.date} ${values.time}`,
      DATETIME_FORMAT
    ).toISOString();
    values.end = values.start;

    const response = await updateAppointment(appointment.url, values);
    utils.handleResponse({
      response,
      setError,
      history,
      redirectRoute: ROUTE_CHECKOUT,
    });
  };

  return (
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
      <Field
        register={register}
        name="promiseToCome"
        label="Vállalom, hogy megjelenek a kiválasztott időpontban"
        type="checkbox"
        errors={errors}
        required
      />
      <Button type="submit">Tovább</Button>
    </Form>
  );
}
