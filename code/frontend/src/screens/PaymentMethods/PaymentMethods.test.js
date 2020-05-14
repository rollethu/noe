jest.mock("react-router-dom", () => ({
  ...jest.requireActual("react-router-dom"),
  useHistory: jest.fn(() => ({
    push: () => {},
  })),
  // useLocation: jest.fn(() => ({})),
}));

import React from "react";
import { mount } from "enzyme";

import { Provider as AppointmentProvider } from "../../contexts/appointmentContext";
import { Provider as SeatProvider } from "../../contexts/seatContext";
import PaymentMethods, { CREDIT_CARD_ONLINE } from "./PaymentMethods";

test("Online Payment is the default value", () => {
  const wrapper = mount(
    <AppointmentProvider>
      <SeatProvider>
        <PaymentMethods />
      </SeatProvider>
    </AppointmentProvider>
  );
  const paymentMethodField = wrapper.find('select[name="payment_method"]');
  expect(paymentMethodField.getDOMNode().value).toBe(CREDIT_CARD_ONLINE);
});
