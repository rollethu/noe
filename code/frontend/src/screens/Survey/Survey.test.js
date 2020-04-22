import React from "react";
import axios from "axios";
import { shallow, mount } from "enzyme";
import renderer from "react-test-renderer";

import {
  sendSurveyAnswers,
  updateSurveyAnswers,
} from "../../contexts/surveyContext";
import SurveyForm from "./SurveyForm";

jest.mock("axios");

test("SurveyForm for creation renders OK", () => {
  const tree = renderer
    .create(
      <SurveyForm
        activeSurvey={null}
        surveyQuestions={[
          { url: "fake-url-1" },
          { url: "fake-url-2" },
          { url: "fake-url-3" },
        ]}
      />
    )
    .toJSON();
  expect(tree).toMatchSnapshot();
});

test("SurveyForm for update renders OK", () => {
  const activeSurvey = [
    { seat: "seat-1-url", question: "fake-url-1", url: "answer-1-url" },
    { seat: "seat-1-url", question: "fake-url-2", url: "answer-2-url" },
    { seat: "seat-1-url", question: "fake-url-3", url: "answer-3-url" },
  ];
  const surveyQuestions = [
    { url: "fake-url-1" },
    { url: "fake-url-2" },
    { url: "fake-url-3" },
  ];
  const tree = renderer
    .create(
      <SurveyForm
        activeSurvey={activeSurvey}
        surveyQuestions={surveyQuestions}
      />
    )
    .toJSON();
  expect(tree).toMatchSnapshot();
});

test("Survey submission doesn't break without questions", async () => {
  axios.post.mockImplementationOnce(() => Promise.resolve({ data: [] }));
  const mockDispatch = jest.fn(() => {});
  await sendSurveyAnswers(mockDispatch)();
  expect(mockDispatch).toHaveBeenCalledWith({
    type: "ADD_SURVEY_ANSWERS",
    payload: {},
  });
});

test("Survey update submission doesn't break without questions", async () => {
  axios.post.mockImplementationOnce(() => Promise.resolve({ data: [] }));
  const mockDispatch = jest.fn(() => {});
  await updateSurveyAnswers(mockDispatch)([]);
  expect(mockDispatch).toHaveBeenCalledWith({
    type: "UPDATE_SURVEY_ANSWERS",
    payload: {},
  });
});
