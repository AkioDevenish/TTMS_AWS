<template>
	<div class="container-fluid dashboard-4">
		<div class="row mb-4">
			<div class="col-12">
				<div class="d-flex align-items-start gap-4">
					<div class="station-selector">
						<label for="stationSelect" class="form-label">Select Zentra Station</label>
						<select id="stationSelect" v-model="selectedStation" class="form-select">
							<option v-for="station in stationNames" :key="station.id" :value="station.id">
								{{ station.name }}
							</option>
						</select>
					</div>
					<div class="station-export flex-grow-1" v-if="selectedStation">
						<StationDataExport 
							:stationId="selectedStation"
							:stationName="getSelectedStationName"
							:sensors="availableSensors"
							brand="Zentra"
						/>
					</div>
				</div>
			</div>
		</div>
		<div class="row">
			<template v-if="selectedStation">
				<div class="row">
					<ZentraInsMonitor :selectedStation="selectedStation" :measurements="zentraData.measurements?.value || []" :stationInfo="zentraData.stationInfo?.value || {}" />
					<ZentraStatistics :selectedStation="selectedStation" :measurements="zentraData.getLast24HoursMeasurements?.value || []" :stationInfo="zentraData.stationInfo?.value || {}" />
					<ZentraTempCard :selectedStation="selectedStation" :measurements="zentraData.measurements?.value || []" :stationInfo="zentraData.stationInfo?.value || {}" />
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
import { ref, onMounted, watch, computed } from 'vue';
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
const StationDataExport = defineAsyncComponent(() => import("@/components/theme/stations/StationDataExport.vue"));

const stationNames = ref<Station[]>([]);
const selectedStation = ref<number>(0);
const isLoading = ref<boolean>(false);
const error = ref<string | null>(null);

const zentraData = useStationData();

// Get the name of the selected station
const getSelectedStationName = computed(() => {
	const station = stationNames.value.find(s => s.id === selectedStation.value);
	return station?.name || '';
});

// Add type for sensorCodeMap to allow string indexing
const sensorCodeMap: { [key: string]: string } = {
	'Air Temperature': 'Air Temperature',
	'Wind Speed': 'Wind Speed',
	'Solar Radiation': 'Solar Radiation',
	'Precipitation': 'Precipitation',
	'Relative Humidity': 'Relative Humidity',
	'Atmospheric Pressure': 'Atmospheric Pressure'
};

const availableSensors = computed(() => Object.keys(sensorCodeMap));

const fetchStationNames = async () => {
	try {
		const response = await axios.get<Station[]>('/stations/');
		const zentraStations = response.data.filter(station => station.brand_name === "Zentra");
		stationNames.value = zentraStations;

		if (zentraStations.length > 0 && !selectedStation.value) {
			selectedStation.value = zentraStations[0].id;
		}
	} catch (err) {
		console.error('Error fetching station names:', err);
		error.value = err instanceof Error ? err.message : 'An error occurred while fetching station names';
	}
};

watch(() => selectedStation.value, async (newVal) => {
	if (newVal) {
		// Fetch all sensors for the last 12 hours, using mapped codes
		await zentraData.fetchStationData(newVal, availableSensors.value.map(s => sensorCodeMap[s]).join(','), 12);
	}
}, { immediate: true });

onMounted(fetchStationNames);
</script>

<style scoped>
.station-selector {
	background-color: white;
	padding: 1rem;
	border-radius: 0.5rem;
	box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
	width: 300px;
}

.station-export {
	background-color: white;
	padding: 1rem;
	border-radius: 0.5rem;
	box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
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

.gap-4 {
	gap: 1.5rem;
}
</style>