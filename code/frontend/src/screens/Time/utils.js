import moment from "moment";

export function makeDateTimeFromDate(dateString) {
  let momentValue = moment();
  if (!!dateString) {
    momentValue = moment(`${dateString} ${moment().format("HH:mm:ss")}`);
  }

  return momentValue
    .toISOString(true) // Keep utc offset
    .replace(/\.[0-9]{3}/g, ""); // cut off milliseconds
}

export function getTimeSlotOptions(timeSlots) {
  if (timeSlots === null) {
    return [];
  }

  return timeSlots.map((slot) => ({
    value: slot.url,
    text: `${moment(slot.start).format("HH:mm")}-${moment(slot.end).format(
      "HH:mm"
    )}`,
  }));
}

export function updateFiltersWithDate(filters, newDate) {
  const newDateValue = makeDateTimeFromDate(newDate);

  // Filters for date, but expects an isostring to
  // determine the client's timezone
  filters.start_date = newDateValue;
}
