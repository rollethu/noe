export function makePaymentUpdateRequest(appointment) {
  return {
    appointment: appointment.url,
    payment_method_type: "ON_SITE",
    total_price: appointment.total_price,
    currency: appointment.currency,
  };
}

export function getTotalPriceDisplay(appointment) {
  let total = "Ár nem elérhető!";
  if (
    appointment.total_price !== undefined &&
    appointment.currency !== undefined
  ) {
    const currency =
      appointment.currency === "HUF" ? "Ft" : appointment.currency;
    total = `${appointment.total_price} ${currency}`;
  }

  return total;
}
