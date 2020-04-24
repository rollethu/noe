import React from "react";
import { useForm } from "react-hook-form";
import * as surveyUtils from "./utils";

import { Form, Field, NextButton, Toggle, InputGroup, Label } from "../../UI";

const toggleOptions = [
  { value: "yes", text: "Igen" },
  { value: "no", text: "Nem" },
];

export default function SurveyForm({
  submitMode,
  surveyQuestions,
  surveyAnswersForActiveSeat,
  onSubmit,
}) {
  const formData = surveyUtils.getFormData(
    submitMode,
    surveyQuestions,
    surveyAnswersForActiveSeat
  );
  const { register, handleSubmit, errors, setError } = useForm();

  return (
    <Form onSubmit={handleSubmit((values) => onSubmit(values, setError))}>
      {formData.map((field) => {
        // May be a question (create) or an answer (update)
        if (field.type === "survey-toggle") {
          return (
            <InputGroup key={field.name}>
              <Label>{field.label}</Label>
              <Toggle
                register={register}
                options={toggleOptions}
                name={field.name} // question url for creation, answer url for update
                defaultValue={field.defaultValue}
              />
            </InputGroup>
          );
        }
        return (
          <Field
            key={field.name}
            register={register}
            label={field.label}
            errors={errors}
            name={field.name} // question url for creation, answer url for update
            type={field.type}
            defaultValue={field.defaultValue}
          />
        );
      })}
      <NextButton type="submit" />
    </Form>
  );
}
