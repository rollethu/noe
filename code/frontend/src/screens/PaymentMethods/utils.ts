import { useFeatureSimplePay } from "../../featureFlags";
import { Appointment } from "../../models";

export function makePaymentUpdateRequest(appointment: Appointment, productID, billingDetailsValues, paymentMethod) {
  return {
    appointment: appointment.url,
    total_price: appointment.totalPrice,
    currency: appointment.currency,
    product_type: productID,
    ...(useFeatureSimplePay ? { payment_method: paymentMethod } : {}),
    ...billingDetailsValues,
  };
}

export function getTotalPriceDisplay(appointment: Appointment) {
  if (!appointment.currency) {
    return "Ár nem elérhető!";
  }

  let currency = appointment.currency;
  if (currency === "HUF") {
    currency = "Ft";
  }

  return `${appointment.totalPrice} ${currency}`;
}
