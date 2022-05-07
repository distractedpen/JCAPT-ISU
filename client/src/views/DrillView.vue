<script setup>
/**********************************
 * Global Variables
 **********************************/
import DrillSelector from "../components/DrillSelector.vue";
import DrillViewer from "../components/DrillViewer.vue";
import { reactive } from "vue";
// import service from "../service/service.js";

// const env = {"SERVICE_HOST": "https://172.19.122.255", "SERVICE_PORT": "8000", "CLIENT_HOST": "0.0.0.0"};
// const selectEl = document.getElementById("drill-select");

/**********************
 * Setup for page
 **********************/

// Get chosen data from DrillSector, send correct drill set to Drill Viewer
const drillSetList = [
  { id: "1", name: "Set 1" },
  { id: "2", name: "Set 2" },
];

const drillSets = {
  1: {
    name: "Set 1",
    sentences: ["Sentence 1 Set 1", "Sentence 2 Set 1"],
    audio: ["sent1.mp3", "sent2.mp3"],
  },
  2: {
    name: "Set 2",
    sentences: ["Sentence 1 Set 2", "Sentence 2 Set 2"],
    audio: ["sent1.mp3", "sent2.mp3"],
  },
};
// service.fetchDrillSets();
//
// const drillSet = service.fetchDrillSet(name);
const state = reactive({
  drillSetList: drillSetList,
  drillSet: null,
  validSelection: false,
});

function fetchDrillSet(drillSetId) {
  const drillSet = state.drillSetList.find(
    (drillSet) => drillSet.id == drillSetId
  );
  console.log(drillSetId, drillSet);
  state.validSelection = true;
  state.drillSet = drillSets[drillSetId];
  console.log(state.drillSet);
}
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
  />
</template>

<style>
@import "@/assets/style.css";
</style>
