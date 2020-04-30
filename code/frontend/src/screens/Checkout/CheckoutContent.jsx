import React from "react";
import {
  View,
  Caption,
  Text,
  DataRow,
  IconButton,
  NextLinkButton,
  Button,
} from "../../UI";
import * as checkoutUtils from "./utils";
import { ROUTE_PAYMENT_METHODS } from "../../App";

export default function CheckoutContent({
  appointment,
  seats,
  onSeatEditClick,
  onSeatDeleteClick,
  selectedTimeSlot,
  onNewSeatClick,
  isAddSeatDisabled,
}) {
  const shouldShowDeleteButtons = checkoutUtils.canDeleteSeat(seats);

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
          {checkoutUtils.formatAppointmentDate(selectedTimeSlot)}
        </Text>
      </DataRow>
      <DataRow>
        <Text light>Mintavétel helyszíne</Text>
        <Text dark>{appointment.location_name}</Text>
      </DataRow>
      {seats.map((seat) => (
        <div className="CheckoutSeat" key={seat.url}>
          <Text strong style={{ marginBottom: 0 }}>
            {seat.full_name}
            {seat.has_doctor_referral && " - Beutalo"}
            <IconButton icon="pencil" onClick={() => onSeatEditClick(seat)} />
            {shouldShowDeleteButtons && (
              <IconButton
                icon="close"
                onClick={() => onSeatDeleteClick(seat)}
              />
            )}
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
            <Text dark>
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
        </div>
      ))}
      <NextLinkButton toCenter to={ROUTE_PAYMENT_METHODS} />
      <Button
        id="AddSeatButton"
        onClick={onNewSeatClick}
        toCenter
        inverse
        disabled={isAddSeatDisabled}
      >
        Új személy hozzáadása
      </Button>
    </View>
  );
}
