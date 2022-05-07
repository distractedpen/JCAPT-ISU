// function fetchDrillSets() {
//   const payload = {
//     method: "POST",
//     mode: "cors",
//     cache: "no-cache",
//     headers: {
//       "Content-Type": "application/json",
//     },
//   };
//   fetch(`${env["SERVICE_HOST"]}:${env["SERVICE_PORT"]}/getDrillSets`, payload)
//     .then((response) => response.json())
//     .then((json) => {
//       const drillSets = json.drill_sets;
//       console.log(drillSets);
//       drillSets.forEach((drillset) => {
//         console.log(drillset);
//         const optionEl = document.createElement("option");
//         optionEl.value = drillset["id"];
//         optionEl.textContent = drillset["name"];
//         selectEl.appendChild(optionEl);
//       });
//     })
//     .catch((err) => {
//       console.log(err);
//       return err;
//     });
// }

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