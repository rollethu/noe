import React from "react";
import { useForm } from "react-hook-form";
import { Redirect } from "react-router-dom";

import { ROUTE_EMAIL_VERIFICATION } from "../App";
import { Context as AppointmentContext } from "../contexts/appointmentContext";
import { View, Caption, Form, Field, Button } from "../UI";

const GTC_VERSION = "1.0";
const PRIVACY_POLICY_VERSION = "1.0";
const TXT_CAPTION = "Áthajtásos koronavírus (COVID-19) teszt";
const TXT_SUBMIT_BUTTON = "Tovább";
const TXT_ACCEPT_GTC = "Elfogadom az ÁSZF-et.";
const TXT_ACCEPT_PRIVACY_POLICY = "Elfogadom az Adatvédelmi Szabályzatot.";

export default function Start(props) {
  const [redirectTo, setRedirectTo] = React.useState(null);
  const { register, handleSubmit, setError, errors } = useForm();
  const { createAppointment } = React.useContext(AppointmentContext);

  const onSubmit = async (values) => {
    const response = await createAppointment(values);
    if (response.error) {
      if (response.errors) {
        Object.keys(response.errors).map((fieldName) => {
          setError(fieldName, "", response.errors[fieldName]);
        });
      } else {
        alert("Váratlan hiba történt.");
      }
    } else {
      setRedirectTo(ROUTE_EMAIL_VERIFICATION);
    }
  };

  if (redirectTo) {
    return <Redirect to={redirectTo} />;
  }

  return (
    <View>
      <Caption center>{TXT_CAPTION}</Caption>
      <Form onSubmit={handleSubmit(onSubmit)}>
        <Field
          register={register}
          name="email"
          label="E-mail"
          type="text"
          errors={errors}
        />
        <Field
          register={register}
          name="gtc"
          label={TXT_ACCEPT_GTC}
          type="checkbox"
          value={GTC_VERSION}
          errors={errors}
        />
        <Field
          register={register}
          name="privacy_policy"
          label={TXT_ACCEPT_PRIVACY_POLICY}
          type="checkbox"
          value={PRIVACY_POLICY_VERSION}
          errors={errors}
        />
        <Button type="submit">{TXT_SUBMIT_BUTTON}</Button>
      </Form>
    </View>
  );
}
