export function handleResponse({ response, setError, history, redirectRoute }) {
  if (response.error) {
    if (response.status !== 500 && response.errors) {
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

export function getResourceUuidFromUrl(url) {
  if (!url) {
    return null;
  }
  const parts = url.split("/");
  const uuid =
    parts[parts.length - 1] === ""
      ? parts[parts.length - 2] // due to trailing slash, last `part` is ""
      : parts[parts.length - 1];
  return uuid;
}
