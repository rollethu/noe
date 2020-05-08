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
  Text,
} from "../../UI";

const defaultValues = {
  country: "Magyarország",
};

export default function BillingDetailsForm({ onSubmit, seat }) {
  const [wasResetted, setWasResetted] = React.useState(false);
  const { register, handleSubmit, setError, errors, setValue, reset } = useForm(
    {
      defaultValues,
    }
  );
  const managedSubmit = handleSubmit((values) => onSubmit(values, setError));

  React.useEffect(() => {
    if (!!seat) {
      prefillForm(seat);
    }
  }, [seat?.url]);

  function prefillForm(seat) {
    setValue("company_name", seat?.full_name);
    setValue("country", seat?.country);
    setValue("post_code", seat?.post_code);
    setValue("city", seat?.city);
    setValue("address_line1", seat?.address_line1);
    setValue("tax_number", seat?.tax_number);
  }

  function onIsCompanyChange(value) {
    if (value && !wasResetted) {
      reset({ ...defaultValues, isCompany: true }); // Prevent resetting checkbox too
      setWasResetted(true);
    }
  }

  return (
    <Form onSubmit={managedSubmit}>
      <Field
        type="checkbox"
        name="isCompany"
        register={register}
        label="Cég számára szeretnék áfás számlát igényelni."
        onChange={onIsCompanyChange}
      />
      <Text dark style={{ alignSelf: "flex-start" }}>
        Kérjük adja meg számlázási adatait.
      </Text>
      <Field
        register={register}
        name="company_name"
        label="Név vagy cégnév"
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
      <Text small style={{ alignSelf: "flex-start" }}>
        * Helyszíni fizetés esetén a számla a tranzakció után kerül kiállításra.
      </Text>
      <NextButton type="submit">Véglegesítés</NextButton>
    </Form>
  );
}
