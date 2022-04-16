const env = {"SERVICE_HOST": "https://172.19.119.223", "SERVICE_PORT": "8000", "CLIENT_HOST": "0.0.0.0"};
const containerDiv = document.querySelector(".container");
const formEl = document.getElementById("drill-form");
const nameInput = document.getElementById("nameInput");

nameInput.addEventListener("input", () => {
	nameInput.setCustomValidity('');
	nameInput.checkValidity();
})
nameInput.addEventListener("invalid", () => {
	if (nameInput.value === "") {
		nameInput.setCustomValidity("Must enter a name for this drill set.");
	}
})

let nextSentenceCount = 0;

let sentences = [];

function addSentence() {
	sentences.push(nextSentenceCount);
	const newSentenceDiv = document.createElement("div");
	newSentenceDiv.className = "new-sentence";

	const sentNumber = nextSentenceCount;
	const labelName = "sentence" + sentNumber;
	const audioName = "audio" + sentNumber;


	const deleteBtn = document.createElement("button");
	deleteBtn.textContent = "X";
	deleteBtn.className = "xbtn";
	deleteBtn.onclick = function() {
		sentences = sentences.filter((value) => value !== sentNumber);
		formEl.removeChild(deleteBtn.parentNode);
	}

	const sentenceLabel = document.createElement("label");
	sentenceLabel.innerHTML = "Sentence: "

	const sentenceInput = document.createElement("input");
	sentenceInput.name = labelName;
	sentenceInput.setAttribute("type", "text");
	sentenceInput.setAttribute("required", "");

	sentenceLabel.appendChild(sentenceInput);

	const audioLabel = document.createElement("label");
	audioLabel.innerHTML = "Audio: "

	const audioInput = document.createElement("input");
	audioInput.name = audioName;
	audioInput.setAttribute("type", "file");
	audioInput.setAttribute("accept", ".wav");

	audioLabel.appendChild(audioInput);

	newSentenceDiv.appendChild(deleteBtn);
	newSentenceDiv.appendChild(sentenceLabel);
	newSentenceDiv.appendChild(audioLabel);

	nextSentenceCount++;
	formEl.appendChild(newSentenceDiv);
	console.log(sentences);

}
addSentence();

function validateForm() {

	let valid = false;
	
	const nameInput = document.getElementById("nameInput");
	if (nameInput.value === "")
		valid = false;
	if (valid) {
		sentences.forEach( (value) => {
			const sentEl = document.getElementsByName(oldLabelName);
			if (sentEl.value === "") {
				valid = false; 
				return;
			}
		});
	};

	if (valid)
		submitForm();
}


async function submitForm() {
	// gather data stored in sentenceX audioX named tags

	let formData = new FormData();
	let newCounter = 0;

	formData.append("num_sentences", sentences.length);
	formData.append("name", nameInput.value);
	sentences.forEach( (value) => {
		const oldLabelName = "sentence" + value;
		const oldAudioName = "audio" + value;

		const sentEl = document.getElementsByName(oldLabelName);
		const audioEl = document.getElementsByName(oldAudioName);

		const newLabelName = "sentence" + newCounter;
		const newAudioName = "audio" + newCounter;



		formData.append(newLabelName, sentEl[0].value);
		formData.append(newAudioName, audioEl[0].files[0], newAudioName+".wav");
		newCounter++;
	});

	// Send formData to service for processing!!!
	const payload = {
		method: "POST",
		mode: "cors",
		cache: "no-cache",
		body: formData
	};

	const response = await fetch(`${env["SERVICE_HOST"]}:${env["SERVICE_PORT"]}/newDrillSet`, payload)
		.then( (response) => { return response.json(); } )	
		.then( (data) => { return data } )
		.catch( (err) => { return console.error(err); } );
	console.log(response);

	if (response.status === "success"){
		nameInput.value = "";

		const formTop = document.querySelector(".form-top");
		while (formEl.lastChild !== formTop) {
			formEl.removeChild(formEl.lastChild);
		}
		addSentence();
	}

	const statusText = document.createElement("p");
	statusText.innerHTML = response.status === "success" ? "Drill Created Successfully." : response.error;
	containerDiv.appendChild(statusText);

}