import React from "react";
import { useHistory } from "react-router-dom";
import axios from "axios";
import { useForm } from "react-hook-form";

import * as consts from "../../contexts/consts";
import * as paymentUtils from "./utils";
import ProgressBarSVG from "../../assets/progressbar_5.svg";
import { ROUTE_APPOINTMENT_SUCCESS } from "../../App";
import { Context as AppointmentContext } from "../../contexts/appointmentContext";
import {
  View,
  Caption,
  Text,
  Button,
  HighlightText,
  Image,
  NextButton,
  Form,
  Field,
} from "../../UI";

// Ordering matters. First is the default value.
const products = [
  { id: "NORMAL_EXAM", text: "Normál vizsgálat", isActive: true },
  { id: "PRIORITY_EXAM", text: "Elsőbbségi vizsgálat", isActive: true },
  {
    id: "PRIORITY_EXAM_FRADI",
    text: "Elsőbbségi vizsgálat Fradi Szurkólói Kártya kedvezménnyel",
    isActive: true,
  },
];
const productOptions = products.map((p) => ({ value: p.id, text: p.text }));

export default function PaymentMethods() {
  const history = useHistory();
  const {
    state: { appointment, productID: selectedProductID },
    updateAppointment,
    fetchPrice,
    setProduct,
  } = React.useContext(AppointmentContext);
  const defaultValues = { product: selectedProductID || products[0].id };
  const { register } = useForm({
    defaultValues,
  });

  React.useEffect(() => {
    if (selectedProductID !== null) {
      setProduct(products[0].id);
    }

    fetchPrice({
      appointment: appointment.url,
      product: selectedProductID || products[0].id,
    });
  }, []);

  async function onNextClick() {
    if (!appointment.url) {
      alert("No appointment to update");
      return;
    }

    // Updates Appointment's all Seats's Payments's payment_method_type
    // We don't do anything if this request fails
    // This must change in the future
    await axios.post(
      consts.PAY_APPOINTMENT_URL,
      paymentUtils.makePaymentUpdateRequest(appointment)
    );

    const response = await updateAppointment(appointment.url, {
      is_registration_completed: true,
    });
    if (response.error) {
      if (!response.errors) {
        alert("Váratlan hiba történt.");
      }
    } else {
      history.push(ROUTE_APPOINTMENT_SUCCESS);
    }
  }

  function onProductSelect(productID) {
    setProduct(productID);
    fetchPrice({ appointment: appointment.url, product: productID });
  }

  return (
    <View>
      <Image src={ProgressBarSVG} />
      <Caption>Fizetési mód választás</Caption>
      <HighlightText toCenter>
        Fizetendő összeg: {paymentUtils.getTotalPriceDisplay(appointment)}
      </HighlightText>
      <Text>Válassza ki a kívánt fizetési módot.</Text>
      <Field
        type="select"
        options={productOptions}
        onChange={(newValue) => onProductSelect(newValue)}
        register={register}
        name="product"
      />
      <NextButton toCenter onClick={onNextClick}>
        Véglegesítés
      </NextButton>
    </View>
  );
}
