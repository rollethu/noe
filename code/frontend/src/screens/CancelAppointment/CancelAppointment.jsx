import React from "react";
import { useLocation } from 'react-router-dom'
import ConfirmCancelAppointment from "./ConfirmCancelAppointment";
import { Context as AppointmentContext } from '../../contexts/appointmentContext'
import { setDefaultAuthorizationHeader } from "../../contexts/utils";

export default function CancelAppointment() {
  const params = new URLSearchParams(useLocation().search)
  const token = params.get('token');
  const { state: { appointment }, fetchCurrentAppointment } = React.useContext(AppointmentContext)

  React.useEffect(() => {
    setDefaultAuthorizationHeader(token)
    fetchCurrentAppointment()
  }, [])

  if (appointment === null) {
    return null;
  }

  return (
    <ConfirmCancelAppointment
      locationName={appointment.locationName || "Nincs helyszín"}
      licencePlate={appointment.licencePlate || "Nincs rendszám"}
      appointment={appointment}
    />
  );
}
