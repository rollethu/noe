import React from "react";
import { useHistory } from "react-router-dom";

import * as utils from "../../utils";
import { ROUTE_SEAT_DETAILS, ROUTE_CHECKOUT } from "../../App";
import { Context as AppointmentContext } from "../../contexts/appointmentContext";
import { Context as LocationContext } from "../../contexts/locationContext";
import RegistrationForm from "./RegistrationForm";
import ProgressBarSVG from "../../assets/progressbar_1.svg";
import { View, Caption, Text, Image } from "../../UI";

export default function Registration() {
  const history = useHistory();
  const {
    state: { appointment },
    updateAppointment,
  } = React.useContext(AppointmentContext);
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

  const onSubmit = async (values, setError) => {
    if (!appointment.url) {
      alert("No appointment to update");
      return;
    }

    const response = await updateAppointment(appointment.url, values);
    utils.handleResponse({
      response,
      setError,
      history,
      redirectRoute: ROUTE_SEAT_DETAILS,
    });
  };

  return (
    <View>
      <Image src={ProgressBarSVG} />
      <Caption>Regisztráció</Caption>
      <Text>Válassza ki a tesztelőállomást és adja meg a gépjármű rendszámát, amivel érkezni fog</Text>
      <RegistrationForm locationOptions={locationOptions} onSubmit={onSubmit} appointment={appointment} />
    </View>
  );
}
