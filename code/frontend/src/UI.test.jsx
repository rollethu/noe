import React from "react";
import { shallow } from "enzyme";

import { Pill } from "./UI";

describe("Pill UI component", () => {
  test("Renders external link", () => {
    const wrapper = shallow(<Pill to="http://" />);
    const aTag = wrapper.find("a");
    expect(aTag.exists()).toBe(true);
    expect(aTag.props()).toHaveProperty("target", "_blank");
  });

  test("Renders internal link", () => {
    const wrapper = shallow(<Pill to="/start" />);
    const link = wrapper.find("Link");
    expect(link.exists()).toBe(true);
  });

  test("Doesn't render link without `to`", () => {
    const wrapper = shallow(<Pill />);
    const link = wrapper.find("Link");
    const aTag = wrapper.find("Link");
    expect(link.exists()).toBe(false);
    expect(aTag.exists()).toBe(false);
  });

  test("Becomes Info", () => {
    const wrapper = shallow(<Pill info />);
    const pillComponent = wrapper.find(".Pill");
    expect(pillComponent.hasClass("Info")).toBe(true);
  });

  test("Becomes Success", () => {
    const wrapper = shallow(<Pill success />);
    const pillComponent = wrapper.find(".Pill");
    expect(pillComponent.hasClass("Success")).toBe(true);
  });

  test("Becomes Error", () => {
    const wrapper = shallow(<Pill error />);
    const pillComponent = wrapper.find(".Pill");
    expect(pillComponent.hasClass("Error")).toBe(true);
  });
});
