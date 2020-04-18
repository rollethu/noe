import React from "react";
import { useForm } from "react-hook-form";
import { useHistory } from "react-router-dom";
import moment from "moment";

import { ROUTE_CHECKOUT } from "../../App";
import { Context as TimeSlotContext } from "../../contexts/timeSlotContext";
import { Context as AppointmentContext } from "../../contexts/appointmentContext";
import { Form, Field, Button } from "../../UI";
import * as utils from "../../utils";

const DATETIME_FORMAT = "YYYY-MM-DD HH:mm";

export default function TimeForm() {
  const {
    state: { timeSlots },
    fetchTimeSlots,
  } = React.useContext(TimeSlotContext);

  const timeSlotOptions = getTimeSlotOptions(timeSlots);
  const history = useHistory();
  const { register, handleSubmit, setError, errors, watch } = useForm();
  const {
    state: { appointment },
    updateAppointment,
  } = React.useContext(AppointmentContext);

  const selectedDate = watch("date") || null;

  React.useEffect(() => {
    const filters = {};
    if (selectedDate) {
      filters.start_date = selectedDate;
    } else {
      filters.start_date = moment().format("YYYY-MM-DD");
    }

    fetchTimeSlots(filters);
  }, [selectedDate]);

  const onSubmit = async (values) => {
    if (!appointment.url) {
      alert("No appointment to update");
      return;
    }

    values.start = moment(
      `${values.date} ${values.time}`,
      DATETIME_FORMAT
    ).toISOString();
    values.end = values.start;

    const response = await updateAppointment(appointment.url, values);
    utils.handleResponse({
      response,
      setError,
      history,
      redirectRoute: ROUTE_CHECKOUT,
    });
  };

  return (
    <Form onSubmit={handleSubmit(onSubmit)}>
      <Field
        register={register}
        name="date"
        label="Nap kiválasztása"
        type="date"
        defaultValue={moment().format("YYYY-MM-DD")}
        errors={errors}
      />
      <Field
        register={register}
        name="time"
        label="Idősáv kiválasztása"
        type="select"
        errors={errors}
        options={timeSlotOptions}
      />
      <Field
        register={register}
        name="promiseToCome"
        label="Vállalom, hogy megjelenek a kiválasztott időpontban"
        type="checkbox"
        errors={errors}
        required
      />
      <Button type="submit">Tovább</Button>
    </Form>
  );
}

function getTimeSlotOptions(timeSlots) {
  if (timeSlots === null) {
    return [];
  }

  return timeSlots.map((slot) => ({
    value: slot.url,
    text: `${moment(slot.start).format("HH:mm")}-${moment(slot.end).format(
      "HH:mm"
    )} (${slot.usage}/${slot.capacity})`,
  }));
}
