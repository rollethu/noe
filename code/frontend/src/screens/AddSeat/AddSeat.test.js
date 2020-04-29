import React from "react";
import { mount } from "enzyme";
import { BrowserRouter as Router } from "react-router-dom";
import _ from "lodash";

import * as utils from "../../utils";
import { Provider as SeatProvider } from "../../contexts/seatContext";
import AddSeat from "./AddSeat";

test("Add new seat button is active", () => {
  const wrapper = mount(
    <Router>
      <SeatProvider>
        <AddSeat />
      </SeatProvider>
    </Router>
  );

  const addNewSeatButton = wrapper.find("#AddSeatButton");
  expect(addNewSeatButton.props()).toHaveProperty("disabled", false);
});

test("Add new seat button is disabled if seat count is reached", () => {
  const seats = _.range(utils.MAX_SEATS_PER_APPOINTMENT).map(() => {
    return {};
  });

  const wrapper = mount(
    <Router>
      <SeatProvider injectState={{ seats }}>
        <AddSeat />
      </SeatProvider>
    </Router>
  );

  const addNewSeatButton = wrapper.find("#AddSeatButton");
  expect(addNewSeatButton.props()).toHaveProperty("disabled", true);
});
