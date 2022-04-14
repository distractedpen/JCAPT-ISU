const formEl = document.getElementById("drill-form");
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


function submitForm() {
	// gather data stored in sentenceX audioX named tags

	let formData = new FormData();
	let newCounter = 0;

	sentences.forEach( (value) => {
		const oldLabelName = "sentence" + value;
		const oldAudioName = "audio" + value;

		const sentEl = document.getElementByName(oldLabelName);
		const audioEl = document.getElementByName(oldAudioName);

		const newLabelName = "sentence" + newCounter;
		const newAudioName = "audio" + newCounter;

		formData.append(newLabelName, sentEl.value);
		formData.append(newAudioName, audioEl.files[0], newAudioName+".wav");
		newCounter++;
	});

	// Send formData to service for processing!!!

}