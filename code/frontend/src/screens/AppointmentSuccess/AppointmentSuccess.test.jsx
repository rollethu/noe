const mockResetState = jest.fn();
jest.mock("../../contexts/common", () => ({
  resetState: () => mockResetState,
}));

import React from "react";
import { mount } from "enzyme";

import AppointmentSuccess from "./AppointmentSuccess";
import { Provider as AppointmentProvider } from "../../contexts/appointmentContext";
import { Provider as SeatProvider } from "../../contexts/seatContext";
import { Provider as SurveyProvider } from "../../contexts/surveyContext";
import { Provider as TimeSlotProvider } from "../../contexts/timeSlotContext";

test("AppointmentSuccess resets all states", () => {
  mount(
    <AppointmentProvider>
      <SeatProvider>
        <SurveyProvider>
          <TimeSlotProvider>
            <AppointmentSuccess />
          </TimeSlotProvider>
        </SurveyProvider>
      </SeatProvider>
    </AppointmentProvider>
  );
  expect(mockResetState).toHaveBeenCalledTimes(4);
});
