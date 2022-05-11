<script setup>
import { ref, reactive, watch } from "vue";

const props = defineProps(["drillSet", "currentListeningURL", "result"]);
const emit = defineEmits(["fetchAudio", "fetchResult"]);
console.log(props.drillSet);
const state = reactive({
  prevDisabled: true,
  nextDisabled: props.drillSet.sentences.length > 1 ? false : true,
  hasAudio: false,
  isRecording: false,
  audioURL: null,
});

const currentSentence = ref(0);
let audio = ref(null);
let listen = ref(null);
let mediaRecorder = null;
let chunks = [];

watch(currentSentence, () => {
  emit("fetchAudio", props.drillSet.audio[currentSentence.value]);
  if (currentSentence.value == 0) {
    state.prevDisabled = true;
  } else {
    state.prevDisabled = false;
  }

  if (currentSentence.value == props.drillSet.sentences.length - 1) {
    state.nextDisabled = true;
  } else {
    state.nextDisabled = false;
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

        // send data to service
        blob.lastModifiedDate = new Date();
        blob.name = "voice_cap" + Date.now().toString();

        emit("fetchResult", blob, currentSentence);
      };
      console.log(mediaRecorder);
    })
    .catch(function (err) {
      console.log("The following getUserMedia error occurred: " + err);
    });
} else {
  console.log("getUserMedia not supported on your browser!");
}


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
      <button
        class="listen-btn"
        @click="() => listen.play()"
        v-if="props.currentListeningURL"
      >
        Listen
      </button>
      <audio
        ref="listen"
        :src="props.currentListeningURL"
        class="listen-audio"
        controls="disabled"
      ></audio>
    </div>
    <slot></slot>
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

.listen-container {
  display: flex;
  justify-content: center;
  align-items: center;
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
