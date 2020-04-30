import React from "react";
import moment from "moment";

export function formatAppointmentDate(selectedTimeSlot) {
  if (!selectedTimeSlot) {
    return "";
  }

  const start = moment(selectedTimeSlot.start);
  return (
    <>
      {`${start.format("YYYY. MM. DD.")}`}
      <br />
      {`${start.format("HH:mm")}-${moment(selectedTimeSlot.end).format(
        "HH:mm"
      )}`}
    </>
  );
}

export function canDeleteSeat(seats) {
  return seats.length > 1;
}
