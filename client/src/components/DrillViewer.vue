<script setup>
import { ref, reactive, watch } from "vue";

const currentSentence = ref(0);

const props = defineProps(["drillSet"]);
const state = reactive({
  prevDisabled: true,
  nextDisabled: false,
  hasAudio: false,
  isRecording: false,
  audioURL: null,
});

let audio = ref(null);
let mediaRecorder = null;
let chunks = [];
// function blobToFile(blob, filename) {
//   blob.lastModifiedDate = new Date();
//   blob.name = filename;
//   return blob;
// }

watch(currentSentence, () => {
  if (currentSentence.value == 0) {
    state.prevDisabled = true;
    state.nextDisabled = false;
  } else if (0 < currentSentence.value < props.drillSet.length) {
    state.prevDisabled = false;
    state.nextDisabled = false;
  } else {
    // end of list
    state.prevDisabled = false;
    state.nextDisabled = true;
  }
});

/********************************
 * Setup and Callbacks and API Calls
 * for Microphone and Recorded Data
 ********************************/

if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
  console.log("getUserMedia supported.");
  navigator.mediaDevices
    .getUserMedia({ audio: true })
    .then((stream) => {
      mediaRecorder = new MediaRecorder(stream);
      mediaRecorder.onstart = () => (state.isRecording = true);
      mediaRecorder.ondataavailable = (e) => chunks.push(e.data);
      mediaRecorder.onstop = async () => {
        state.isRecording = false;
        const blob = new Blob(chunks, { mimeType: "audio/ogg; codecs=opus" });
        chunks = [];
        state.audioURL = window.URL.createObjectURL(blob);
        state.hasAudio = true;
        audio.value.src = state.audioURL;
        audio.value.controls = true;
      };
      console.log(mediaRecorder);
    })
    .catch(function (err) {
      console.log("The following getUserMedia error occurred: " + err);
    });
} else {
  console.log("getUserMedia not supported on your browser!");
}

// const audioFile = blobToFile(blob, `${clipName}.ogg`);

// const formData = new FormData();
// formData.append("id", drillSetId);
// formData.append("index", current_sentence);
// formData.append("audio", audioFile);

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

// const correct_aligned = response.correct;
// const result_aligned = response.result;
// const align_str = response.align_str;

// recText.innerHTML = "";
// align_str.forEach((char, index) => {
//   let charSpan = document.createElement("span");
//   if (char === "-") charSpan.style.color = "red";
//   charSpan.innerHTML = result_aligned[index];
//   recText.appendChild(charSpan);
// });
//   };
// })

function startRecord() {
  mediaRecorder.start();
}

function stopRecord() {
  mediaRecorder.stop();
}
</script>

<template>
  <div class="container">
    <div class="text-container">
      <button
        class="previous"
        @click="currentSentence--"
        :disabled="state.prevDisabled"
      >
        &lt;
      </button>
      <p class="sen-text">
        {{ props.drillSet.sentences[currentSentence] }}
      </p>
      <button
        class="next"
        @click="currentSentence++"
        :disabled="state.nextDisabled"
      >
        &gt;
      </button>
    </div>
    <div class="listen-container">
      <button class="listen-btn">Listen</button>
    </div>
    <p class="rec-text">
      Press Record and Start Speaking. Press Stop to Send Recording to Service.
    </p>
    <audio ref="audio" :class="{ hidden: !state.hasAudio }"></audio>
    <div class="audio-controls">
      <button :class="{ recording: state.isRecording }" @click="startRecord">
        Record
      </button>
      <button @click="stopRecord">Stop</button>
    </div>
  </div>
</template>

<style>
* {
  box-sizing: border-box;
}

body {
  background-color: #aaa;
}

h1 {
  font-size: 32px;
}

button {
  background-color: #eee;
  border: none;
  font-size: 24px;
  width: 100px;
  height: 50px;
  margin: 10px;
  flex-shrink: 1;
}

.next {
  width: 50px;
  height: 50px;
}

.previous {
  width: 50px;
  height: 50px;
}

.page-header {
  display: flex;
  justify-content: center;
  align-items: center;
}

.container {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.sound-clip {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 50px;
  width: 100%;
}

.text-container {
  display: flex;
  flex-direction: row;
  align-items: center;
}

.sen-text {
  font-size: 20px;
  margin: 10px;
}

.listen-audio {
  visibility: hidden;
  position: absolute;
}

.recording {
  background: red;
}

.hidden {
  visibility: hidden;
}
</style>
