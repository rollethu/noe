import { ROUTE_ADD_SEAT, ROUTE_CHECKOUT } from "../../App";

export const SUBMIT_MODE_CREATE = "CREATE";
export const SUBMIT_MODE_UPDATE = "UPDATE";

export function getFieldTypeFromSurveyAnswerType(question) {
  switch (question.answer_datatype) {
    case "BOOLEAN":
      return "survey-toggle";
    case "INTEGER":
      return "number";
    // including `STRING`
    default:
      return "text";
  }
}

export function getSubmitMode(surveyAnswersForActiveSeat) {
  return surveyAnswersForActiveSeat === null
    ? SUBMIT_MODE_CREATE
    : SUBMIT_MODE_UPDATE;
}

export function getFormData(
  submitMode,
  surveyQuestions,
  surveyAnswersForActiveSeat
) {
  if (submitMode === SUBMIT_MODE_CREATE) {
    return getFormDataForCreation(surveyQuestions);
  }

  return getFormDataForUpdate(surveyQuestions, surveyAnswersForActiveSeat);
}

function getFormDataForCreation(surveyQuestions) {
  return surveyQuestions.map((question, i) => {
    const fieldType = getFieldTypeFromSurveyAnswerType(question);
    return {
      label: question.question,
      name: `question-${i}`, // To create answers based on the question url
      type: fieldType,
      defaultValue: fieldType === "survey-toggle" ? "no" : "",
    };
  });
}

function getFormDataForUpdate(surveyQuestions, surveyAnswersForActiveSeat) {
  return surveyQuestions.map((question, i) => {
    const existingAnswer = surveyAnswersForActiveSeat.filter(
      (answer) => answer.question === question.url
    )[0];
    return {
      label: question.question,
      name: `answer-${i}`, // To update existing answers based on their urls
      type: getFieldTypeFromSurveyAnswerType(question),
      defaultValue: existingAnswer.answer,
    };
  });
}

export const processCreateValues = (values, activeSeat, surveyQuestions) => {
  return Object.keys(values).map((questionFieldName) => {
    const index = parseInt(questionFieldName.split("-")[1], 10);
    const question = surveyQuestions[index];
    return {
      question: question.url,
      answer: values[questionFieldName],
      seat: activeSeat.url,
    };
  });
};

export const processUpdateValues = (values, surveyAnswersForActiveSeat) => {
  return Object.keys(values).map((answerFieldName) => {
    const index = parseInt(answerFieldName.split("-")[1], 10);
    const answer = surveyAnswersForActiveSeat[index];
    return {
      url: answer.url,
      answer: values[answerFieldName],
      seat: answer.seat,
      question: answer.question,
    };
  });
};

export function getRedirectRoute(submitMode) {
  return submitMode === SUBMIT_MODE_CREATE ? ROUTE_ADD_SEAT : ROUTE_CHECKOUT;
}

export function matchQuestionErrors(errors, questions) {
  return matchErrors(errors, questions, "question-");
}

export function matchAnswerErrors(errors, existingAnswers) {
  return matchErrors(errors, existingAnswers, "answer-");
}

export function matchErrors(errors, data, prefix) {
  // Data can be list of question, or a list of existing answers
  // Matches error keys (urls) with form fields (question or answer)

  if (errors === undefined) {
    return {};
  }

  const matchedErrors = {};
  Object.keys(errors).forEach((error) => {
    const questionUrl = error;
    let matchingIndex = null;
    data.forEach((q, i) => {
      if (q.url === questionUrl) {
        matchingIndex = i;
      }
    });

    if (matchingIndex !== null) {
      matchedErrors[`${prefix}${matchingIndex}`] = errors[error];
    }
  });

  return matchedErrors;
}
