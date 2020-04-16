import React from "react";
import "./styles/styles.css";
import Start from "./screens/Start";
import AddSeat from "./screens/AddSeat";
import EmailVerification from "./screens/EmailVerification";
import PaymentMethod from "./screens/PaymentMethod";
import Registration from "./screens/Registration";
import SeatDetails from "./screens/SeatDetails";
import Survey from "./screens/Survey";
import Time from "./screens/Time";
import { BrowserRouter as Router, Switch, Route, Link } from "react-router-dom";

function App() {
  return (
    <div className="App">
      <Router>
        <Switch>
          <Route path="/start">
            <Start />
          </Route>
          <Route path="/email-megerosites">
            <EmailVerification />
          </Route>
          <Route path="/regisztracio">
            <Registration />
          </Route>
          <Route path="/szemelyes-adatok">
            <SeatDetails />
          </Route>
          <Route path="/kerdoiv">
            <Survey />
          </Route>
          <Route path="/uj-szemely">
            <AddSeat />
          </Route>
          <Route path="/idopont">
            <Time />
          </Route>
          <Route path="/fizetes-mod">
            <PaymentMethod />
          </Route>
          <Route path="/sikeres-regisztracio">
            <Start />
          </Route>
        </Switch>
      </Router>
    </div>
  );
}

export default App;
