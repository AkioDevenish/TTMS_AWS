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
		
		<div v-if="isLoading" class="d-flex justify-content-center align-items-center" style="height: 300px;">
			<div class="spinner-border text-primary" role="status">
				<span class="visually-hidden">Loading...</span>
			</div>
		</div>
		<div v-else>
			<div class="row">
				<template v-if="selectedStation">
					<!-- Status Summary Row -->
					<div class="row mb-3">
						<div class="col-12">
							<StationStatusSummary 
								:stations="getStationStatusData()" 
							/>
						</div>
					</div>
					
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
const StationStatusSummary = defineAsyncComponent(() => import("@/components/theme/stations/StationStatusSummary.vue"));

const stationNames = ref<Station[]>([]);
const selectedStation = ref<number>(0);
const baraniData = useStationData();
const isLoading = ref(false);

// Get the name of the selected station
const getSelectedStationName = computed(() => {
	const station = stationNames.value.find(s => s.id === selectedStation.value);
	return station?.name || '';
});

// Get station status data for the status summary component
const getStationStatusData = () => {
    if (!baraniData.measurements?.value?.length || !baraniData.stationInfo?.value) {
        return [];
    }
    const measurements = baraniData.measurements.value;
    const stationInfo = baraniData.stationInfo.value;
    const sorted = [...measurements].sort((a: any, b: any) => {
        const dateA = new Date(`${a.date}T${a.time}`);
        const dateB = new Date(`${b.date}T${b.time}`);
        return dateB.getTime() - dateA.getTime();
    });
    const now = Date.now();
    const onlineThresholdMinutes = 60;
    const recentMeasurement = sorted.find((m: any) => {
        const measurementTime = new Date(`${m.date}T${m.time}`).getTime();
        const diffMinutes = (now - measurementTime) / (1000 * 60);
        return diffMinutes <= onlineThresholdMinutes;
    });
    
    let status = 'Offline';
    if (recentMeasurement) {
        const recentMeasurements = sorted.slice(0, 100);
        const totalCount = recentMeasurements.length;
        const invalidCount = recentMeasurements.filter((m: any) => {
            if (m.flag === false) return true;
            const value = parseFloat(m.value);
            if (isNaN(value)) return true;
            if (value === -999 || value === -999.0 || value === 999 || value === 999.0) return true;
            if (value === -9999 || value === -9999.0 || value === 9999 || value === 9999.0) return true;
            if (value === -32768 || value === -32768.0) return true;
            return false;
        }).length;
        
        if (totalCount > 0) {
            const invalidPercentage = (invalidCount / totalCount) * 100;
            const isStuckSensor = checkStuckSensor(recentMeasurements, 'temperature'); // Assuming temperature for Barani
            if (invalidPercentage > 50 || isStuckSensor) {
                status = 'Online Erroneous Data';
            } else {
                status = 'Online';
            }
        } else {
            status = 'Online';
        }
    }
    
    return [{
        status,
        dataQuality: measurements.length > 0 ? {
            validCount: measurements.filter((m: any) => {
                if (m.flag === false) return false;
                const value = parseFloat(m.value);
                if (isNaN(value)) return false;
                if (value === -999 || value === -999.0 || value === 999 || value === 999.0) return false;
                if (value === -9999 || value === -9999.0 || value === 9999 || value === 9999.0) return false;
                if (value === -32768 || value === -32768.0) return false;
                return true;
            }).length,
            totalCount: measurements.length,
            validPercentage: Math.round((measurements.filter((m: any) => {
                if (m.flag === false) return false;
                const value = parseFloat(m.value);
                if (isNaN(value)) return false;
                if (value === -999 || value === -999.0 || value === 999 || value === 999.0) return false;
                if (value === -9999 || value === -9999.0 || value === 9999 || value === 9999.0) return false;
                if (value === -32768 || value === -32768.0) return false;
                return true;
            }).length / measurements.length) * 100)
        } : undefined
    }];
};

// Function to check for stuck sensor (always reading the same value)
const checkStuckSensor = (measurements: any[], sensorType: string) => {
    if (measurements.length < 5) return false; // Need at least 5 measurements to determine if stuck
    
    const firstValue = parseFloat(measurements[0].value);
    if (isNaN(firstValue)) return false; // Cannot determine if stuck if value is NaN
    
    const tolerance = 0.1; // Tolerance for considering values "the same"
    
    // Check if all subsequent values are within tolerance of the first value
    const isStuck = measurements.every(m => {
        const value = parseFloat(m.value);
        return !isNaN(value) && Math.abs(value - firstValue) <= tolerance;
    });
    
    if (!isStuck) return false;
    
    // Additional check: Don't flag sensors where zero values are normal
    const zeroValueSensors = ['rg', 'Precipitation', 'rain_counter', 'rain_intensity_max'];
    
    if (zeroValueSensors.includes(sensorType) && Math.abs(firstValue) < 0.1) {
        return false; // Precipitation sensors reading 0.0mm is normal (no rain)
    }
    
    return true;
};

// List of available sensors for Barani stations
const availableSensors = computed(() => [
	'wind_ave10', 'wind_max10', 'wind_min10', 'dir_ave10', 'dir_max10', 'dir_hi10', 'dir_lo10',
	'battery', 'humidity', 'irradiation', 'irr_max', 'pressure', 'temperature', 'temperature_max',
	'temperature_min', 'rain_counter', 'rain_intensity_max'
]);

const fetchStationNames = async () => {
	try {
		isLoading.value = true;
		const response = await axios.get<any>('/api/stations/');
		// Fix: Handle paginated response structure
		const stationsData = response.data.results || response.data;
		const baraniStations = stationsData.filter((station: any) => 
			station.brand_name.toLowerCase() === "allmeteo".toLowerCase()
		);
		stationNames.value = baraniStations;

		if (baraniStations.length > 0 && !selectedStation.value) {
			selectedStation.value = baraniStations[0].id;
		}
		// Always fetch with both station_ids and sensor_type
		const firstSensor = availableSensors.value[0];
		if (baraniStations.length > 0 && firstSensor) {
			await baraniData.fetchStationData(baraniStations.map((s: any) => s.id), firstSensor, 12);
		} else if (baraniStations.length > 0) {
			console.warn('No sensors available for Barani stations');
		}
	} catch (err) {
		console.error('Error fetching station names:', err);
	} finally {
		isLoading.value = false;
	}
};

watch(() => selectedStation.value, async (newVal) => {
	if (newVal) {
		isLoading.value = true;
		try {
			await baraniData.fetchStationData(newVal, availableSensors.value.join(','), 12);
		} catch (err) {
			console.error('Error fetching station data:', err);
		} finally {
			isLoading.value = false;
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