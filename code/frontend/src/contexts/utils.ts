import axios from "axios";
import { AppointmentState } from "./interfaces";

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

export function addStateToLocalStorage(states: any) {
  localStorage.clear();
  localStorage.setItem("appointmentState", JSON.stringify(<AppointmentState>states.appointmentState));
  localStorage.setItem("seatState", JSON.stringify(states.seatState));
  localStorage.setItem("surveyState", JSON.stringify(states.surveyState));
}

export function loadStateFromLocalStorage(setters) {
  const appointmentState: AppointmentState = JSON.parse(localStorage.getItem("appointmentState") || "{}");
  setters.setAppointmentState(appointmentState);
  setters.setSeatState(JSON.parse(localStorage.getItem("seatState") || "{}"));
  setters.setSurveyState(JSON.parse(localStorage.getItem("surveyState") || "{}"));

  localStorage.clear();

  setDefaultAuthorizationHeader(appointmentState?.token);
}

export function setDefaultAuthorizationHeader(token) {
  axios.defaults.headers.common["Authorization"] = `Apptoken ${token}`;
}
