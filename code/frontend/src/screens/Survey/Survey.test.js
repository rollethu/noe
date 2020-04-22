import React from "react";
import axios from "axios";
import { mount } from "enzyme";

import { sendSurveyAnswers } from "../../contexts/surveyContext";
import SurveyForm from "./SurveyForm";

jest.mock("axios");

test("Survey submission without questsions doesn't break", () => {
  const surveyQuestions = [];
  const activeSeat = { url: "seat-url-1" };
  const mock = jest.fn(() => {});
  const tree = mount(
    <SurveyForm
      surveyQuestions={surveyQuestions}
      activeSurvey={null}
      activeSeat={activeSeat}
      sendSurveyAnswers={mock}
      setActiveSeat={() => {}}
      setActiveSurvey={() => {}}
    />
  );
  const submitButton = tree.find("button");
  expect(submitButton.text()).toBe("Tovább");
  const form = tree.find("form");
  form.simulate("submit");
  expect(mock).toHaveBeenCalled();
});

test("Survey submission doesn't break without questsions", async () => {
  axios.post.mockImplementationOnce(() => Promise.resolve({ data: [] }));
  const mockDispatch = jest.fn(() => {});
  await sendSurveyAnswers(mockDispatch)();
  expect(mockDispatch).toHaveBeenCalledWith({
    type: "ADD_SURVEY_ANSWERS",
    payload: {},
  });
});
