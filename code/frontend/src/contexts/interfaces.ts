import { Appointment } from "../models";

export interface AppointmentState {
  appointment: Appointment | null;
  emailVerification: any;
  productId: any;
  token: string; // Used for authorization during appointment session
}

export interface SeatState {
  seats: any[];
  activeSeat: any;
}

export interface SurveyState {
  surveyQuestions: any[];
  surveyAnswers: any[];
  surveyAnswersForActiveSeat: any[];
}
