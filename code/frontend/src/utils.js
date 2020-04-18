export function normalizeLicencePlate(licencePlate) {
  return licencePlate.toUpperCase().replace(/[^A-Z0-9]/g, "");
}

export function handleResponse({ response, setError, history, redirectRoute }) {
  if (response.error) {
    if (response.errors) {
      Object.keys(response.errors).map((fieldName) =>
        setError(fieldName, "", response.errors[fieldName])
      );
    } else {
      alert("Váratlan hiba történt.");
    }
  } else {
    history.push(redirectRoute);
  }
}

export function getQueryParamsFromObject(params) {
  if (!params) {
    return "";
  }

  const queryString = Object.keys(params)
    .map((key) => key + "=" + params[key])
    .join("&");

  return queryString === "" ? "" : `?${queryString}`;
}
