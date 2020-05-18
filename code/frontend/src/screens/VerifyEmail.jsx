import React from "react";
import { useLocation } from "react-router-dom";

import { Context as AppointmentContext } from "../contexts/appointmentContext";
import { View, Caption } from "../UI";
import EmailVerificationSuccess from "./EmailVerificationSuccess";
import EmailVerificationFailure from "./EmailVerificationFailure";

export default function VerifyEmail(props) {
  const {
    state: { appointment, emailVerification },
    verifyToken,
  } = React.useContext(AppointmentContext);
  const queryParams = new URLSearchParams(useLocation().search);

  React.useEffect(() => {
    verifyToken(queryParams.get("token"));
  }, []);

  if (appointment?.url && appointment?.email && appointment?.isEmailVerified) {
    return <EmailVerificationSuccess />;
  } else if (appointment?.isEmailVerified === false) {
    return <EmailVerificationFailure error={emailVerification.error} />;
  } else if (appointment?.isEmailVerified === true) {
    // verified appointment without email or url is a server error
    alert("Unexpected error occured.");
  }

  return (
    <View>
      <Caption>Loading</Caption>
    </View>
  );
}
