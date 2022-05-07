<script setup>
import { reactive } from "vue";

const props = defineProps(["drillSetList"]);

const state = reactive({
  selected: null,
});
</script>

<template>
  <div class="small-content">
    <select id="drill-select" v-model="state.selected">
      <option disabled value="">Please select one</option>
      <option
        v-for="drillSet in props.drillSetList"
        :value="drillSet.id"
        :key="drillSet.id"
      >
        {{ drillSet.name }}
      </option>
    </select>
    <br />
    <button class="btn-long" @click="$emit('selectDrillSet', state.selected)">
      Run Drill Set
    </button>
  </div>
</template>

<style></style>
