import React from "react";
import "./styles/styles.css";

import Nav from "./components/Nav";
import Start from "./screens/Start";
import AddSeat from "./screens/AddSeat";
import EmailVerification from "./screens/EmailVerification";
import PaymentMethod from "./screens/PaymentMethod";
import Registration from "./screens/Registration";
import SeatDetails from "./screens/SeatDetails";
import Survey from "./screens/Survey";
import Time from "./screens/Time";
import AppointmentSuccess from "./screens/AppointmentSuccess";
import { BrowserRouter as Router, Switch, Route } from "react-router-dom";

function App() {
  const routes = [
    { path: "/start", component: Start },
    { path: "/email-megerosites", component: EmailVerification },
    { path: "/regisztracio", component: Registration },
    { path: "/uj-szemely", component: AddSeat },
    { path: "/fizetesi-mod", component: PaymentMethod },
    { path: "/szemelyes-adatok", component: SeatDetails },
    { path: "/kerdoiv", component: Survey },
    { path: "/idopont", component: Time },
    { path: "/sikeres-regisztracio", component: AppointmentSuccess },
  ];
  return (
    <div className="App">
      <Router>
        <Nav routes={routes} />
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

export default App;
