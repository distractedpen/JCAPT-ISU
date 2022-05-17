<script setup>
import DrillManager from "../components/DrillManager.vue";
import DrillViewer from "../components/DrillViewer.vue";
import PageHeader from "../components/PageHeader.vue";
import { reactive, ref } from "vue";
import service from "../service/service.js";

const resultText = ref(null);

const state = reactive({
  routeFrom: "drill",
  drillSet: null,
  currentListeningURL: "",
  hasResult: false,
  result: {},
});

const getDrillSet = (drillSet) => {
  state.drillSet = drillSet;
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

const fetchAudio = async (drillSetId, fileName) => {
  const blob = await service.blobAPI(
    "getAudio",
    JSON.stringify({
      drillSetId: drillSetId,
      fileName: fileName,
    })
  );
  state.currentListeningURL = window.URL.createObjectURL(blob);
};
</script>

<template>
  <PageHeader />

  <DrillManager
    v-if="!state.drillSet"
    :routeFrom="state.routeFrom"
    @getDrill="(drillset) => getDrillSet(drillset)"
  />

  <!--DrillViewer gets drill set data from DrillSelector-->
  <DrillViewer
    v-if="state.drillSet"
    :drillSet="state.drillSet"
    :currentListeningURL="state.currentListeningURL"
    :result="state.result"
    @fetchAudio="(fileName) => fetchAudio(state.drillSet.id, fileName)"
    @fetchResult="
      (audio, currentSentence) =>
        fetchResult(state.drillSet.id, audio, currentSentence)
    "
  >
    <p ref="resultText" class="resultText">
      Press Record and Start Speaking. Press Stop to Send Recording to Service.
    </p>
  </DrillViewer>
</template>

<style>
@import "@/assets/style.css";

.resultText {
  font-size: 24px;
}
</style>
