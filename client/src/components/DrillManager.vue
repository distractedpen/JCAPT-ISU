<script setup>
import DrillSelector from "../components/DrillSelector.vue";
import { reactive } from "vue";
import service from "../service/service.js";

const props = defineProps(["routeFrom"]);
const emit = defineEmits(["getDrill"]);

const state = reactive({
  drillSetList: [],
});

const fetchDrillSets = async () => {
  const json = service.jsonAPI("getDrillSets", {});
  json.then((data) => {
    state.drillSetList = data.drill_sets;
  });
};
fetchDrillSets();

const fetchDrillSet = async (drillSetId) => {
  if (
    props.routeFrom === "drill" ||
    (props.routeFrom === "admin" && drillSetId)
  ) {
    const json = service.jsonAPI(
      "getDrillSet",
      JSON.stringify({ drill_set_id: drillSetId })
    );
    json.then((data) => {
      emit("getDrill", { ...data.drillSet, id: drillSetId });
    });
  } else if (props.routeFrom === "admin" && !drillSetId) {
    emit("getDrill", {});
  }
};
</script>

<template>
  <DrillSelector
    :drillSetList="state.drillSetList"
    :routeFrom="props.routeFrom"
    @selectDrillSet="(drillSetId) => fetchDrillSet(drillSetId)"
  />
</template>

<style></style>
