<template>
	<div v-if="isLoading" class="d-flex justify-content-center align-items-center" style="height: 300px;">
		<div class="spinner-border text-primary" role="status">
			<span class="visually-hidden">Loading...</span>
		</div>
	</div>
	<div v-else>
		<div class="container-fluid dashboard-4">
			<div class="row mb-4">
				<div class="col-12">
					<div class="d-flex align-items-start gap-4">
						<div class="station-selector">
							<label for="stationSelect" class="form-label">Select OTT Station</label>
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
								brand="OTT"
							/>
						</div>
					</div>
				</div>
			</div>
			<div class="row">
				<template v-if="selectedStation">
					<div class="row">
						<HydrometInsMonitor :selectedStation="selectedStation" :measurements="ottData.measurements?.value || []" :stationInfo="ottData.stationInfo?.value || {}" />
						<HydrometStatistics :selectedStation="selectedStation" :measurements="ottData.getLast24HoursMeasurements?.value || []" :stationInfo="ottData.stationInfo?.value || {}" />
						<HydrometTempCard :selectedStation="selectedStation" :measurements="ottData.measurements?.value || []" :stationInfo="ottData.stationInfo?.value || {}" />
					</div>
				</template>
				<template v-else>
					<div class="text-center py-4">
						<p>Please select a station</p>
					</div>
				</template>
			</div>
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

const HydrometInsMonitor = defineAsyncComponent(() => import("@/components/theme/stations/hydromet/HydrometInsMonitor.vue"));
const HydrometStatistics = defineAsyncComponent(() => import("@/components/theme/stations/hydromet/HydrometStatistics.vue"));
const HydrometTempCard = defineAsyncComponent(() => import("@/components/theme/stations/hydromet/HydrometTempCard.vue"));
const StationDataExport = defineAsyncComponent(() => import("@/components/theme/stations/StationDataExport.vue"));

const stationNames = ref<Station[]>([]);
const selectedStation = ref<number>(0);
const ottData = useStationData();
const isLoading = ref(false);

// Get the name of the selected station
const getSelectedStationName = computed(() => {
	const station = stationNames.value.find(s => s.id === selectedStation.value);
	return station?.name || '';
});

// List of available sensors for OTT stations
const availableSensors = computed(() => [
	'5 min rain',
	'Air Temperature',
	'Barometric Pressure',
	'Baro Tendency',
	'Battery',
	'Daily Rain',
	'Dew Point',
	'Gust Direction',
	'Gust Speed',
	'Hours of Sunshine',
	'Maximum Air Temperature',
	'Minimum Air Temperature',
	'Relative Humidity',
	'Solar Radiation Avg',
	'Solar Radiation Total',
	'Wind Dir Average',
	'Wind Dir Inst',
	'Wind Speed Average',
	'Wind Speed Inst'
]);

const fetchStationNames = async () => {
	try {
		isLoading.value = true;
		const response = await axios.get<Station[]>('/stations/');
		const ottStations = response.data.filter(station => station.brand_name === "OTT");
		stationNames.value = ottStations;

		if (ottStations.length > 0 && !selectedStation.value) {
			selectedStation.value = ottStations[0].id;
		}
		// Always fetch with both station_ids and sensor_type
		const firstSensor = availableSensors.value[0];
		if (ottStations.length > 0 && firstSensor) {
			await ottData.fetchStationData(ottStations.map(s => s.id), firstSensor, 12);
		} else if (ottStations.length > 0) {
			console.warn('No sensors available for OTT stations');
		}
	} catch (err) {
		console.error('Error fetching station names:', err);
	} finally {
		isLoading.value = false;
	}
};

watch(() => selectedStation.value, async (newVal) => {
	const firstSensor = availableSensors.value[0];
	if (newVal && firstSensor) {
		isLoading.value = true;
		try {
			await ottData.fetchStationData(newVal, firstSensor, 12);
		} catch (err) {
			console.error('Error fetching station data:', err);
		} finally {
			isLoading.value = false;
		}
	} else if (newVal) {
		console.warn('No sensors available for selected station');
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