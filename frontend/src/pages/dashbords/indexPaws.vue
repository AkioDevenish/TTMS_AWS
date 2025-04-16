<template>
	<div class="container-fluid dashboard-4">
		<div class="row mb-4">
			<div class="col-12">
				<div class="d-flex align-items-start gap-4">
					<div class="station-selector">
						<label for="stationSelect" class="form-label">Select Station</label>
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
							brand="3D_Paws"
						/>
					</div>
				</div>
			</div>
		</div>
		<div class="row">
			<template v-if="selectedStation">
				<div class="row">
					<PawsInsMonitor :selectedStation="selectedStation" :measurements="pawsData.measurements?.value || []" :stationInfo="pawsData.stationInfo?.value || {}" />
					<PawsStatistics :selectedStation="selectedStation" :measurements="pawsData.getLast24HoursMeasurements?.value || []" :stationInfo="pawsData.stationInfo?.value || {}" />
					<PawsTempCard :selectedStation="selectedStation" :measurements="pawsData.measurements?.value || []" :stationInfo="pawsData.stationInfo?.value || {}" />
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

// Define the type for a station
interface Station {
	id: number;
	name: string;
	brand_name: string;
}

const PawsInsMonitor = defineAsyncComponent(() => import("@/components/theme/stations/paws/PawsInsMonitor.vue"));
const PawsStatistics = defineAsyncComponent(() => import("@/components/theme/stations/paws/PawsStatistics.vue"));
const PawsTempCard = defineAsyncComponent(() => import("@/components/theme/stations/paws/PawsTempCard.vue"));
const StationDataExport = defineAsyncComponent(() => import("@/components/theme/stations/StationDataExport.vue"));

const stationNames = ref<Station[]>([]); // Explicitly define the type as an array of Station
const selectedStation = ref<number>(0); // Default to 0 instead of null

const pawsData = useStationData();

// Get the name of the selected station
const getSelectedStationName = computed(() => {
	const station = stationNames.value.find(s => s.id === selectedStation.value);
	return station?.name || '';
});

// List of available sensors for 3D_Paws stations
const availableSensors = computed(() => [
	'bt1',
	'mt1',
	'bp1',
	'ws',
	'wd',
	'rg',
	'sv1',
	'si1',
	'su1',
	'bpc',
	'css'
]);

const fetchStationNames = async () => {
	try {
		const response = await axios.get<Station[]>('/stations/');
		const pawsStations = response.data.filter(station => station.brand_name === "3D_Paws");
		stationNames.value = pawsStations;

		if (pawsStations.length > 0 && !selectedStation.value) {
			selectedStation.value = pawsStations[0].id;
		}
	} catch (error) {
		console.error('Error fetching station names:', error);
	}
};

// Watch for station changes to refetch data
watch(() => selectedStation.value, async (newVal) => {
	if (newVal) {
		await pawsData.fetchStationData(newVal);
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