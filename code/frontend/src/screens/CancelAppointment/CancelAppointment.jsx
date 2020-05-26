import React from "react";
import ConfirmCancelAppointment from "./ConfirmCancelAppointment";

export default function CancelAppointment() {
  const locationName = "KÖKI";
  const licencePlate = "ABC123";
  const selectedTimeSlot = "5";
  const personCount = 3;

  return (
    <ConfirmCancelAppointment
      locationName={locationName}
      licencePlate={licencePlate}
      selectedTimeSlot={selectedTimeSlot}
      personCount={personCount}
    />
  );
}
