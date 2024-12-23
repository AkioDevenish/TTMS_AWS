<template>
  <div class="container-fluid dashboard-4">
    <div class="row">
      <div class="col-12 mb-4">
        <select v-model="selectedStation" @change="fetchData" class="form-select">
          <option v-for="station in stationNames" :key="station.id" :value="station.id">
            {{ station.name }}
          </option>
        </select>
      </div>
      <PawsInsMonitor :selectedStation="selectedStation" />
      <PawsStatistics :selectedStation="selectedStation" />
      <PawsTempCard :selectedStation="selectedStation" />
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ref, onMounted } from 'vue';
import { defineAsyncComponent } from 'vue';
import axios from 'axios';

// Define the type for a station
interface Station {
  id: number;
  name: string;
  brand_name: string;
}

const PawsInsMonitor = defineAsyncComponent(() => import("@/components/theme/stations/paws/PawsInsMonitor.vue"));
const PawsStatistics = defineAsyncComponent(() => import("@/components/theme/stations/paws/PawsStatistics.vue"));
const PawsTempCard = defineAsyncComponent(() => import("@/components/theme/stations/paws/PawsTempCard.vue"));

const stationNames = ref<Station[]>([]); // Explicitly define the type as an array of Station
const selectedStation = ref<number>(0); // Default to 0 instead of null

const fetchStationNames = async () => {
  try {
    const response = await axios.get<Station[]>('http://127.0.0.1:8000/stations/'); // Specify the expected response type
    // Filter the response to get only the station named "3D Paws"
    stationNames.value = response.data.filter(station => station.brand_name === "3D Paws");
    if (stationNames.value.length > 0) {
      selectedStation.value = stationNames.value[0].id; // Set default to the first station
    }
  } catch (error) {
    console.error('Error fetching station names:', error);
  }
};

onMounted(fetchStationNames);
</script>