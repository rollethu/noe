import React from "react";
import { useForm } from "react-hook-form";
import moment from "moment";

import { Form, Field, NextButton } from "../../UI";
import * as timeUtils from "./utils";

export default function TimeForm({ onSubmit, onDateChange, timeSlots }) {
  const { register, handleSubmit, setError, errors } = useForm();
  const timeSlotOptions = timeUtils.getTimeSlotOptions(timeSlots);

  return (
    <Form onSubmit={handleSubmit((values) => onSubmit(values, setError))}>
      <Field
        register={register}
        name="date"
        label="Nap kiválasztása"
        type="date"
        min={moment().format("YYYY-MM-DD")}
        defaultValue={moment().format("YYYY-MM-DD")}
        errors={errors}
        onChange={(event) => onDateChange(event.target.value)}
      />
      <Field
        register={register}
        name="time_slot"
        label="Idősáv kiválasztása"
        type="select"
        errors={errors}
        options={timeSlotOptions}
      />
      <Field
        register={register}
        name="promiseToCome"
        label="Vállalom, hogy megjelenek a kiválasztott időpontban"
        type="checkbox"
        errors={errors}
        required
      />
      <NextButton type="submit" />
    </Form>
  );
}
