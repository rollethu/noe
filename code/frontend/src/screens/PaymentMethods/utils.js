export function makePaymentUpdateRequest(appointment) {
  return {
    appointment: appointment.url,
    payment_method_type: "ON_SITE",
    total_price: appointment.total_price,
    currency: appointment.currency,
  };
}
