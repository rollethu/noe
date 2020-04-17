import React from "react";

import { Context as SeatContext } from "../contexts/seatContext";
import { View, Caption } from "../UI";

export default function Checkout() {
  const {
    state: { seats },
  } = React.useContext(SeatContext);
  return (
    <View>
      <Caption>Összegzés</Caption>
      <DataRow>
        <Text light>Regisztrált jármű</Text>
        <Text strong>__LICENCE_PLATE__</Text>
      </DataRow>
      <DataRow>
        <Text light>Mintavétel időpontja</Text>
        <Text strong>__LICENCE_PLATE__</Text>
      </DataRow>
      <DataRow>
        <Text light>Mintavétel helyszíne</Text>
        <Text strong>__LICENCE_PLATE__</Text>
      </DataRow>
      {seats.map((seat) => (
        <>
          <Text>__HUMAN__</Text>
          <DataRow>
            <Text light>Születési dátum</Text>
            <Text light>__LICENCE_PLATE__</Text>
          </DataRow>
          <DataRow>
            <Text light>Személyi igazolvány száma</Text>
            <Text light>__LICENCE_PLATE__</Text>
          </DataRow>
          <DataRow>
            <Text light>Tartózkodási lakcím</Text>
            <Text light>__LICENCE_PLATE__</Text>
          </DataRow>
          <DataRow>
            <Text light>Értesítési telefonszám</Text>
            <Text light>__LICENCE_PLATE__</Text>
          </DataRow>
          <DataRow>
            <Text light>Értesítési e-mail cím</Text>
            <Text light>__LICENCE_PLATE__</Text>
          </DataRow>
          <DataRow>
            <Text light>TAJ kártya száma</Text>
            <Text light>__LICENCE_PLATE__</Text>
          </DataRow>
          <HR />
          <DataRow>
            <Text light>Fizetendő összeg</Text>
            <Text light>__LICENCE_PLATE__</Text>
          </DataRow>
        </>
      ))}
    </View>
  );
}
