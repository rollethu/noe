import React from "react";
import { useHistory } from "react-router-dom";
import moment from "moment";
import { Context as SeatContext } from "../contexts/seatContext";
import { Context as AppointmentContext } from "../contexts/appointmentContext";
import {
  View,
  Caption,
  Text,
  DataRow,
  HR,
  LinkButton,
  IconButton,
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

  function onSeatEditClick(seat) {
    setActiveSeat(seat);
    history.push(ROUTE_SEAT_DETAILS);
  }

  function onSeatDeleteClick(seat) {
    const confirmed = window.confirm("Biztosan törölni akarja?");
    if (!confirmed) {
      return;
    }
    deleteSeat(seat.url);
  }

  const formatAppointmentDate = () => {
    if (!appointment.start || !appointment.end) {
      return "";
    }

    const start = moment(appointment.start);
    return (
      <>
        {`${start.format("YYYY. MM. DD.")}`}
        <br />
        {`${start.format("HH:mm")}-${moment(appointment.end).format("HH:mm")}`}
      </>
    );
  };

  return (
    <View>
      <Caption center>Összegzés</Caption>
      <DataRow>
        <Text light>Regisztrált jármű</Text>
        <Text strong>{appointment.licence_plate}</Text>
      </DataRow>
      <DataRow>
        <Text light>Mintavétel időpontja</Text>
        <Text strong right>
          {formatAppointmentDate()}
        </Text>
      </DataRow>
      <DataRow>
        <Text light>Mintavétel helyszíne</Text>
        <Text strong>{appointment.location_name}</Text>
      </DataRow>
      {seats.map((seat) => (
        <React.Fragment key={seat.url}>
          <Text strong>
            {seat.full_name}
            {seat.has_doctor_referral && " - Beutalo"}
            <IconButton icon="pencil" onClick={() => onSeatEditClick(seat)} />
            <IconButton icon="close" onClick={() => onSeatDeleteClick(seat)} />
          </Text>
          <DataRow>
            <Text light>Születési dátum</Text>
            <Text strong>{seat.birth_date}</Text>
          </DataRow>
          <DataRow>
            <Text light>Személyi igazolvány száma</Text>
            <Text strong>{seat.identity_card_number}</Text>
          </DataRow>
          <DataRow>
            <Text light>Tartózkodási lakcím</Text>
            <Text strong>
              {seat.post_code} {seat.city} {seat.address_line1}
            </Text>
          </DataRow>
          <DataRow>
            <Text light>Értesítési telefonszám</Text>
            <Text strong>{seat.phone_number}</Text>
          </DataRow>
          <DataRow>
            <Text light>Értesítési e-mail cím</Text>
            <Text strong>{seat.email}</Text>
          </DataRow>
          <DataRow>
            <Text light>TAJ kártya száma</Text>
            <Text strong>{seat.healthcare_number}</Text>
          </DataRow>
          <HR />
          <DataRow>
            <Text light>Fizetendő összeg</Text>
            <Text strong>__LICENCE_PLATE__</Text>
          </DataRow>
        </React.Fragment>
      ))}
      <LinkButton toCenter to={ROUTE_PAYMENT_METHODS}>
        Tovább
      </LinkButton>
    </View>
  );
}
