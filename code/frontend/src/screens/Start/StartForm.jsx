import React from "react";
import { useForm } from "react-hook-form";
import { useHistory } from "react-router-dom";

import * as utils from "../../utils";
import { ROUTE_EMAIL_VERIFICATION } from "../../App";
import { Context as AppointmentContext } from "../../contexts/appointmentContext";
import { Form, Field, NextButton } from "../../UI";

const GTC_VERSION = "1.0";
const PRIVACY_POLICY_VERSION = "1.0";
const registrationFields = [
  {
    name: "email",
    label: "E-mail cím",
    type: "email",
    placeholder: "pelda@gmail.com",
  },
  {
    name: "gtc",
    label: "Elfogadom az ÁSZF-et.",
    type: "checkbox",
    required: true,
    value: GTC_VERSION,
  },
  {
    name: "privacy_policy",
    label: "Elfogadom az Adatvédelmi Szabályzatot.",
    type: "checkbox",
    required: true,
    value: PRIVACY_POLICY_VERSION,
  },
];

export default function StartForm() {
  const history = useHistory();
  const { register, handleSubmit, setError, errors } = useForm();
  const { createAppointment } = React.useContext(AppointmentContext);

  const onSubmit = async (values) => {
    const response = await createAppointment(values);
    utils.handleResponse({
      response,
      setError,
      history,
      redirectRoute: ROUTE_EMAIL_VERIFICATION,
    });
  };

  return (
    <Form onSubmit={handleSubmit(onSubmit)}>
      {registrationFields.map((field) => (
        <Field
          {...field}
          key={field.name}
          register={register}
          errors={errors}
        />
      ))}
      <NextButton type="submit" />
    </Form>
  );
}
