<template>
  <div class="container-fluid dashboard-4">
    <div class="row mb-4">
      <div class="col-12">
        <div class="d-flex align-items-center">
          <div class="station-selector" style="width: 300px;">
            <label for="stationSelect" class="form-label">Select Zentra Station</label>
            <select 
              id="stationSelect"
              v-model="selectedStation" 
              class="form-select"
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
      <template v-if="selectedStation">
        <div class="row">
          <ZentraInsMonitor 
            :selectedStation="selectedStation"
            :measurements="zentraData.measurements?.value || []"
            :stationInfo="zentraData.stationInfo?.value || {}"
          />
          <ZentraStatistics 
            :selectedStation="selectedStation"
            :measurements="zentraData.getLast24HoursMeasurements?.value || []"
            :stationInfo="zentraData.stationInfo?.value || {}"
          />
          <ZentraTempCard 
            :selectedStation="selectedStation"
            :measurements="zentraData.measurements?.value || []"
            :stationInfo="zentraData.stationInfo?.value || {}"
          />
        </div>
      </template>
      <template v-else>
        <div class="text-center py-4">
          <p>Please select a station</p>
        </div>
      </template>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ref, onMounted, watch } from 'vue';
import { defineAsyncComponent } from 'vue';
import axios from 'axios';
import { useStationData } from '@/composables/useStationData';

interface Station {
  id: number;
  name: string;
  brand_name: string;
}

const ZentraInsMonitor = defineAsyncComponent(() => import("@/components/theme/stations/zentra/ZentraInsMonitor.vue"));
const ZentraStatistics = defineAsyncComponent(() => import("@/components/theme/stations/zentra/ZentraStatistics.vue"));
const ZentraTempCard = defineAsyncComponent(() => import("@/components/theme/stations/zentra/ZentraTempCard.vue"));

const stationNames = ref<Station[]>([]);
const selectedStation = ref<number>(0);
const isLoading = ref<boolean>(false);
const error = ref<string | null>(null);

const zentraData = useStationData();

const fetchStationNames = async () => {
  try {
    isLoading.value = true;
    const response = await axios.get<Station[]>('http://127.0.0.1:8000/stations/');
    // Try both formats of the brand name
    const zentraStations = response.data.filter(station => 
      station.brand_name === "Zentra" || station.brand_name === "ZENTRA"
    );
    
    console.log('All stations:', response.data); // Debug log
    console.log('Filtered Zentra stations:', zentraStations); // Debug log
    
    stationNames.value = zentraStations;
    
    if (zentraStations.length > 0 && !selectedStation.value) {
      selectedStation.value = zentraStations[0].id;
    } else {
      error.value = 'No Zentra stations available';
    }
  } catch (error) {
    console.error('Error fetching station names:', error);
    error.value = 'Failed to fetch station data';
  } finally {
    isLoading.value = false;
  }
};

watch(() => selectedStation.value, async (newVal) => {
  if (newVal) {
    await zentraData.fetchStationData(newVal);
  }
}, { immediate: true });

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
</style>