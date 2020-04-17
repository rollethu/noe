import React from "react";
import { useLocation, Redirect } from "react-router-dom";

import { ROUTE_REGISTRATION } from "../App";
import { Context as AppointmentContext } from "../contexts/appointmentContext";
import { View, Caption, LinkButton } from "../UI";

const TXT_BUTTON = "Tovább";

export default function VerifyEmail(props) {
  const { state, verifyToken } = React.useContext(AppointmentContext);
  const {
    state: { appointment },
  } = state;
  const queryParams = new URLSearchParams(useLocation().search);

  React.useEffect(() => {
    verifyToken(queryParams.get("token"));
  }, []);

  if (appointment.url && appointment.email && appointment.isEmailVerified) {
    return (
      <View>
        <Caption>Success</Caption>
        <LinkButton toCenter to={ROUTE_REGISTRATION}>
          {TXT_BUTTON}
        </LinkButton>
      </View>
    );
  } else if (appointment.isEmailVerified === false) {
    return (
      <View>
        <Caption>Failed</Caption>
      </View>
    );
  } else if (appointment.isEmailVerified === true) {
    // verified appointment without email or url is a server error
    alert("Unexpected error occured.");
  }

  return (
    <View>
      <Caption>Loading</Caption>
    </View>
  );
}
