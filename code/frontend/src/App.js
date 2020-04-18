import React from "react";
import {
  BrowserRouter as Router,
  Switch,
  Route,
  Redirect,
} from "react-router-dom";

import "./styles/styles.css";
import { Provider as AppointmentProvider } from "./contexts/appointmentContext";
import { Provider as LocationProvider } from "./contexts/locationContext";
import { Provider as SeatProvider } from "./contexts/seatContext";
import { Provider as SurveyProvider } from "./contexts/surveyContext";
import { Provider as TimeSlotProvider } from "./contexts/timeSlotContext";
import Nav from "./components/Nav";
import Start from "./screens/Start/Start";
import AddSeat from "./screens/AddSeat";
import EmailVerification from "./screens/EmailVerification";
import VerifyEmail from "./screens/VerifyEmail";
import PaymentMethod from "./screens/PaymentMethod";
import Registration from "./screens/Registration/Registration";
import SeatDetails from "./screens/SeatDetails/SeatDetails";
import Survey from "./screens/Survey/Survey";
import Time from "./screens/Time/Time";
import Checkout from "./screens/Checkout";
import AppointmentSuccess from "./screens/AppointmentSuccess";

export const ROUTE_START = "/start";
export const ROUTE_EMAIL_VERIFICATION = "/megerosito-email";
export const ROUTE_VERIFY_EMAIL = "/email-megerosites";
export const ROUTE_REGISTRATION = "/regisztracio";
export const ROUTE_SEAT_DETAILS = "/szemelyes-adatok";
export const ROUTE_SURVEY = "/kerdoiv";
export const ROUTE_ADD_SEAT = "/uj-szemely";
export const ROUTE_TIME = "/idopont";
export const ROUTE_PAYMENT_METHODS = "/fizetesi-mod";
export const ROUTE_CHECKOUT = "/osszegzes";
export const ROUTE_APPOINTMENT_SUCCESS = "/sikeres-regisztracio";

let DEFAULT_ROUTE = ROUTE_START;
if (process.env.NODE_ENV === "development") {
  DEFAULT_ROUTE = ROUTE_TIME;
}

function App() {
  const routes = [
    { path: ROUTE_START, component: Start },
    { path: ROUTE_EMAIL_VERIFICATION, component: EmailVerification },
    { path: ROUTE_VERIFY_EMAIL, component: VerifyEmail },
    { path: ROUTE_REGISTRATION, component: Registration },
    { path: ROUTE_SEAT_DETAILS, component: SeatDetails },
    { path: ROUTE_SURVEY, component: Survey },
    { path: ROUTE_ADD_SEAT, component: AddSeat },
    { path: ROUTE_TIME, component: Time },
    { path: ROUTE_PAYMENT_METHODS, component: PaymentMethod },
    { path: ROUTE_CHECKOUT, component: Checkout },
    { path: ROUTE_APPOINTMENT_SUCCESS, component: AppointmentSuccess },
  ];

  return (
    <div className="App">
      <Router>
        <Nav routes={routes} />
        <Switch>
          <Redirect exact from="/" to={DEFAULT_ROUTE} />
          {routes.map((route) => (
            <Route path={route.path} key={route.path}>
              <route.component></route.component>
            </Route>
          ))}
        </Switch>
      </Router>
    </div>
  );
}

function WrappedApp(props) {
  return (
    <AppointmentProvider>
      <LocationProvider>
        <SeatProvider>
          <SurveyProvider>
            <TimeSlotProvider>
              <App />
            </TimeSlotProvider>
          </SurveyProvider>
        </SeatProvider>
      </LocationProvider>
    </AppointmentProvider>
  );
}

export default WrappedApp;
