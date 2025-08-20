<template>
	<div class="container-fluid dashboard-4">
		<div class="row mb-4">
			<div class="col-12">
				<div class="d-flex align-items-start gap-4">
					<div class="station-selector">
						<label for="stationSelect" class="form-label">Select Sutron Station</label>
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
							brand="Sutron"
						/>
					</div>
				</div>
			</div>
		</div>
		
		<div v-if="isLoading" class="d-flex justify-content-center align-items-center" style="height: 300px;">
			<div class="spinner-border text-primary" role="status">
				<span class="visually-hidden">Loading...</span>
			</div>
		</div>
		
		<div v-else-if="stationNames.length === 0" class="text-center py-4">
			<div class="alert alert-info">
				<h4>No Sutron Stations Available</h4>
				<p>Sutron stations will be automatically created when the data fetcher connects to the external database.</p>
				<p>Please run the data fetcher to sync Sutron stations.</p>
			</div>
		</div>
		
		<div v-else-if="selectedStation" class="row">
			<div class="col-12">
				<div class="card">
					<div class="card-header">
						<h5 class="card-title">Sutron Station Data</h5>
					</div>
					<div class="card-body">
						<p>Station: <strong>{{ getSelectedStationName }}</strong></p>
						<p>Data will be displayed here once measurements are available.</p>
					</div>
				</div>
			</div>
		</div>
		
		<div v-else class="text-center py-4">
			<p>Please select a Sutron station to view data</p>
		</div>
	</div>
</template>

<script lang="ts" setup>
import { ref, onMounted, watch, computed, Ref } from 'vue';
import { defineAsyncComponent } from 'vue';
import axios from 'axios';
import { useStationData } from '@/composables/useStationData';

// Define the type for a station
interface Station {
	id: number;
	name: string;
	brand_name: string;
}

const StationDataExport = defineAsyncComponent(() => import("@/components/theme/stations/StationDataExport.vue"));

const stationNames = ref<Station[]>([]);
const selectedStation = ref<number>(0);
const isLoading = ref(false);

const sutronData = useStationData();

// Get the name of the selected station
const getSelectedStationName = computed(() => {
	const station = stationNames.value.find(s => s.id === selectedStation.value);
	return station?.name || '';
});

// List of available sensors for Sutron stations
const availableSensors = computed(() => [
	'temperature',
	'humidity',
	'pressure',
	'wind_speed',
	'wind_direction',
	'rainfall',
	'solar_radiation',
	'battery'
]);

const fetchStationNames = async () => {
	try {
		isLoading.value = true;
		const response = await axios.get<any>('/api/stations/');
		// Handle paginated response structure
		const stationsData = response.data.results || response.data;
		const sutronStations = stationsData.filter((station: any) => 
			station.brand_name === "Sutron"
		);
		stationNames.value = sutronStations;

		if (sutronStations.length > 0 && !selectedStation.value) {
			selectedStation.value = sutronStations[0].id;
		}
	} catch (err) {
		console.error('Error fetching station names:', err);
	} finally {
		isLoading.value = false;
	}
};

watch(() => selectedStation.value, async (newVal) => {
	if (newVal) {
		// Fetch data for the selected station
		try {
			await sutronData.fetchStationData(newVal, availableSensors.value.join(','), 12);
		} catch (err) {
			console.error('Error fetching station data:', err);
		}
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