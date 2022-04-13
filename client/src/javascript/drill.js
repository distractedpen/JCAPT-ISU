/**********************************
 * Global Variables
 **********************************/
const record = document.querySelector('.record');	
const stop = document.querySelector('.stop');
const soundClip = document.querySelector('.sound-clip');
const recText = document.querySelector('.rec-text');
const senText = document.querySelector('.sen-text');
const previous = document.querySelector('.previous');
const next = document.querySelector('.next');
const listenContainer = document.querySelector('.listen-container');
const listenBtn = document.querySelector('.listen-btn');

const drill_set_id = localStorage.getItem("drill_set");

let current_sentence = 0;

const env = {"SERVICE_HOST": "https://172.19.124.246", "SERVICE_PORT": "8000", "CLIENT_HOST": "0.0.0.0"}


/**********************************
 * API Calls
 **********************************/
function fetchText(index) {
	const payload = {
		method: "POST",
		mode: "cors",
		cache: "no-cache",
		headers: {
			"Content-Type": 'application/json',
			"Origin": `${env["CLIENT_HOST"]}`
		},
		body: JSON.stringify({
			sent_index: current_sentence
		})
	};
	fetch(`${env["SERVICE_HOST"]}:${env["SERVICE_PORT"]}/getText`, payload)
	.then( (response) => response.json() )
	.then( (json) => {
		console.log(json.sentence, json.endOfList)
	    senText.innerHTML = json.sentence;

	    if (json.endOfList)
		   	next.setAttribute('disabled', '');
		else
			next.removeAttribute('disabled');

		if (index === 0)
			previous.setAttribute('disabled', '');
		else
			previous.removeAttribute('disabled');
	 }) 
	.catch( (err) => { 
		return err; 
	});	
}

function fetchTextAudio(index) {
	const payload = {
		method: "POST",
		mode: "cors",
		cache: "no-cache",
		headers: {
			"Content-Type": 'application/json'
		},
		body: JSON.stringify({
			audiofileIndex: index,
		})
	};
	fetch(`${env["SERVICE_HOST"]}:${env["SERVICE_PORT"]}/getAudio`, payload)
	.then( (response) => response.blob())
	.then( (blob) => {
	    const r_audio = document.querySelector(".listen-audio");
	    if (r_audio !== null)
	    	listenContainer.removeChild(r_audio);

	    let audio = document.createElement("audio");
	    audio.className = "listen-audio";

	    audio.src = window.URL.createObjectURL(blob);
	    audio.setAttribute("controls", 'disabled');
	    listenContainer.appendChild(audio);

	    listenBtn.onclick = function () {
	    	audio.play();
	    }
	})
}
fetchText(current_sentence);
fetchTextAudio(current_sentence);


/********************************
 * Helper Functions
 ********************************/
function blobToFile(blob, filename) {
	blob.lastModifiedDate = new Date();
	blob.name = filename;
	return blob;
}


/********************************
 * Callbacks for Sentence Buttons
 ********************************/
previous.onclick = function() {
	current_sentence--;
	fetchText(current_sentence);
	fetchTextAudio(current_sentence);
}

next.onclick = function() {
	current_sentence++;
	fetchText(current_sentence);
	fetchTextAudio(current_sentence);
}


/********************************
 * Setup and Callbacks and API Calls
 * for Microphone and Recorded Data
 ********************************/

if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
	console.log("getUserMedia supported.");
	navigator.mediaDevices.getUserMedia (
		// constraints - only audio needed for this app
		{
			audio: true
		})

		// Success callback
		.then(function(stream) {

			const mediaRecorder = new MediaRecorder(stream);

			record.onclick = function () {
				if ( soundClip.firstChild !== null)
					soundClip.firstChild.parentNode.removeChild(soundClip.firstChild)
				mediaRecorder.start();
				console.log(mediaRecorder.state);
				console.log("recorder started");
				record.style.background = "red";
				record.style.color = "black";
			}

			let chunks = [];

			mediaRecorder.ondataavailable = function(e) {
				chunks.push(e.data);
			}

			stop.onclick = function() {
				mediaRecorder.stop();
				console.log(mediaRecorder.state);
				console.log("recorder stopped");
				record.style.background = "";
				record.style.color = "";
			}

			mediaRecorder.onstop = async function(e) {
				console.log("recorder stopped, event fired.")

				const clipName = "voice_cap" + Date.now().toString();
				const audio = document.createElement('audio');

				audio.setAttribute('controls', '');	
				soundClip.appendChild(audio);

				const blob = new Blob(chunks, { 'mimeType' : 'audio/wav; codecs="1"'});
				chunks = [];

				const audioURL = window.URL.createObjectURL(blob);
				audio.src = audioURL;

				const audioFile = blobToFile(blob, `${clipName}.ogg`);

				const payload = {
					method: "POST",
					mode: "cors",
					cache: "no-cache",
					headers: {
						"Content-Type": 'audio/ogg; codecs="opus"'
					},
					body: audioFile
				};

				const response = await fetch(`${env["SERVICE_HOST"]}:${env["SERVICE_PORT"]}/results`, payload)
					.then( (response) => { return response.json(); } )	
					.then( (data) => { return data.result } )
					.catch( (err) => { return console.error(err); } );
				console.log(response);

				const correct_aligned = response.correct;
				const result_aligned = response.result;
				const align_str = response.align_str;

				recText.innerHTML = "";
				align_str.forEach( (char, index) => {
					let charSpan = document.createElement('span');
					if (char === "-")
						charSpan.style.color = "red";
					charSpan.innerHTML = result_aligned[index];
					recText.appendChild(charSpan);
				});

			}

		})

		// Error callback
		.catch(function(err) {
			console.log("The following getUserMedia error occurred: " + err);
		}
	);
} else {
	console.log("getUserMedia not supported on your browser!");
}
