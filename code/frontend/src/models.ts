import moment from "moment";

export interface Appointment {
  url: string;
  createdAt: moment.Moment;
  email: string;
  gtc: string;
  privacyPolicy: string;
  locationUrl: string;
  licencePlate: string;
  normalizedLicencePlate: string;
  start: moment.Moment | null;
  end: moment.Moment | null;
  isRegistrationCompleted: boolean;
  timeSlotUrl: string | null;
  totalPrice?: number;
  currency?: string;
  isEmailVerified?: boolean;
}

export function jsonToAppointment(jsonObj: any): Appointment {
  return {
    url: jsonObj.url,
    createdAt: moment(jsonObj.created_at),
    email: jsonObj.email,
    gtc: jsonObj.gtc,
    privacyPolicy: jsonObj.privacy_policy,
    locationUrl: jsonObj.location || "",
    licencePlate: jsonObj.licence_plate,
    normalizedLicencePlate: jsonObj.normalized_licence_plate,
    start: jsonObj.start ? moment(jsonObj.start) : null,
    end: jsonObj.end ? moment(jsonObj.end) : null,
    isRegistrationCompleted: jsonObj.is_registration_completed,
    timeSlotUrl: jsonObj.time_slot,
    isEmailVerified: jsonObj.isEmailVerified,
  };
}
