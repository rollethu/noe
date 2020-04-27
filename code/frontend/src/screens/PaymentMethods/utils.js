export function makePaymentUpdateRequest(appointment) {
  return {
    appointment: appointment.url,
    payment_method_type: "ON_SITE",
    total_price: appointment.total_price,
    currency: appointment.currency,
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
