import React from "react";
import { useForm } from "react-hook-form";

import { Form, Field, NextButton } from "../../UI";

export default function RegistrationForm({ locationOptions, onSubmit }) {
  const { register, handleSubmit, setError, errors, setValue } = useForm();

  function onLicencePlateChange(event) {
    setValue("licence_plate", event.target.value.toUpperCase());
  }

  return (
    <Form onSubmit={handleSubmit((values) => onSubmit(values, setError))}>
      <Field
        register={register}
        name="location"
        label="Tesztelőállomás kiválasztása"
        type="select"
        errors={errors}
        options={locationOptions}
        selectOptionText="Kiválasztás"
        helpText="Kérjük figyelmesen válasszon helyszínt, később nem lehet módosítani."
      />
      <Field
        register={register}
        name="licence_plate"
        label="Rendszám"
        type="text"
        errors={errors}
        onChange={onLicencePlateChange}
        placeholder="ABC-123"
      />
      <NextButton type="submit" />
    </Form>
  );
}
