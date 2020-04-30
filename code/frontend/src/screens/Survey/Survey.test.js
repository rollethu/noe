import React from "react";
import axios from "axios";
import renderer from "react-test-renderer";
import { act } from "react-dom/test-utils";
import { mount } from "enzyme";
import {
  sendSurveyAnswers,
  updateSurveyAnswers,
} from "../../contexts/surveyContext";
import SurveyForm from "./SurveyForm";
import * as surveyUtils from "./utils";
import { ROUTE_ADD_SEAT, ROUTE_CHECKOUT, ROUTE_START } from "../../App";

jest.mock("axios");

test("SurveyForm for creation renders OK", () => {
  const tree = renderer
    .create(
      <SurveyForm
        submitMode={surveyUtils.SUBMIT_MODE_CREATE}
        surveyAnswersForActiveSeat={null}
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
  const surveyAnswersForActiveSeat = [
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
        submitMode={surveyUtils.SUBMIT_MODE_UPDATE}
        surveyAnswersForActiveSeat={surveyAnswersForActiveSeat}
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
    type: "SET_NEW_SURVEY_ANSWERS",
    payload: {},
  });
});

test("Survey update submission doesn't break without questions", async () => {
  axios.post.mockImplementationOnce(() => Promise.resolve({ data: [] }));
  const mockDispatch = jest.fn(() => {});
  await updateSurveyAnswers(mockDispatch)([]);
  expect(mockDispatch).toHaveBeenCalledWith({
    type: "SET_NEW_SURVEY_ANSWERS",
    payload: {},
  });
});

test("Process survey answers for create", () => {
  const submitValues = {
    "question-0": "Hello",
    "question-1": "Yolo",
  };
  const activeSeat = { url: "http://localhost:8000/api/seats/1/" };
  const surveyQuestions = [
    { url: "http://localhost:8000/api/survey-questsions/1/" },
    { url: "http://localhost:8000/api/survey-questsions/2/" },
  ];
  const expected = [
    {
      question: "http://localhost:8000/api/survey-questsions/1/",
      answer: "Hello",
      seat: "http://localhost:8000/api/seats/1/",
    },
    {
      question: "http://localhost:8000/api/survey-questsions/2/",
      answer: "Yolo",
      seat: "http://localhost:8000/api/seats/1/",
    },
  ];
  const res = surveyUtils.processCreateValues(
    submitValues,
    activeSeat,
    surveyQuestions
  );
  expect(res).toEqual(expected);
});

test("Survey Form create submit with questions as subdomains", async () => {
  const surveyQuestions = [
    {
      url:
        "https://api.noe.rollet.app/api/survey-questsions/1231-123-123-124asdf1/",
    },
    {
      url:
        "https://api.noe.rollet.app/api/survey-questsions/1232-123-123-124asdf2/",
    },
    {
      url:
        "https://api.noe.rollet.app/api/survey-questsions/1233-123-123-124asdf3/",
    },
  ];
  const activeSeat = {
    url: "https://api.noe.rollet.app/api/seats/1/",
  };

  const mockSubmit = jest.fn();
  const wrapper = mount(
    <SurveyForm
      submitMode={surveyUtils.SUBMIT_MODE_CREATE}
      surveyQuestions={surveyQuestions}
      activeSeat={activeSeat}
      surveyAnswersForActiveSeat={null}
      onSubmit={mockSubmit}
    />
  );
  const form = wrapper.find("form");

  await act(async () => {
    await form.simulate("submit");
  });

  expect(mockSubmit.mock.calls[0][0]).toEqual({
    "question-0": "",
    "question-1": "",
    "question-2": "",
  });
});

test("Processing update answers", () => {
  const seatUrl = "https://api.noe.rollet.app/api/seats/1/";
  const surveyAnswersForActiveSeat = [
    {
      seat: seatUrl,
      question: "https://api.noe.rollet.app/api/survey-questions/1/",
      url: "https://api.noe.rollet.app/api/survey-answers/1/",
      answer: "",
    },
    {
      seat: seatUrl,
      question: "https://api.noe.rollet.app/api/survey-questions/2/",
      url: "https://api.noe.rollet.app/api/survey-answers/2/",
      answer: "",
    },
  ];
  const submitValues = {
    "answer-0": "Hello",
    "answer-1": "Yolo",
  };
  const expected = [
    {
      url: "https://api.noe.rollet.app/api/survey-answers/1/",
      question: "https://api.noe.rollet.app/api/survey-questions/1/",
      answer: "Hello",
      seat: seatUrl,
    },
    {
      url: "https://api.noe.rollet.app/api/survey-answers/2/",
      question: "https://api.noe.rollet.app/api/survey-questions/2/",
      answer: "Yolo",
      seat: seatUrl,
    },
  ];
  const res = surveyUtils.processUpdateValues(
    submitValues,
    surveyAnswersForActiveSeat
  );
  expect(res).toEqual(expected);
});

test("Redirect Route", () => {
  expect(surveyUtils.getRedirectRoute(surveyUtils.SUBMIT_MODE_CREATE)).toBe(
    ROUTE_ADD_SEAT
  );
  expect(surveyUtils.getRedirectRoute(surveyUtils.SUBMIT_MODE_UPDATE)).toBe(
    ROUTE_CHECKOUT
  );
});

test("matchQuestionErrors", () => {
  const questions = [{ url: "url1" }, { url: "url2" }, { url: "url3" }];
  const errors = { url1: "error1", url3: "error3" };

  const matchings = surveyUtils.matchQuestionErrors(errors, questions);
  const expected = { "question-0": "error1", "question-2": "error3" };
  expect(matchings).toEqual(expected);
});

test("matchQuestionErrors if no errors", () => {
  const questions = [{ url: "url1" }, { url: "url2" }, { url: "url3" }];
  const errors = {};

  const matchings = surveyUtils.matchQuestionErrors(errors, questions);
  const expected = {};
  expect(matchings).toEqual(expected);
});

test("matchQuestionErrors if errors are undefined", () => {
  const questions = [{ url: "url1" }, { url: "url2" }, { url: "url3" }];
  const errors = undefined;

  const matchings = surveyUtils.matchQuestionErrors(errors, questions);
  const expected = {};
  expect(matchings).toEqual(expected);
});

test("Test redirect route on submission", () => {
  const cases = [
    [["CREATE", undefined], ROUTE_ADD_SEAT],
    [["UPDATE", undefined], ROUTE_CHECKOUT],
    [["CREATE", ROUTE_START], ROUTE_START],
    [["CREATE", ROUTE_CHECKOUT], ROUTE_CHECKOUT],
    [["UPDATE", ROUTE_START], ROUTE_START],
    [["UPDATE", ROUTE_CHECKOUT], ROUTE_CHECKOUT],
  ];
  cases.forEach((testCase) => {
    expect(surveyUtils.getRedirectRoute(...testCase[0])).toBe(testCase[1]);
  });
});
