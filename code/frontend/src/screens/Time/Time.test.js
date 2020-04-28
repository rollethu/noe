jest.mock("react-router-dom", () => ({
  useHistory: () => {},
}));
jest.mock("axios");
import axios from "axios";

import React from "react";
import { mount, shallow } from "enzyme";
import { act } from "react-dom/test-utils";

import Time from "./Time";
import TimeForm from "./TimeForm";
import { makeDateTimeFromDate, updateFiltersWithDate } from "./utils";
import { Provider as AppointmentProvider } from "../../contexts/appointmentContext";
import { Provider as TimeSlotProvider } from "../../contexts/timeSlotContext";
import { Provider as SeatProvider } from "../../contexts/seatContext";

test("Transforms date string to datetime with timezone", () => {
  Date.now = () => new Date("2020-06-14T12:34:56+02:00").getTime();
  const params = [
    ["2020-01-01", "2020-01-01T12:34:56+01:00"],
    ["2020-06-14", "2020-06-14T12:34:56+02:00"],
  ];
  params.forEach((params) => {
    const [input, expected] = params;
    const actual = makeDateTimeFromDate(input);
    expect(actual).toBe(expected);
  });
});

test("Date change triggers onDateChange", async () => {
  const mockOnDateChange = jest.fn();
  const wrapper = mount(
    <TimeForm onDateChange={mockOnDateChange} timeSlots={[]} />
  );
  const dateInput = wrapper.find('input[name="date"]');
  await act(async () => {
    await dateInput.simulate("change", { target: { value: "2020-01-04" } });
  });
  expect(mockOnDateChange).toHaveBeenCalledWith("2020-01-04");
});

test("Update filter with date", () => {
  Date.now = () => new Date("2020-06-14T12:34:56+02:00").getTime();
  const filters = {};
  updateFiltersWithDate(filters, "2008-08-12");
  expect(filters).toEqual({ start_date: "2008-08-12T12:34:56+02:00" });
});

test("Sends API request on date change", async () => {
  Date.now = () => new Date("2020-06-14T12:34:56+02:00").getTime();
  const wrapper = mount(
    <AppointmentProvider>
      <TimeSlotProvider>
        <SeatProvider>
          <Time />
        </SeatProvider>
      </TimeSlotProvider>
    </AppointmentProvider>
  );
  const dateInput = wrapper.find('input[name="date"]');
  axios.get.mockClear();
  await act(async () => {
    await dateInput.simulate("change", { target: { value: "2020-01-04" } });
  });

  expect(axios.get.mock.calls[0][0].split("?")[1]).toBe(
    "location=null&min_availability=0&start_date=2020-01-04T12:34:56+01:00"
  );
});

test("Min date is today on date field", () => {
  Date.now = () => new Date("2020-01-31T12:34:56+02:00").getTime();
  const wrapper = mount(<TimeForm timeSlots={[]} />);
  const dateInput = wrapper.find("input[type='date']");
  expect(dateInput.props()).toHaveProperty("min", "2020-01-31");
});
