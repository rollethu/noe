import React from "react";
import { useForm } from "react-hook-form";

import { Form, Field, NextButton } from "../../UI";
import { Appointment } from "../../models";

type registrationFormProps = {
  locationOptions: any;
  onSubmit: any;
  appointment: Appointment;
};

export default function RegistrationForm({ locationOptions, onSubmit, appointment }: registrationFormProps) {
  let defaultValues = {
    location: "",
    licence_plate: "",
  };
  let isLocationDisabled = false;
  if (appointment) {
    defaultValues.location = appointment.locationUrl;
    defaultValues.licence_plate = appointment.licencePlate;
    isLocationDisabled = !!appointment.locationUrl;
  }
  const { register, handleSubmit, setError, errors, setValue } = useForm({ defaultValues });

  function onLicencePlateChange(event) {
    setValue("licence_plate", event.target.value.toUpperCase());
  }

  return (
    <Form onSubmit={handleSubmit((values) => onSubmit(values, setError))}>
      {/*
// @ts-ignore */}
      <Field
        register={register}
        name="location"
        label="Tesztelőállomás kiválasztása"
        type="select"
        errors={errors}
        options={locationOptions}
        selectOptionText="Kiválasztás"
        helpText="Kérjük figyelmesen válasszon helyszínt, később nem lehet módosítani."
        disabled={isLocationDisabled}
      />
      {/*
// @ts-ignore */}
      <Field
        register={register}
        name="licence_plate"
        label="Rendszám"
        type="text"
        errors={errors}
        onChange={onLicencePlateChange}
        placeholder="ABC-123"
      />
      {/*
// @ts-ignore */}
      <NextButton type="submit" />
    </Form>
  );
}
