import axios from "axios";

export async function handleRequest(requestCreator) {
  let response;
  try {
    response = await requestCreator();
    response.error = false;
  } catch (error) {
    if (!error.response) {
      return { error: true };
    }
    response = error.response;
    setErrorFlagsOnResponse(response);
  }
  return response;
}

function setErrorFlagsOnResponse(response) {
  response.error = true;
  response.errors = response.data;
}

export function addStateToLocalStorage(state) {
  localStorage.clear();
  localStorage.setItem("appointmentState", JSON.stringify(state.appointmentState));
  localStorage.setItem("seatState", JSON.stringify(state.seatState));
  localStorage.setItem("surveyState", JSON.stringify(state.surveyState));
}

export function loadStateFromLocalStorage(setters) {
  setters.setAppointmentState(JSON.parse(localStorage.getItem("appointmentState")));
  setters.setSeatState(JSON.parse(localStorage.getItem("seatState")));
  setters.setSurveyState(JSON.parse(localStorage.getItem("surveyState")));
  localStorage.clear();
}

export function setDefaultAuthorizationHeader(token) {
  axios.defaults.headers.common["Authorization"] = `Apptoken ${token}`;
}
