<script setup>
import DrillManager from "../components/DrillManager.vue";
import DrillEditor from "../components/DrillEditor.vue";
import PageHeader from "../components/PageHeader.vue";
import { reactive, ref } from "vue";
import service from "../service/service.js";

const state = reactive({
  routeFrom: "admin",
  validSelection: false,
  isNewDrillSet: false,
  drillSet: {},
  drillSetAudioFiles: {},
  listeningURLs: {},
});

const resetState = () => {
  state.routeFrom = "admin";
  state.validSelection = false;
  state.isNewDrillSet = false;
  state.drillSet = {};
  state.drillSetAudioFiles = {};
  state.listeningURLs = {};
};

const statusRef = ref(null);
const messageTimeOut = (type, message) => {
  statusRef.value.innerHTML = message;
  statusRef.value.style.color = type === "error" ? "red" : "black";
  setTimeout(() => {
    statusRef.value.innerHTML = "";
    statusRef.value.style.color = "black";
  }, 2000);
};

const getDrillSet = (drillSet) => {
  state.drillSet = drillSet;
  if (
    state.drillSet &&
    Object.keys(state.drillSet).length === 0 &&
    Object.getPrototypeOf(state.drillSet) === Object.prototype
  ) {
    state.isNewDrillSet = true;
  }
  state.validSelection = true;
};

const onNameChange = (newName) => {
  state.drillSet.name = newName;
};

const onSentenceChange = (index, newText) => {
  state.drillSet.sentences[index] = newText;
};

const onAudioChange = (index, audioFile) => {
  state.drillSetAudioFiles[index] = audioFile;
  state.listeningURLs[index] = window.URL.createObjectURL(audioFile);
};

const deleteSentence = (index) => {
  if (Object.keys(state.listeningURLs).find((key) => key === index)) {
    delete state.listeningURLs[index];
  }
  if (Object.keys(state.drillSetAudioFiles).find((key) => key === index)) {
    delete state.drillSetAudioFiles[index];
  }
  state.drillSet.sentences.splice(index, 1);
  state.drillSet.audio.splice(index, 1);
};

const addSentence = () => {
  if (!state.drillSet.sentences) {
    state.drillSet.sentences = [];
    state.drillSet.audio = [];
  }
  state.drillSet.sentences.push("");
  state.drillSet.audio.push(null);
};

const saveDrillSet = () => {
  let formData = new FormData();

  formData.append("num_sentences", state.drillSet.sentences.length);
  formData.append("name", state.drillSet.name);
  state.drillSet.sentences.forEach((sentence, index) => {
    formData.append(`sentence${index}`, sentence);
    formData.append(
      `audio${index}`,
      state.drillSetAudioFiles[index],
      `audio${index}.wav`
    );
  });

  if (state.isNewDrillSet) {
    fetchCreate(formData);
  } else {
    fetchUpdate(formData);
  }
};

const deleteDrillSet = () => {
  if (confirm("This process cannot be undone. Delete this Drill Set?")) {
    fetchDelete();
  }
};

const fetchCreate = async (formData) => {
  const response = service.formDataAPI("newDrillSet", formData);
  response.then((json) => {
    if (json.status == "success") {
      messageTimeOut("success", "Drill Set created successfully");
      resetState();
    } else {
      messageTimeOut("error", "An Error has occured");
    }
  });
};

const fetchUpdate = async (formData) => {
  const response = service.formDataAPI("updateDrillSet", formData);
  response.then((json) => {
    if (json.status == "success") {
      messageTimeOut("success", "Drill Set updated successfully");
      resetState();
    } else {
      messageTimeOut("error", "An Error has occured");
    }
  });
};

const fetchDelete = async () => {
  const response = service.jsonAPI(
    "deleteDrillSet",
    JSON.stringify({ drillSetId: state.drillSet.id })
  );
  response.then((json) => {
    if (json.status === "success") {
      messageTimeOut("success", "Drill Set deleted successfully");
      resetState();
    } else {
      messageTimeOut("error", "An Error has occured");
    }
  });
};

const fetchAudio = async (drillSetId, index, fileName) => {
  const blob = await service.blobAPI(
    "getAudio",
    JSON.stringify({
      drillSetId: drillSetId,
      fileName: fileName,
    })
  );
  state.drillSetAudioFiles[index] = blob;
  state.listeningURLs[index] = window.URL.createObjectURL(blob);
};
</script>

<template>
  <PageHeader />
  <div class="container">
    <DrillManager
      v-if="!state.validSelection"
      :routeFrom="state.routeFrom"
      @getDrill="(drillset) => getDrillSet(drillset)"
    />

    <!--DrillViewer gets drill set data from DrillSelector-->
    <DrillEditor
      v-if="state.validSelection"
      :drillSet="state.drillSet"
      :listeningURLs="state.listeningURLs"
      @fetchAudio="
        (index, fileName) => fetchAudio(state.drillSet.id, index, fileName)
      "
      @deleteRequest="(index) => deleteSentence(index)"
      @onSentenceChange="(ind, newText) => onSentenceChange(ind, newText)"
      @onAudioChange="(ind, audioFile) => onAudioChange(ind, audioFile)"
      @addSentence="addSentence"
      @saveDrillSet="saveDrillSet"
      @deleteDrillSet="deleteDrillSet"
      @onNameChange="(newName) => onNameChange(newName)"
    >
    </DrillEditor>
    <p ref="statusRef"></p>
  </div>
</template>

<style>
@import "@/assets/style.css";
</style>
