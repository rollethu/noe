import React from 'react';
import { useForm } from 'react-hook-form';
import { Redirect } from 'react-router-dom';

import ProgressBarSVG from '../assets/progressbar_1.svg';
import { Context as LocationContext } from '../contexts/locationContext';
import { Context as AppointmentContext } from '../contexts/appointmentContext';
import { ROUTE_SEAT_DETAILS } from '../App';
import { View, Caption, Form, Field, Button, Text, Image } from '../UI';

const TXT_LOCATION = 'Helyszín';
const TXT_LICENCE_PLATE = 'Rendszám';
const TXT_SUBMIT_BUTTON = 'Tovább';

export default function Registration() {
  const [redirectTo, setRedirectTo] = React.useState(null);
  const { register, handleSubmit, setError, errors } = useForm();
  const {
    state: { appointment },
    updateAppointment,
  } = React.useContext(AppointmentContext);
  const {
    state: { locations },
    fetchLocations,
  } = React.useContext(LocationContext);

  const onSubmit = async (values) => {
    let appointmentUrl = appointment.url;
    if (process.env.NODE_ENV === 'development') {
      appointmentUrl =
        'http://localhost:8000/api/appointments/54d027ec-3f32-49d8-91d1-d5a1ea2ad5c8/';
    }
    if (!appointmentUrl) {
      alert('No appointment to update');
    }

    const response = await updateAppointment(appointmentUrl, values);
    if (response.error) {
      if (response.errors) {
        Object.keys(response.errors).map((fieldName) => {
          setError(fieldName, '', response.errors[fieldName]);
        });
      } else {
        alert('Váratlan hiba történt.');
      }
    } else {
      setRedirectTo(ROUTE_SEAT_DETAILS);
    }
  };

  React.useEffect(() => {
    fetchLocations();
  }, []);

  if (redirectTo) {
    return <Redirect to={redirectTo} />;
  }

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
      <Form onSubmit={handleSubmit(onSubmit)}>
        <Field
          register={register}
          name="location"
          label={TXT_LOCATION}
          type="select"
          errors={errors}
          options={locationOptions}
        />
        <Field
          register={register}
          name="licence_plate"
          label={TXT_LICENCE_PLATE}
          type="text"
          errors={errors}
        />
        <Button type="submit">{TXT_SUBMIT_BUTTON}</Button>
      </Form>
    </View>
  );
}
