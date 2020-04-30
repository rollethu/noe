import React from "react";
import { mount } from "enzyme";

import RegistrationForm from "./RegistrationForm";
import { Field } from "../../UI";

test("Licence plate field has no help text", () => {
  const wrapper = mount(<RegistrationForm locationOptions={[]} />);

  const licencePlateField = wrapper.find(Field).last();
  expect(licencePlateField.props()).toHaveProperty("name", "licence_plate");

  const helpBlock = licencePlateField.find(".HelpBlock");
  expect(helpBlock.exists()).toBeFalsy();
});

test("Location field has help test", () => {
  const wrapper = mount(<RegistrationForm locationOptions={[]} />);

  const licencePlateField = wrapper.find(Field).first();
  expect(licencePlateField.props()).toHaveProperty("name", "location");

  const helpBlock = licencePlateField.find(".HelpBlock");
  expect(helpBlock.exists()).toBeTruthy();
});
