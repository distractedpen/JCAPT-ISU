<script setup>
/**********************************
 * Global Variables
 **********************************/
import DrillSelector from "../components/DrillSelector.vue";
import DrillViewer from "../components/DrillViewer.vue";
import { reactive } from "vue";
import service from "../service/service.js";

const state = reactive({
  drillSetId: null,
  drillSet: null,
  drillSetList: [],
  validSelection: false,
  currentListeningURL: "",
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
    @fetchAudio="(filename) => fetchAudio(state.drillSetId, filename)"
    :currentListeningURL="state.currentListeningURL"
  />
</template>

<style>
@import "@/assets/style.css";
</style>
