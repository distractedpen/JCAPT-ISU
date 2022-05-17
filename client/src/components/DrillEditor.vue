<script setup>
import { computed } from "vue";
import SentenceEditor from "./SentenceEditor.vue";

const props = defineProps(["drillSet", "listeningURLs"]);
const emit = defineEmits([
  "fetchAudio",
  "deleteRequest",
  "onSentenceChange",
  "onAudioChange",
  "addSentence",
  "saveDrillSet",
  "deleteDrillSet",
  "onNameChange",
]);

const computed_drillSet = computed(() => {
  return { ...props.drillSet };
});

if (
  props.drillSet &&
  Object.keys(props.drillSet).length === 0 &&
  Object.getPrototypeOf(props.drillSet) === Object.prototype
) {
  emit("addSentence");
} else {
  let index = 0;
  props.drillSet.audio.forEach((fileName) => {
    emit("fetchAudio", index++, fileName);
  });
}
</script>

<template>
  <div class="container">
    <label
      >Name:
      <input
        type="text"
        :value="computed_drillSet.name"
        @change="(event) => emit('onNameChange', event.target.value)"
        required
    /></label>
    <template v-for="index in computed_drillSet.sentences.length" :key="index">
      <SentenceEditor
        :index="index - 1"
        :sentence="computed_drillSet.sentences[index - 1]"
        :audioURL="props.listeningURLs[index - 1]"
        @deleteRequest="(ind) => emit('deleteRequest', ind)"
        @onSentenceChange="
          (ind, newText) => emit('onSentenceChange', ind, newText)
        "
        @onAudioChange="
          (ind, audioFile) => emit('onAudioChange', ind, audioFile)
        "
      />
    </template>
    <button @click="emit('addSentence')">Add Sentence</button>
    <button @click="emit('saveDrillSet')">Save Drill Set</button>
    <button
      class="delBtn"
      v-if="computed_drillSet.id"
      @click="emit('deleteDrillSet')"
    >
      Delete Drill Set
    </button>
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

.delBtn {
  background-color: red;
  border: none;
  font-size: 18px;
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

.container {
  display: flex;
  flex-direction: column;
  text-align: center;
  align-items: center;
  padding: 20px;
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
</style>
