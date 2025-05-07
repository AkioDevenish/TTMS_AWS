<template>
	<div class="container-fluid dashboard-4">
		<div class="row mb-4">
			<div class="col-12">
				<div class="d-flex align-items-start gap-4">
					<div class="station-selector">
						<label for="stationSelect" class="form-label">Select Barani Station</label>
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
							brand="Barani"
						/>
					</div>
				</div>
			</div>
		</div>
		<div class="row">
			<template v-if="selectedStation">
				<div class="row">
					<BaraniInsMonitor :selectedStation="selectedStation" :measurements="baraniData.measurements?.value || []" :stationInfo="baraniData.stationInfo?.value || {}" />
					<BaraniStatistics :selectedStation="selectedStation" :measurements="baraniData.getLast24HoursMeasurements?.value || []" :stationInfo="baraniData.stationInfo?.value || {}" />
					<BaraniTempCard :selectedStation="selectedStation" :measurements="baraniData.measurements?.value || []" :stationInfo="baraniData.stationInfo?.value || {}" />
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

const BaraniInsMonitor = defineAsyncComponent(() => import("@/components/theme/stations/barani/BaraniInsMonitor.vue"));
const BaraniStatistics = defineAsyncComponent(() => import("@/components/theme/stations/barani/BaraniStatistics.vue"));
const BaraniTempCard = defineAsyncComponent(() => import("@/components/theme/stations/barani/BaraniTempCard.vue"));
const StationDataExport = defineAsyncComponent(() => import("@/components/theme/stations/StationDataExport.vue"));

const stationNames = ref<Station[]>([]);
const selectedStation = ref<number>(0);
const baraniData = useStationData();

// Get the name of the selected station
const getSelectedStationName = computed(() => {
	const station = stationNames.value.find(s => s.id === selectedStation.value);
	return station?.name || '';
});

// List of available sensors for Barani stations
const availableSensors = computed(() => [
	'wind_ave10',
	'dir_ave10',
	'battery'
]);

const fetchStationNames = async () => {
	try {
		const response = await axios.get<Station[]>('/stations/');
		const baraniStations = response.data.filter(station => station.brand_name === "Allmeteo");
		stationNames.value = baraniStations;

		if (baraniStations.length > 0 && !selectedStation.value) {
			selectedStation.value = baraniStations[0].id;
		}
	} catch (err) {
		console.error('Error fetching station names:', err);
	}
};

watch(() => selectedStation.value, async (newVal) => {
	if (newVal) {
		await baraniData.fetchStationData(newVal);
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