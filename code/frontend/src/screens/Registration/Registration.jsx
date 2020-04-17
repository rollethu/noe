import React from "react";

import RegistrationForm from "./RegistrationForm";
import ProgressBarSVG from "../../assets/progressbar_1.svg";
import { Context as LocationContext } from "../../contexts/locationContext";
import { View, Caption, Text, Image } from "../../UI";

export default function Registration() {
  const {
    state: { locations },
    fetchLocations,
  } = React.useContext(LocationContext);

  React.useEffect(() => {
    fetchLocations();
  }, []);

  if (locations === null) {
    return (
      <View>
        <Caption>Loading</Caption>
      </View>
    );
  }

  const locationOptions = locations.map((location) => ({
    text: location.name,
    value: location.url,
  }));

  return (
    <View>
      <Image src={ProgressBarSVG} />
      <Caption>Regisztráció</Caption>
      <Text>
        Válassza ki a tesztelőállomást és adja meg a gépjármű redszámát, amivel
        érkezni fog
      </Text>
      <RegistrationForm locationOptions={locationOptions} />
    </View>
  );
}
