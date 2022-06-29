const SERVICE_HOST = import.meta.env.VITE_SERVICE_HOST;
const SERVICE_PORT = import.meta.env.VITE_SERVICE_PORT;
const SERVICE_URL = `https://${SERVICE_HOST}:${SERVICE_PORT}`;

function addAuth() {
  const user = JSON.parse(localStorage.getItem("user"));

  if (user && user.token) {
    return "JWT " + user.token;
  } else {
    return "";
  }
}

async function login(body) {
  const payload = {
    method: "POST",
    mode: "cors",
    cache: "no-cache",
    headers: {
      "Content-Type": "application/json",
    },
    body: body,
  };

  try {
    const response = await fetch(`${SERVICE_URL}/login`, payload).then(
      (response) => response.json()
    );

    return response;
  } catch (error) {
    console.error(error);
  }
}

async function jsonAPI(endpoint, body) {
  const payload = {
    method: "POST",
    mode: "cors",
    cache: "no-cache",
    headers: {
      "Content-Type": "application/json",
      Authorization: addAuth(),
    },
    body: body,
  };

  try {
    const response = await fetch(`${SERVICE_URL}/${endpoint}`, payload).then(
      (response) => response.json()
    );

    return response;
  } catch (error) {
    console.error(error);
  }
}

async function blobAPI(endpoint, body) {
  const payload = {
    method: "POST",
    mode: "cors",
    cache: "no-cache",
    headers: {
      "Content-Type": "application/json",
      Authorization: addAuth(),
    },
    body: body,
  };

  try {
    const response = await fetch(`${SERVICE_URL}/${endpoint}`, payload).then(
      (response) => response.blob()
    );
    return response;
  } catch (error) {
    console.error(error);
  }
}

async function formDataAPI(endpoint, formdata) {
  const payload = {
    method: "POST",
    mode: "cors",
    cache: "no-cache",
    headers: {
      Authorization: addAuth(),
    },
    body: formdata,
  };

  try {
    const response = await fetch(`${SERVICE_URL}/${endpoint}`, payload).then(
      (response) => response.json()
    );
    return response;
  } catch (error) {
    console.error(error);
  }
}

export default {
  login,
  jsonAPI,
  blobAPI,
  formDataAPI,
};
