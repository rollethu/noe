export async function handleRequest(requestCreator) {
  let response;
  try {
    response = await requestCreator();
    response.error = false;
  } catch (error) {
    if (!error.response) {
      return { error: true };
    }
    response = error.response;
    setErrorFlagsOnResponse(response);
  }
  return response;
}

function setErrorFlagsOnResponse(response) {
  response.error = true;
  response.errors = response.data;
}

export function addStateToLocalStorage(state) {
  localStorage.setItem("tesztallomasState", JSON.stringify(state));
}
