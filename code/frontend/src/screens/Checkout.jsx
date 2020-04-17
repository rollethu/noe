import React from "react";

import { Context as SeatContext } from "../contexts/seatContext";
import { Context as AppointmentContext } from "../contexts/appointmentContext";
import { View, Caption, Text, DataRow, HR, LinkButton } from "../UI";
import { ROUTE_PAYMENT_METHODS } from "../App";

export default function Checkout() {
  const {
    state: { seats },
  } = React.useContext(SeatContext);
  const {
    state: { appointment },
  } = React.useContext(AppointmentContext);

  return (
    <View>
      <Caption center>Összegzés</Caption>
      <DataRow>
        <Text light>Regisztrált jármű</Text>
        <Text strong>{appointment.licence_plate}</Text>
      </DataRow>
      <DataRow>
        <Text light>Mintavétel időpontja</Text>
        <Text strong>
          {appointment.start} {appointment.end}
        </Text>
      </DataRow>
      <DataRow>
        <Text light>Mintavétel helyszíne</Text>
        <Text strong>{appointment.location_name}</Text>
      </DataRow>
      {seats.map((seat) => (
        <>
          <Text strong>
            {seat.full_name}
            {seat.has_doctor_referral && " - Beutalo"}
          </Text>
          <DataRow>
            <Text light>Születési dátum</Text>
            <Text strong>{seat.full_name}</Text>
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
        </>
      ))}
      <LinkButton toCenter to={ROUTE_PAYMENT_METHODS}>
        Tovább
      </LinkButton>
    </View>
  );
}
