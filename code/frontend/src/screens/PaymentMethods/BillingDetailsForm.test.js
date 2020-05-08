import React from "react";
import { shallow } from "enzyme";
import { act } from "react-dom/test-utils";
import renderer from "react-test-renderer";
import BillingDetailsForm from "./BillingDetailsForm";
import { Form } from "../../UI";

test("Matches snapshot", () => {
  const wrapper = renderer.create(<BillingDetailsForm />).toJSON();
  expect(wrapper).toMatchSnapshot();
});

test("Calls onSubmit", () => {
  const mockSubmit = jest.fn();
  const wrapper = shallow(<BillingDetailsForm onSubmit={mockSubmit} />);
  const form = wrapper.find(Form);
  act(() => {
    form.simulate("submit");
  });
  expect(mockSubmit).toHaveBeenCalled();
});
