import React from "react";
import { useForm } from "react-hook-form";
import { useHistory } from "react-router-dom";

import * as utils from "../../utils";
import { ROUTE_SURVEY as redirectRoute } from "../../App";
import { InputGroup, Label, Input, Form, Field, Button, Flex } from "../../UI";
import { Context as SeatContext } from "../../contexts/seatContext";
import { Context as AppointmentContext } from "../../contexts/appointmentContext";

const SUBMIT_MODE_CREATE = "CREATE";
const SUBMIT_MODE_UPDATE = "UPDATE";

export default function SeatDetailsForm() {
  const history = useHistory();
  const {
    state: { activeSeat },
    createSeat,
    updateSeat,
  } = React.useContext(SeatContext);
  const {
    state: { appointment },
  } = React.useContext(AppointmentContext);
  const submitMode =
    activeSeat === null ? SUBMIT_MODE_CREATE : SUBMIT_MODE_UPDATE;
  const { register, handleSubmit, setError, errors, watch } = useForm({
    defaultValues:
      submitMode === SUBMIT_MODE_CREATE
        ? { email: appointment.email }
        : activeSeat,
  });

  const onSubmit = (values) => {
    if (!appointment.url) {
      alert("No appointment to update");
      return;
    }

    if (!values.has_doctor_referral) {
      delete values.healthcare_number;
    }

    if (submitMode === SUBMIT_MODE_CREATE) {
      onCreateSubmit(values);
    } else {
      onUpdateSubmit(values);
    }
  };

  const onCreateSubmit = async (values) => {
    values.appointment = appointment.url;

    const response = await createSeat(values);
    utils.handleResponse({
      response,
      setError,
      history,
      redirectRoute,
    });
  };

  const onUpdateSubmit = async (values) => {
    if (!values.has_doctor_referral) {
      delete values.healthcare_number;
    }

    const response = await updateSeat(activeSeat.url, values);
    utils.handleResponse({
      response,
      setError,
      history,
      redirectRoute,
    });
  };

  return (
    <Form onSubmit={handleSubmit(onSubmit)}>
      <Field
        register={register}
        name="full_name"
        label="Név"
        errors={errors}
        placeholder="Példa Péter"
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
        placeholder="123456AB"
      />
      <InputGroup>
        <Label>Tartózkodási cím</Label>
        <InputGroup>
          <Flex>
            <Input
              style={{ flex: 2 }}
              register={register}
              name="post_code"
              placeholder="Irányítósz."
            />
            <Input
              style={{ flex: 5, marginLeft: 10 }}
              register={register}
              name="city"
              placeholder="Település"
            />
          </Flex>
        </InputGroup>
        <Input
          register={register}
          name="address_line1"
          placeholder="Utca és Házszám"
        />
      </InputGroup>
      <Field
        register={register}
        name="phone_number"
        label="Értesítési telefonszám"
        type="text"
        errors={errors}
        placeholder="+36 70 123 4567"
      />
      <Field
        register={register}
        name="email"
        label="Értesítési e-mail cím"
        type="email"
        errors={errors}
        helpText="Amennyiben értesítési e-mail címe eltér a megadottól "
        placeholder="pelda@gmail.com"
      />
      <Field
        register={register}
        name="has_doctor_referral"
        label="Orvosi beutalóval érkezem"
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
        placeholder="123-456-789"
      />
      <Button type="submit">Tovább</Button>
    </Form>
  );
}
