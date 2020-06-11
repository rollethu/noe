import React, { useState } from "react";
import axios from 'axios';

import { View, Caption, Text, Image, NextButton, Button, DataRow } from "../../UI";
import { formatAppointmentDate } from "../../utils";

export default function ConfirmCancelAppointment({ locationName, licencePlate, appointment }) {
  const [isCancelled, setCancelled] = useState(false);

  const onClickCancelAppointment = async () => {
    try {
      await axios.delete(appointment.url);
    } catch (error) {
      return { error: true, errors: error?.response?.data || [] };
    }
    setCancelled(true);
  };

  let bottomPart;
  if (isCancelled) {
    bottomPart = "Regisztrációját töröltük rendszerünkből minden hozzá tartozó adattal együtt.";
  } else {
    bottomPart = (
      <>
        <Button toCenter onClick={onClickCancelAppointment}>
          Lemondás
        </Button>
        <a href="https://www.tesztallomas.hu" className="Button ToCenter Inverse">
          Vissza a főoldalra
        </a>
      </>
    );
  }

  return (
    <View>
      <Caption>Regisztráció lemondása</Caption>
      <DataRow>
        <Text light>Helyszín</Text>
        <Text dark>{locationName}</Text>
      </DataRow>
      <DataRow>
        <Text light>Regisztrált jármű</Text>
        <Text dark>{licencePlate}</Text>
      </DataRow>
      <DataRow>
        <Text light>Mintavétel időpontja</Text>
        <Text dark right>
          {formatAppointmentDate(appointment)}
        </Text>
      </DataRow>
      {bottomPart}
    </View>
  );
}
