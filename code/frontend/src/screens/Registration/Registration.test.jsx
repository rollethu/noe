import React from "react";
import { mount } from "enzyme";
import renderer from "react-test-renderer";

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

test("Location field is disbaled", () => {
  const wrapper = mount(<RegistrationForm locationOptions={[]} appointment={{ locationUrl: "fake-url" }} />);
  expect(wrapper.find("select[name='location']").props()).toHaveProperty("disabled", true);
});

test("Registration form before save", () => {
  const tree = renderer.create(<RegistrationForm locationOptions={[]} appointment={{ url: "fake-url" }} />).toJSON();
  expect(tree).toMatchSnapshot();
});

test("Registration form after save", () => {
  const tree = renderer
    .create(
      <RegistrationForm
        locationOptions={[]}
        appointment={{
          url: "fake-url",
          locationUrl: "fake-url",
          licencePlate: "fake-plate",
        }}
      />
    )
    .toJSON();
  expect(tree).toMatchSnapshot();

  // Snapshot tests don't see input values
  const wrapper = mount(
    <RegistrationForm
      locationOptions={[]}
      appointment={{
        url: "fake-url",
        location: "fake-url",
        licencePlate: "fake-plate",
      }}
    />
  );
  expect(wrapper.find("input[name='licence_plate']").getDOMNode().value).toBe("fake-plate");
});
