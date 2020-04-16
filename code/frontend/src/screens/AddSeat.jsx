import React from "react";

import { ROUTE_TIME, ROUTE_SEAT_DETAILS } from "../App";
import { View, Caption, Image, Text, LinkButton } from "../UI";

export default function AddSeat() {
  return (
    <View>
      <Caption center>Új személy hozzáadása</Caption>
      <Image src="https://via.placeholder.com/150" />
      <Text>
        Lehetősége van további személyeket hozzáadni, akikkel együtt jönne
        tesztelni. Felhívjuk figyelmét, hogy a fertőzésveszély minimalizálása
        érdekében, csak önnel egy háztartásban élőket regisztráljon. Egy
        regisztrációval maximum 5 személy rögzíthető.
      </Text>
      <LinkButton to={ROUTE_TIME} toCenter>
        Tovább
      </LinkButton>
      <LinkButton to={ROUTE_SEAT_DETAILS} toCenter inverse>
        Új személy hozzáadása
      </LinkButton>
    </View>
  );
}
