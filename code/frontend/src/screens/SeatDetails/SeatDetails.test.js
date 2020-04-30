import React from "react";
import axios from "axios";
import { act } from "react-dom/test-utils";
import { mount } from "enzyme";

import SeatDetails from "./SeatDetails";
import { Provider as SeatProvider } from "../../contexts/seatContext";
import { Provider as AppointmentProvider } from "../../contexts/appointmentContext";

jest.mock("axios");
jest.mock("react-router-dom", () => ({
  ...jest.requireActual("react-router-dom"),
  useHistory: jest.fn(() => ({
    push: () => {},
  })),
  useLocation: jest.fn(() => ({})),
}));

test("Update sends healthcare_number", async () => {
  axios.patch.mockResolvedValue({ data: { yolo: "troll" } });
  const wrapper = mount(
    <SeatProvider injectState={{ activeSeat: { url: "fake-url" } }}>
      <AppointmentProvider injectState={{ appointment: { url: "fake-url" } }}>
        <SeatDetails />
      </AppointmentProvider>
    </SeatProvider>
  );
  const form = wrapper.find("form");
  await act(async () => {
    await form.simulate("submit");
  });
  const apiCallValues = axios.patch.mock.calls[0][1];
  expect(
    Object.keys(apiCallValues).indexOf("healthcare_number") > -1
  ).toBeTruthy();
});
