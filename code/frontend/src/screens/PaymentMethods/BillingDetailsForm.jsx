import React from "react";
import { useForm } from "react-hook-form";
import {
  Form,
  Field,
  InputGroup,
  Label,
  Flex,
  Input,
  HelpBlock,
  NextButton,
} from "../../UI";

export default function BillingDetailsForm({ onSubmit }) {
  const { register, handleSubmit, setError, errors } = useForm();
  const managedSubmit = handleSubmit((values) => onSubmit(values, setError));

  return (
    <Form onSubmit={managedSubmit}>
      <Field
        register={register}
        name="company_name"
        label="Név"
        placeholder="Példa Kft."
        errors={errors}
        required
      />
      <Field
        register={register}
        name="country"
        label="Ország"
        placeholder="Magyarország"
        errors={errors}
        required
      />
      <InputGroup
        hasError={errors.post_code || errors.city || errors.address_line1}
      >
        <Label>Tartózkodási cím</Label>
        <InputGroup>
          <Flex>
            <div style={{ flex: 2 }}>
              <Input
                register={register}
                name="post_code"
                placeholder="Irányítósz."
                required
              />
              {errors.post_code && (
                <HelpBlock>
                  {errors.post_code.type === "required"
                    ? "Ez a mező kötelező."
                    : errors.post_code.message}
                </HelpBlock>
              )}
            </div>
            <div style={{ flex: 5, marginLeft: 10 }}>
              <Input
                register={register}
                name="city"
                placeholder="Település"
                required
              />
              {errors.city && (
                <HelpBlock>
                  {errors.city.type === "required"
                    ? "Ez a mező kötelező."
                    : errors.city.message}
                </HelpBlock>
              )}
            </div>
          </Flex>
        </InputGroup>
        <Input
          register={register}
          name="address_line1"
          placeholder="Utca és Házszám"
          required
        />
        {errors.address_line1 && (
          <HelpBlock>
            {errors.address_line1.type === "required"
              ? "Ez a mező kötelező."
              : errors.address_line1.message}
          </HelpBlock>
        )}
      </InputGroup>
      <Field
        register={register}
        name="tax_number"
        label="Adószám"
        placeholder="123456789"
        errors={errors}
      />
      <NextButton type="submit">Véglegesítés</NextButton>
    </Form>
  );
}
