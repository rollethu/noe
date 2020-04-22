import React from "react";
import { useHistory } from "react-router-dom";
import moment from "moment";
import { Context as SeatContext } from "../contexts/seatContext";
import { Context as AppointmentContext } from "../contexts/appointmentContext";
import { Context as TimeSlotContext } from "../contexts/timeSlotContext";
import { Context as SurveyContext } from "../contexts/surveyContext";
import {
  View,
  Caption,
  Text,
  DataRow,
  HR,
  IconButton,
  NextLinkButton,
} from "../UI";
import { ROUTE_PAYMENT_METHODS, ROUTE_SEAT_DETAILS } from "../App";

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
  const { setActiveSurvey } = React.useContext(SurveyContext);

  React.useEffect(() => {
    if (!appointment) {
      return;
    }
    fetchSelectedTimeSlot(appointment.time_slot);
  }, []);

  function onSeatEditClick(seat) {
    setActiveSeat(seat);
    setActiveSurvey(seat);
    history.push(ROUTE_SEAT_DETAILS);
  }

  function onSeatDeleteClick(seat) {
    const confirmed = window.confirm("Biztosan törölni akarja?");
    if (!confirmed) {
      return;
    }
    deleteSeat(seat.url);
  }

  const formatAppointmentDate = (selectedTimeSlot) => {
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
  };

  return (
    <View>
      <Caption center>Összegzés</Caption>
      <DataRow>
        <Text light>Regisztrált jármű</Text>
        <Text dark>{appointment.licence_plate}</Text>
      </DataRow>
      <DataRow>
        <Text light>Mintavétel időpontja</Text>
        <Text dark right>
          {formatAppointmentDate(selectedTimeSlot)}
        </Text>
      </DataRow>
      <DataRow>
        <Text light>Mintavétel helyszíne</Text>
        <Text dark>{appointment.location_name}</Text>
      </DataRow>
      {seats.map((seat) => (
        <React.Fragment key={seat.url}>
          <Text strong style={{ marginBottom: 0 }}>
            {seat.full_name}
            {seat.has_doctor_referral && " - Beutalo"}
            <IconButton icon="pencil" onClick={() => onSeatEditClick(seat)} />
            <IconButton icon="close" onClick={() => onSeatDeleteClick(seat)} />
          </Text>
          <DataRow>
            <Text light>Születési dátum</Text>
            <Text dark>{seat.birth_date}</Text>
          </DataRow>
          <DataRow>
            <Text light>Személyi igazolvány száma</Text>
            <Text dark>{seat.identity_card_number}</Text>
          </DataRow>
          <DataRow>
            <Text light>Tartózkodási lakcím</Text>
            <Text strong>
              {seat.post_code} {seat.city} {seat.address_line1}
            </Text>
          </DataRow>
          <DataRow>
            <Text light>Értesítési telefonszám</Text>
            <Text dark>{seat.phone_number}</Text>
          </DataRow>
          <DataRow>
            <Text light>Értesítési e-mail cím</Text>
            <Text dark>{seat.email}</Text>
          </DataRow>
          <DataRow>
            <Text light>TAJ kártya száma</Text>
            <Text dark>{seat.healthcare_number}</Text>
          </DataRow>
        </React.Fragment>
      ))}
      <NextLinkButton toCenter to={ROUTE_PAYMENT_METHODS} />
    </View>
  );
}
