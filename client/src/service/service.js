console.log(import.meta.env);

const SERVICE_HOST = import.meta.env.VITE_SERVICE_HOST;
const SERVICE_PORT = import.meta.env.VITE_SERVICE_PORT;
const SERVICE_URL = `https://${SERVICE_HOST}:${SERVICE_PORT}`;

async function jsonAPI(endpoint, body) {
  const payload = {
    method: "POST",
    mode: "cors",
    cache: "no-cache",
    headers: {
      "Content-Type": "application/json",
    },
    body: body,
  };

  const response = await fetch(`${SERVICE_URL}/${endpoint}`, payload)
    .then((response) => response.json())
    .catch((error) => {
      return { status: "error", message: error };
    });

  return response;
}

async function blobAPI(endpoint, body) {
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
    const response = await fetch(`${SERVICE_URL}/${endpoint}`, payload).then(
      (response) => response.blob()
    );
    return response;
  } catch (error) {
    console.error(error);
  }
}

// export default {
//   fetchDrillSets,
// };
// function fetchDrillSet(drillSetId) {
//   const payload = {
//     method: "POST",
//     mode: "cors",
//     cache: "no-cache",
//     headers: {
//       "Content-Type": 'application/json',
//     },
//     body: JSON.stringify({
//       drill_set_id: drillSetId
//     })
//   };
//   fetch(`${env["SERVICE_HOST"]}:${env["SERVICE_PORT"]}/getDrillSet`, payload)
//   .then( (response) => response.json())
//   .then( (json) => {
//     drillSet = json.drillSet;
//     fetchAudio(drillSetId, drillSet.audio[current_sentence]);
//     senText.innerHTML = drillSet.sentences[current_sentence];
//    })
//   .catch( (err) => {
//     console.log(err);
//   });
// }

// function fetchAudio(drillSetId, fileName) {
//   const payload = {
//     method: "POST",
//     mode: "cors",
//     cache: "no-cache",
//     headers: {
//       "Content-Type": 'application/json'
//     },
//     body: JSON.stringify({
//       drillSetId: drillSetId,
//       fileName: fileName,
//     })
//   };
//   fetch(`${env["SERVICE_HOST"]}:${env["SERVICE_PORT"]}/getAudio`, payload)
//   .then( (response) => response.blob())
//   .then( (blob) => {
//       const r_audio = document.querySelector(".listen-audio");
//       if (r_audio !== null)
//         listenContainer.removeChild(r_audio);

//       let audio = document.createElement("audio");
//       audio.className = "listen-audio";

//       audio.src = window.URL.createObjectURL(blob);
//       audio.setAttribute("controls", 'disabled');
//       listenContainer.appendChild(audio);

//       listenBtn.onclick = function () {
//         audio.play();
//       }
//   })
// }

// payload = {
//   method: "POST",
//   mode: "cors",
//   cache: "no-cache",
//   body: formData,
// };
// const response = await fetch(
//   `${env["SERVICE_HOST"]}:${env["SERVICE_PORT"]}/results`,
//   payload
// )
//   .then((response) => {
//     return response.json();
//   })
//   .then((data) => {
//     return data.result;
//   })
//   .catch((err) => {
//     return console.error(err);
//   });

export default {
  jsonAPI,
  blobAPI,
};
