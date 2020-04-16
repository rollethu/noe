import React from "react";
import {
  BrowserRouter as Router,
  Switch,
  Route,
  Redirect,
} from "react-router-dom";

import "./styles/styles.css";
import { Provider as AppointmentProvider } from "./contexts/appointmentContext";
import Nav from "./components/Nav";
import Start from "./screens/Start";
import AddSeat from "./screens/AddSeat";
import EmailVerification from "./screens/EmailVerification";
import PaymentMethod from "./screens/PaymentMethod";
import Registration from "./screens/Registration";
import SeatDetails from "./screens/SeatDetails";
import Survey from "./screens/Survey";
import Time from "./screens/Time";
import Checkout from "./screens/Checkout";
import AppointmentSuccess from "./screens/AppointmentSuccess";

export const ROUTE_START = "/start";
export const ROUTE_EMAIL_VERIFICATION = "/megerosito-email";
export const ROUTE_REGISTRATION = "/regisztracio";
export const ROUTE_SEAT_DETAILS = "/szemelyes-adatok";
export const ROUTE_SURVEY = "/kerdoiv";
export const ROUTE_ADD_SEAT = "/uj-szemely";
export const ROUTE_TIME = "/idopont";
export const ROUTE_PAYMENT_METHOD = "/fizetesi-mod";
export const ROUTE_CHEKCOUT = "/osszegzes";
export const ROUTE_APPOINTMENT_SUCCESS = "/sikeres-regisztracio";

function App() {
  const routes = [
    { path: ROUTE_START, component: Start },
    { path: ROUTE_EMAIL_VERIFICATION, component: EmailVerification },
    { path: ROUTE_REGISTRATION, component: Registration },
    { path: ROUTE_SEAT_DETAILS, component: SeatDetails },
    { path: ROUTE_SURVEY, component: Survey },
    { path: ROUTE_ADD_SEAT, component: AddSeat },
    { path: ROUTE_TIME, component: Time },
    { path: ROUTE_PAYMENT_METHOD, component: PaymentMethod },
    { path: ROUTE_CHEKCOUT, component: Checkout },
    { path: ROUTE_APPOINTMENT_SUCCESS, component: AppointmentSuccess },
  ];
  return (
    <div className="App">
      <Router>
        <Nav routes={routes} />
        <Redirect exact from="/" to={routes[0].path} />
        <Switch>
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
      <App />
    </AppointmentProvider>
  );
}

export default WrappedApp;
