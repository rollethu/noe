import { initialState as appointmentInitialState } from "./appointmentContext";
import { initialState as seatInitialState } from "./seatContext";
import { initialState as surveyInitialState } from "./surveyContext";

test("Appointment initial state is empty", () => {
  // It's common to prefill appointment during testing.
  // To prevent this going to production, here is this test
  const expected = {
    appointment: {
      url: null,
      email: null,
      isEmailVerified: null,
    },
    emailVerification: {
      error: null,
    },
    productId: null,
  };
  expect(appointmentInitialState).toStrictEqual(expected);
});

test("Seat initial state is empty", () => {
  // It's common to prefill seats during testing.
  // To prevent this going to production, here is this test
  const expected = {
    seats: [],
    activeSeat: null,
  };
  expect(seatInitialState).toStrictEqual(expected);
});

test("Survey initial state is empty", () => {
  // It's common to prefill survey during testing.
  // To prevent this going to production, here is this test
  const expected = {
    surveyQuestions: null,
    surveyAnswers: {},
    surveyAnswersForActiveSeat: null,
  };
  expect(surveyInitialState).toStrictEqual(expected);
});
