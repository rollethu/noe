import React from "react";
import { useHistory } from "react-router-dom";
import axios from "axios";
import { useForm } from "react-hook-form";

import * as consts from "../../contexts/consts";
import * as paymentUtils from "./utils";
import * as utils from "../../utils";
import ProgressBarSVG from "../../assets/progressbar_5.svg";
import { ROUTE_APPOINTMENT_SUCCESS } from "../../App";
import { Context as AppointmentContext } from "../../contexts/appointmentContext";
import { Context as SeatContext } from "../../contexts/seatContext";
import { View, Caption, Text, Button, HighlightText, Image, NextButton, Form, Field } from "../../UI";
import BillingDetailsForm from "./BillingDetailsForm";
import { useFeatureSimplePay } from "../../featureFlags";

export const CREDIT_CARD_ON_SITE = "CREDIT_CARD_ON_SITE";
export const CREDIT_CARD_ONLINE = "CREDIT_CARD_ONLINE";
export const paymentMethodOptions = [
  { text: "Online Fizetés", value: CREDIT_CARD_ONLINE },
  { text: "Fizetés a helyszínen bankkártyával", value: CREDIT_CARD_ON_SITE },
];

// Ordering matters. First is the default value.
const products = [
  { id: "NORMAL_EXAM", text: "Normál vizsgálat", isActive: true, price: 26990 },
  {
    id: "PRIORITY_EXAM",
    text: "Elsőbbségi vizsgálat",
    isActive: true,
    price: 36990,
  },
  // {
  //   id: "PRIORITY_EXAM_FRADI",
  //   text: "Elsőbbségi vizsgálat Fradi Szurkólói Kártya kedvezménnyel",
  //   isActive: true,
  //   price: 33500,
  // },
];
const productOptions = products.map((p) => ({
  value: p.id,
  text: `${p.text} (${p.price} Ft/db)`,
}));

export default function PaymentMethods() {
  const history = useHistory();
  const {
    state: { appointment, productID: selectedProductID },
    updateAppointment,
    fetchPrice,
    setProduct,
  } = React.useContext(AppointmentContext);
  const [selectedPaymentMethod, setSelectedPaymentMethod] = React.useState(CREDIT_CARD_ONLINE);
  const { state } = React.useContext(SeatContext);
  const firstSeat = state.seats[0] || null;
  const defaultValues = {
    product_type: selectedProductID || products[0].id,
    payment_method: CREDIT_CARD_ONLINE,
  };
  const { register } = useForm({
    defaultValues,
  });

  React.useEffect(() => {
    if (selectedProductID === null) {
      setProduct(products[0].id);
    }

    fetchPrice({
      appointment: appointment.url,
      product_type: selectedProductID || products[0].id,
    });
  }, []);

  async function onNextClick(billingDetailsValues, setError) {
    if (!appointment.url) {
      alert("No appointment to update");
      return;
    }

    handleOnSitePayment(billingDetailsValues, setError);
  }

  async function handleOnSitePayment(billingDetailsValues, setError) {
    const response = await axios.post(
      consts.PAY_APPOINTMENT_URL,
      paymentUtils.makePaymentUpdateRequest(appointment, selectedProductID, billingDetailsValues)
    );
    if (response.error) {
      if (!response.errors) {
        alert("Váratlan hiba történt.");
      } else {
        alert("A regisztrációt nem sikerült véglegesíteni.");
        console.log(response.errors);

        utils.setErrors(setError, response.errors);
      }
    } else {
      history.push(ROUTE_APPOINTMENT_SUCCESS);
    }
  }

  function onProductSelect(productID) {
    setProduct(productID);
    fetchPrice({ appointment: appointment.url, product_type: productID });
  }

  function onPaymentMethodChange(newPaymentMethod) {
    setSelectedPaymentMethod(newPaymentMethod);
  }

  return (
    <View>
      <Image src={ProgressBarSVG} />
      <Caption>Fizetési mód választás</Caption>
      <HighlightText toCenter>Fizetendő összeg: {paymentUtils.getTotalPriceDisplay(appointment)}</HighlightText>
      <Text>Válassza ki a kívánt fizetési módot.</Text>
      <Field
        type="select"
        options={productOptions}
        onChange={(newValue) => onProductSelect(newValue)}
        register={register}
        name="product_type"
      />
      {useFeatureSimplePay && (
        <Field
          type="select"
          options={paymentMethodOptions}
          onChange={(newValue) => onPaymentMethodChange(newValue)}
          register={register}
          name="payment_method"
        />
      )}
      <BillingDetailsForm onSubmit={onNextClick} seat={firstSeat} />
    </View>
  );
}
