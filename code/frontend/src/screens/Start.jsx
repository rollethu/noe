import React from "react";
import { useForm } from "react-hook-form";

import { Context as AppointmentContext } from "../contexts/appointmentContext";
import { View, Caption, Form, Field, Button } from "../UI";

const GTC_VERSION = "1.0";
const PRIVACY_POLICY_VERSION = "1.0";
const TXT_CAPTION = "Áthajtásos koronavírus (COVID-19) teszt";
const TXT_SUBMIT_BUTTON = "Tovább";
const TXT_ACCEPT_GTC = "Elfogadom az ÁSZF-et.";
const TXT_ACCEPT_PRIVACY_POLICY = "Elfogadom az Adatvédelmi Szabályzatot.";

export default function Start() {
  const { register, handleSubmit } = useForm();
  const { createAppointment } = React.useContext(AppointmentContext);
  const onSubmit = (values) => {
    createAppointment(values);
  };

  return (
    <View>
      <Caption center>{TXT_CAPTION}</Caption>
      <Form onSubmit={handleSubmit(onSubmit)}>
        <Field register={register} name="email" label="E-mail" type="text" />
        <Field
          register={register}
          name="gtc"
          label={TXT_ACCEPT_GTC}
          type="checkbox"
          value={GTC_VERSION}
        />
        <Field
          register={register}
          name="privacy_policy"
          label={TXT_ACCEPT_PRIVACY_POLICY}
          type="checkbox"
          value={PRIVACY_POLICY_VERSION}
        />
        <Button type="submit">{TXT_SUBMIT_BUTTON}</Button>
      </Form>
    </View>
  );
}
