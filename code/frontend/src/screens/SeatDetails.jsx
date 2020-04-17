import React from "react";
import { useForm } from "react-hook-form";
import { Redirect } from "react-router-dom";

import ProgressBarSVG from "../assets/progressbar_2.svg";
import { ROUTE_ADD_SEAT, ROUTE_CHECKOUT } from "../App";
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
  Image,
} from "../UI";
import { Context as SeatContext } from "../contexts/seatContext";
import { Context as AppointmentContext } from "../contexts/appointmentContext";

const TXT_SUBMIT_BUTTON = "Tovább";
const TXT_HELP_TEXT =
  "Töltse ki az alábbi mezőket. Kérjük, valós adatokat adjon meg.";

const SUBMIT_MODE_CREATE = "CREATE";
const SUBMIT_MODE_UPDATE = "UPDATE";

export default function SeatDetails() {
  const [redirectTo, setRedirectTo] = React.useState(null);
  const {
    state: { activeSeat },
    createSeat,
    updateSeat,
  } = React.useContext(SeatContext);
  const {
    state: { appointment },
  } = React.useContext(AppointmentContext);
  let appointmentUrl = appointment.url;
  if (process.env.NODE_ENV === "development") {
    appointmentUrl =
      "http://localhost:8000/api/appointments/54d027ec-3f32-49d8-91d1-d5a1ea2ad5c8/";
  }

  const submitMode =
    activeSeat === null ? SUBMIT_MODE_CREATE : SUBMIT_MODE_UPDATE;

  const onCreateSubmit = async (values) => {
    if (!appointment.url) {
      alert("No appointment to update");
    }

    if (!values.has_doctor_referral) {
      delete values.healthcare_number;
    }
    values.appointment = appointment.url;

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

  const onUpdateSubmit = async (values) => {
    if (!values.has_doctor_referral) {
      delete values.healthcare_number;
    }

    const response = await updateSeat(activeSeat.url, values);
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

  let defaultValues;
  let onSubmit;
  if (submitMode === SUBMIT_MODE_CREATE) {
    onSubmit = onCreateSubmit;
    defaultValues = {
      email: appointment.email,
    };
  } else {
    onSubmit = onUpdateSubmit;
    defaultValues = activeSeat;
  }

  const { register, handleSubmit, setError, errors, watch } = useForm({
    defaultValues,
  });

  if (redirectTo) {
    return <Redirect to={redirectTo} />;
  }

  return (
    <View>
      <Image src={ProgressBarSVG} />
      <Caption>Személyes adatok</Caption>
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
          name="email"
          label="Értesítési e-mail cím"
          type="email"
          errors={errors}
          helpText="Amennyiben értesítési e-mail címe eltér a megadottól "
        />
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
