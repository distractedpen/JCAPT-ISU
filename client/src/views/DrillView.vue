<script setup>
/**********************************
 * Global Variables
 **********************************/
import DrillSelector from "../components/DrillSelector.vue";
import DrillViewer from "../components/DrillViewer.vue";
import { reactive, ref } from "vue";
import service from "../service/service.js";

const resultText = ref(null);

const state = reactive({
  drillSetId: null,
  drillSet: null,
  drillSetList: [],
  validSelection: false,
  currentListeningURL: "",
  hasResult: false,
  result: {},
});

const fetchDrillSets = async () => {
  const json = service.jsonAPI("getDrillSets", {});
  json.then((data) => {
    state.drillSetList = data.drill_sets;
  });
};
fetchDrillSets();

const fetchDrillSet = async (drillSetId) => {
  state.drillSetId = drillSetId;
  const json = service.jsonAPI(
    "getDrillSet",
    JSON.stringify({ drill_set_id: drillSetId })
  );
  json.then((data) => {
    state.drillSet = data.drillSet;
    state.validSelection = true;
    fetchAudio(drillSetId, data.drillSet.audio[0]);
  });
};

const fetchAudio = async (drillSetId, fileName) => {
  const blob = service.blobAPI(
    "getAudio",
    JSON.stringify({ drillSetId: drillSetId, fileName: fileName })
  );
  blob.then((blob) => {
    console.log(blob);
    state.currentListeningURL = window.URL.createObjectURL(blob);
  });
};

const fetchResult = async (drillSetId, audio, currentSentence) => {
  const formData = new FormData();
  formData.append("id", drillSetId);
  formData.append("index", currentSentence.value);
  formData.append("audio", audio);
  const json = service.formDataAPI("results", formData);
  json.then((data) => {
    state.hasResult = true;
    const result = data.result;
    let resultHTML = "";
    result.align_str.forEach((char, index) => {
      if (char === "-") resultHTML += "<span style='color: red'>";
      else resultHTML += "<span>";
      resultHTML += result.result[index];
      resultHTML += "</span>";
    });

    resultText.value.innerHTML = resultHTML;
  });
};
</script>

<template>
  <div class="page-header">
    <h1>Voice Recognition in Japanese with Vosk</h1>
  </div>

  <!--Send drill set list to DrillSelector component-->
  <DrillSelector
    v-if="!state.validSelection || !state.drillSet"
    :drillSetList="state.drillSetList"
    @selectDrillSet="(drillSetId) => fetchDrillSet(drillSetId)"
  />

  <!--DrillViewer gets drill set data from DrillSelector-->
  <DrillViewer
    v-if="state.validSelection && state.drillSet"
    :drillSet="state.drillSet"
    :currentListeningURL="state.currentListeningURL"
    :result="state.result"
    @fetchAudio="(filename) => fetchAudio(state.drillSetId, filename)"
    @fetchResult="
      (audio, currentSentence) =>
        fetchResult(state.drillSetId, audio, currentSentence)
    "
  >
    <p ref="resultText">
      Press Record and Start Speaking. Press Stop to Send Recording to Service.
    </p>
  </DrillViewer>
</template>

<style>
@import "@/assets/style.css";
</style>
