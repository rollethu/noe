import React from "react";
import { useHistory } from "react-router-dom";
import _ from "lodash";

import ProgressBarSVG from "../../assets/progressbar_4.svg";
import { Context as TimeSlotContext } from "../../contexts/timeSlotContext";
import { Context as AppointmentContext } from "../../contexts/appointmentContext";
import { Context as SeatContext } from "../../contexts/seatContext";
import { ROUTE_CHECKOUT } from "../../App";
import { View, Caption, Text, Image } from "../../UI";
import TimeForm from "./TimeForm";
import * as utils from "../../utils";
import * as timeUtils from "./utils";
import moment from "moment";

export default function Time() {
  const history = useHistory();

  const {
    state: { appointment },
    updateAppointment,
  } = React.useContext(AppointmentContext);
  const {
    state: { seats },
  } = React.useContext(SeatContext);
  const {
    state: { timeSlots },
    fetchTimeSlots,
  } = React.useContext(TimeSlotContext);

  const filters = { location: null, min_availability: seats.length };
  if (appointment) {
    filters.location = utils.getResourceUuidFromUrl(appointment.locationUrl);
  }

  const onSubmit = async (values, setError) => {
    delete values.date;
    if (!appointment.url) {
      alert("No appointment to update");
      return;
    }

    const response = await updateAppointment(appointment.url, values);
    utils.handleResponse({
      response,
      setError,
      history,
      redirectRoute: ROUTE_CHECKOUT,
    });
  };

  function onDateChange(newDate) {
    if (!moment(newDate).isValid()) {
      return;
    }

    timeUtils.updateFiltersWithDate(filters, newDate);
    fetchTimeSlots(filters);
  }
  onDateChange = _.debounce(onDateChange, 1000);

  React.useEffect(() => {
    timeUtils.updateFiltersWithDate(filters, null);
    fetchTimeSlots(filters);
  }, []);

  return (
    <View>
      <Image src={ProgressBarSVG} />
      <Caption>Időpont foglalás</Caption>
      <Text>
        Válassza ki a mintavétel időpontját. A forgalmi rend fenntartása érdekében kérjük, hogy max. 10 perccel
        korábban érkezzen a helyszínre.
      </Text>
      <TimeForm
        onSubmit={onSubmit}
        appointment={appointment}
        timeSlots={timeSlots}
        fetchTimeSlots={fetchTimeSlots}
        onDateChange={onDateChange}
      />
    </View>
  );
}
