import React from "react";
import { useHistory } from "react-router-dom";
import { Context as SeatContext } from "../../contexts/seatContext";
import { Context as AppointmentContext } from "../../contexts/appointmentContext";
import { Context as TimeSlotContext } from "../../contexts/timeSlotContext";
import { Context as SurveyContext } from "../../contexts/surveyContext";
import { ROUTE_SEAT_DETAILS } from "../../App";
import CheckoutContent from "./CheckoutContent";
import * as checkoutUtils from "./utils";
import * as utils from "../../utils";

export default function Checkout() {
  const history = useHistory();
  const {
    state: { seats },
    deleteSeat,
    setActiveSeat,
  } = React.useContext(SeatContext);
  const {
    state: { appointment },
  } = React.useContext(AppointmentContext);
  const {
    state: { selectedTimeSlot },
    fetchSelectedTimeSlot,
  } = React.useContext(TimeSlotContext);
  const { setActiveSurveyAnswers } = React.useContext(SurveyContext);
  const isAddSeatDisabled = utils.isMaxSeatCountReached(seats);

  React.useEffect(() => {
    if (!appointment) {
      return;
    }
    fetchSelectedTimeSlot(appointment.time_slot);
  }, []);

  function onSeatEditClick(seat) {
    setActiveSeat(seat);
    setActiveSurveyAnswers(seat);
    history.push(ROUTE_SEAT_DETAILS);
  }

  function onSeatDeleteClick(seat) {
    if (!checkoutUtils.canDeleteSeat(seats)) {
      return;
    }

    const confirmed = window.confirm("Biztosan törölni akarja?");
    if (!confirmed) {
      return;
    }
    deleteSeat(seat.url);
  }

  function onNewSeatClick() {
    history.push(ROUTE_SEAT_DETAILS);
  }

  return (
    <CheckoutContent
      appointment={appointment}
      seats={seats}
      onSeatEditClick={onSeatEditClick}
      onSeatDeleteClick={onSeatDeleteClick}
      selectedTimeSlot={selectedTimeSlot}
      onNewSeatClick={onNewSeatClick}
      isAddSeatDisabled={isAddSeatDisabled}
    />
  );
}
