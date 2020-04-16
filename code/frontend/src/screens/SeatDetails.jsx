import React from "react";
import { useForm } from "react-hook-form";
import { Redirect } from "react-router-dom";

import { ROUTE_ADD_SEAT } from "../App";
import {
  View,
  Caption,
  InputGroup,
  Label,
  Input,
  Form,
  Field,
  Button,
  Text,
} from "../UI";
import { Context as SeatContext } from "../contexts/seatContext";
import { Context as AppointmentContext } from "../contexts/appointmentContext";

const TXT_SUBMIT_BUTTON = "Tovább";
const TXT_HELP_TEXT =
  "Töltse ki az alábbi mezőket. Kérjük, valós adatokat adjon meg.";

export default function SeatDetails() {
  const [redirectTo, setRedirectTo] = React.useState(null);
  const { register, handleSubmit, setError, errors, watch } = useForm();
  const { createSeat } = React.useContext(SeatContext);
  const { state } = React.useContext(AppointmentContext);

  const onSubmit = async (values) => {
    let appointmentUrl = state.appointmentUrl;
    if (process.env.NODE_ENV === "development") {
      appointmentUrl =
        "http://localhost:8000/api/appointments/54d027ec-3f32-49d8-91d1-d5a1ea2ad5c8/";
    }
    if (!appointmentUrl) {
      alert("No appointment to update");
    }

    if (!values.has_doctor_referral) {
      delete values.healthcare_number;
    }
    values.appointment = appointmentUrl;

    const response = await createSeat(values);
    if (response.error) {
      if (response.errors) {
        Object.keys(response.errors).map((fieldName) => {
          setError(fieldName, "", response.errors[fieldName]);
        });
      } else {
        alert("Váratlan hiba történt.");
      }
    } else {
      setRedirectTo(ROUTE_ADD_SEAT);
    }
  };

  if (redirectTo) {
    return <Redirect to={redirectTo} />;
  }

  return (
    <View>
      <Caption>SeatDetails</Caption>
      <Text>{TXT_HELP_TEXT}</Text>
      <Form onSubmit={handleSubmit(onSubmit)}>
        <Field
          register={register}
          name="full_name"
          label="Név"
          errors={errors}
        />
        <Field
          register={register}
          name="birth_date"
          label="Születési dátum"
          type="date"
          errors={errors}
        />
        <Field
          register={register}
          name="identity_card_number"
          label="Személyi igazolvány száma"
          errors={errors}
          helpText="Személyigazolvány hiányában, jogosítvány vagy útlevél száma"
        />
        <InputGroup>
          <Label>Tartózkodási cím</Label>
          <>
            <Input register={register} name="post_code" />
            <Input register={register} name="city" />
          </>
          <>
            <Input register={register} name="address_line1" />
          </>
        </InputGroup>
        <Field
          register={register}
          name="phone_number"
          label="Értesítési telefonszám"
          type="text"
          errors={errors}
        />
        <Field
          register={register}
          name="has_doctor_referral"
          label="Beutalóval érkezem"
          type="checkbox"
          errors={errors}
        />
        <Field
          register={register}
          name="healthcare_number"
          label="TAJ kártyaszám"
          type="text"
          errors={errors}
          hidden={!watch("has_doctor_referral")}
        />
        <Button type="submit">{TXT_SUBMIT_BUTTON}</Button>
      </Form>
    </View>
  );
}
