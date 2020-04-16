import React from "react";
import { useLocation, Redirect } from "react-router-dom";

import { Context as AppointmentContext } from "../contexts/appointmentContext";
import { View, Caption } from "../UI";

export default function VerifyEmail(props) {
  const { state, verifyToken } = React.useContext(AppointmentContext);
  const {
    appointmentUrl,
    appointmentEmail,
    isAppointmentEmailVerified,
  } = state;
  const queryParams = new URLSearchParams(useLocation().search);

  React.useEffect(() => {
    verifyToken(queryParams.get("Token"));
  }, []);

  console.log(appointmentUrl, appointmentEmail, isAppointmentEmailVerified);
  if (appointmentUrl && appointmentEmail && isAppointmentEmailVerified) {
    return (
      <View>
        <Caption>Success</Caption>
      </View>
    );
  } else if (isAppointmentEmailVerified === false) {
    return (
      <View>
        <Caption>Failed</Caption>
      </View>
    );
  } else if (isAppointmentEmailVerified === true) {
    // verified appointment without email or url is a server error
    alert("Unexpected error occured.");
  }

  return (
    <View>
      <Caption>Loading</Caption>
    </View>
  );
}
