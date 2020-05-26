jest.mock("react-router-dom", () => ({
  ...jest.requireActual("react-router-dom"),
  useHistory: jest.fn(() => ({
    push: () => {},
  })),
  useLocation: jest.fn(() => ({})),
}));

import React from "react";
import { mount } from "enzyme";

import { Provider as AppointmentProvider } from "../../contexts/appointmentContext";
import { Provider as SeatProvider } from "../../contexts/seatContext";
import { Provider as SurveyProvider } from "../../contexts/surveyContext";
import { Provider as TimeSlotProvider } from "../../contexts/timeSlotContext";
import { Provider as LocationProvider } from "../../contexts/locationContext";
import PaymentMethods, { SIMPLEPAY } from "./PaymentMethods";

test("Online Payment is the default value", () => {
  const wrapper = mount(
    <SurveyProvider>
      <TimeSlotProvider>
        <LocationProvider>
          <AppointmentProvider>
            <SeatProvider>
              <PaymentMethods />
            </SeatProvider>
          </AppointmentProvider>
        </LocationProvider>
      </TimeSlotProvider>
    </SurveyProvider>
  );
  const activePaymentMethod = wrapper.find("label.Active").find("input");
  expect(activePaymentMethod.props().value).toBe(SIMPLEPAY);
});
