export function makePaymentUpdateRequest(appointment, productID, billingDetailsValues, paymentMethod) {
  return {
    appointment: appointment.url,
    total_price: appointment.total_price,
    currency: appointment.currency,
    product_type: productID,
    payment_method: paymentMethod, // useFeatureSimplePay; backend currently ignores
    ...billingDetailsValues,
  };
}

export function getTotalPriceDisplay(appointment) {
  if (!appointment.currency) {
    return "Ár nem elérhető!";
  }

  let currency = appointment.currency;
  if (currency === "HUF") {
    currency = "Ft";
  }

  return `${appointment.total_price} ${currency}`;
}
