<template>
  <div class="container-fluid dashboard-4">
    <div class="row mb-4">
      <div class="col-12">
        <div class="d-flex align-items-center">
          <div class="station-selector" style="width: 300px;">
            <label for="stationSelect" class="form-label">Select Station</label>
            <select 
              id="stationSelect"
              v-model="selectedStation" 
              class="form-select" 
              @change="handleStationChange"
            >
              <option v-for="station in stationNames" :key="station.id" :value="station.id">
                {{ station.name }}
              </option>
            </select>
          </div>
        </div>
      </div>
    </div>
    <div class="row">
      <Suspense>
        <template #default>
          <div class="row">
            <PawsInsMonitor :selectedStation="selectedStation" :key="`monitor-${selectedStation}`" />
            <PawsStatistics :selectedStation="selectedStation" :key="`stats-${selectedStation}`" />
            <PawsTempCard :selectedStation="selectedStation" :key="`temp-${selectedStation}`" />
          </div>
        </template>
        <template #fallback>
          <div class="text-center py-4">
            <div class="spinner-border text-primary" role="status">
              <span class="visually-hidden">Loading...</span>
            </div>
          </div>
        </template>
      </Suspense>
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

const handleStationChange = async (event: Event) => {
  const select = event.target as HTMLSelectElement;
  selectedStation.value = parseInt(select.value);
};

const fetchStationNames = async () => {
  try {
    const response = await axios.get<Station[]>('http://127.0.0.1:8000/stations/');
    stationNames.value = response.data.filter(station => station.brand_name === "3D Paws");
    if (stationNames.value.length > 0) {
      selectedStation.value = stationNames.value[0].id;
    }
  } catch (error) {
    console.error('Error fetching station names:', error);
  }
};

onMounted(fetchStationNames);
</script>

<style scoped>
.station-selector {
  background-color: white;
  padding: 1rem;
  border-radius: 0.5rem;
  box-shadow: 0 2px 4px rgba(0,0,0,0.05);
}

.form-label {
  font-weight: 500;
  color: #495057;
  margin-bottom: 0.5rem;
}

.form-select {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid #dee2e6;
  border-radius: 0.375rem;
  background-color: #f8f9fa;
  cursor: pointer;
}

.form-select:focus {
  border-color: #7A70BA;
  box-shadow: 0 0 0 0.2rem rgba(122, 112, 186, 0.25);
}

.spinner-border {
  width: 3rem;
  height: 3rem;
}
</style>