import React from "react";

import AddSeatSVG from "../assets/add_person.svg";
import { Context as SeatContext } from "../contexts/seatContext";
import { ROUTE_TIME, ROUTE_SEAT_DETAILS } from "../App";
import { View, Caption, Image, Text, NextLinkButton, Button } from "../UI";
import { useHistory } from "react-router-dom";

export default function AddSeat() {
  const history = useHistory();
  const { setActiveSeat } = React.useContext(SeatContext);

  function onNewSeatClick() {
    setActiveSeat(null);
    history.push(ROUTE_SEAT_DETAILS);
  }

  return (
    <View>
      <Caption center>Új személy hozzáadása</Caption>
      <Image src={AddSeatSVG} />
      <Text>
        Lehetősége van további személyeket hozzáadni, akikkel együtt jönne
        tesztelni. Felhívjuk figyelmét, hogy a fertőzésveszély minimalizálása
        érdekében, csak önnel egy háztartásban élőket regisztráljon. Egy
        regisztrációval maximum 5 személy rögzíthető.
      </Text>
      <NextLinkButton to={ROUTE_TIME} toCenter />
      <Button onClick={onNewSeatClick} toCenter inverse>
        Új személy hozzáadása
      </Button>
    </View>
  );
}
