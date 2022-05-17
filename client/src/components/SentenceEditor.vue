<script setup>
const props = defineProps(["index", "sentence", "audioURL"]);
const emit = defineEmits([
  "deleteRequest",
  "onSentenceChange",
  "onAudioChange",
]);
</script>

<template>
  <div>
    <button @click="emit('deleteRequest', props.index)">X</button>
    <label>
      Sentence:
      <input
        type="text"
        :value="sentence"
        @change="
          (event) => emit('onSentenceChange', props.index, event.target.value)
        "
      />
    </label>
    <label
      >Audio File:
      <input
        type="file"
        accept=".wav"
        @change="
          (event) => emit('onAudioChange', props.index, event.target.files[0])
        "
    /></label>
    <audio :v-if="audioURL" :src="audioURL" controls></audio>
  </div>
</template>

<style></style>
