import React from "react";
import { useForm } from "react-hook-form";

import { View, Caption, Form, Field, Button } from "../UI";

const TXT_CAPTION = "Áthajtásos koronavírus (COVID-19) teszt";
const TXT_SUBMIT_BUTTON = "Tovább";
const TXT_ACCEPT_GTC = "Elfogadom az ÁSZF-et.";
const TXT_ACCEPT_PRIVACY_POLICY = "Elfogadom az Adatvédelmi Szabályzatot.";

export default function Start() {
  const { register, handleSubmit } = useForm();
  const onSubmit = (data) => {
    console.log(data);
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
        />
        <Field
          register={register}
          name="privacy_policy"
          label={TXT_ACCEPT_PRIVACY_POLICY}
          type="checkbox"
        />
        <Button type="submit">{TXT_SUBMIT_BUTTON}</Button>
      </Form>
    </View>
  );
}
