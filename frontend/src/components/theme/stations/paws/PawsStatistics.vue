<template>
	<Card1 colClass="col-xl-12 col-md-12 proorder-xl-2 proorder-md-2" dropdown="true" cardhaderClass="card-no-border pb-0">
		<!-- Title and Dropdown Section -->
		<div class="d-flex justify-content-between align-items-center mb-4">
			<h4 class="mb-0">{{ stationInfo?.name || 'Station Statistics' }}</h4>
			<div class="dropdown position-relative">
				<button class="btn dropdown-toggle w-100 d-flex align-items-center justify-content-between" id="measurementDropdown" type="button" data-bs-toggle="dropdown" aria-expanded="false">
					<span class="mx-auto">{{ currentSensorName }}</span>
					<span class="dropdown-toggle-icon ms-3"></span>
				</button>

				<div class="dropdown-menu dropdown-menu-end position-absolute" aria-labelledby="measurementDropdown">
					<a v-for="sensor in availableSensors" 
						:key="sensor.type" 
						class="dropdown-item" 
						href="#" 
						@click.prevent="selectMeasurement(sensor.type)">
						{{ sensor.name }}
					</a>
				</div>
			</div>
		</div>

		<!-- Chart Section -->
		<div class="chart-container">
			<div v-if="isLoading" class="d-flex justify-content-center align-items-center" style="height: 330px;">
				<div class="spinner-border text-primary" role="status">
					<span class="visually-hidden">Loading...</span>
				</div>
			</div>
			<apexchart
				v-else-if="chartData.length > 0"
				type="area"
				height="330"
				ref="chart"
				:options="chartOptions"
				:series="chartData"
			></apexchart>
			<div v-else class="d-flex justify-content-center align-items-center" style="height: 330px;">
				<p class="text-muted">No data available to display.</p>
			</div>
		</div>
	</Card1>
</template>

<script lang="ts" setup>
import { defineAsyncComponent, ref, watch, computed, defineProps, onMounted, onUnmounted } from 'vue';
import { zentraOptions1 } from '@/core/data/chart';
import axios from 'axios';
import { useStationData, type Measurement } from '@/composables/useStationData';
const Card1 = defineAsyncComponent(() => import('@/components/common/card/CardData1.vue'));

const props = defineProps({
	selectedStation: {
		type: Number,
		required: true
	},
	measurements: {
		type: Array,
		default: () => []
	},
	stationInfo: {
		type: Object,
		default: () => ({})
	}
});

const selectedSensorType = ref<string>('');
const chartData = ref<any[]>([]);
const availableSensors = ref<Array<{type: string, name: string, unit: string}>>([]);

// Use the useStationData composable
const pawsData = useStationData();

// Fetch available sensors for the station
const fetchAvailableSensors = async () => {
	if (!props.selectedStation) return;
	
	try {
		// Add debounce to prevent multiple rapid calls
		// We don't need isLoading here as it's handled by pawsData composable
		// if (isLoading.value) return;
		// isLoading.value = true;

		const response = await axios.get(`/station-sensors/`, {
			params: {
				station_id: props.selectedStation,
				brand: '3D_Paws'
			}
		});
		
		if (response.data && Array.isArray(response.data)) {
			// Create a Map to store unique sensors by type
			const uniqueSensors = new Map();
			
			// Filter and deduplicate sensors
			response.data.forEach(sensor => {
				const pawsSensorTypes = [
					'bt1', 'mt1', 'bp1', 'ws', 'wd', 'rg', 
					'sv1', 'si1', 'su1', 'bpc', 'css'
				];
				
				if (pawsSensorTypes.includes(sensor.sensor_type)) {
					// Only add if we haven't seen this sensor type before
					if (!uniqueSensors.has(sensor.sensor_type)) {
						uniqueSensors.set(sensor.sensor_type, {
							type: sensor.sensor_type,
							name: sensor.name || sensor.sensor_type,
							unit: sensor.unit || ''
						});
					}
				}
			});

			// Convert Map values to array
			availableSensors.value = Array.from(uniqueSensors.values());
			
			// Set initial selected sensor if available
			if (availableSensors.value.length > 0 && !selectedSensorType.value) {
				selectedSensorType.value = availableSensors.value[0].type;
			}
		}
	} catch (error) {
		console.error('Error fetching available sensors:', error);
	} finally {
		// isLoading.value = false;
	}
};

const currentSensorName = computed(() => {
	const sensor = availableSensors.value.find(s => s.type === selectedSensorType.value);
	return sensor?.name || selectedSensorType.value;
});

const currentSensorUnit = computed(() => {
	const sensor = availableSensors.value.find(s => s.type === selectedSensorType.value);
	return sensor?.unit || '';
});

const sensorConfig: Record<string, { name: string; unit: string }> = {
	'bp1': { name: 'BMX280 Pressure', unit: 'hPa' },
	'bt1': { name: 'BMX280 Temperature', unit: '°C' },
	'mt1': { name: 'MCP9808 Temperature', unit: '°C' },
	'ws': { name: 'Wind Speed', unit: 'm/s' },
	'wd': { name: 'Wind Direction', unit: '°' },
	'rg': { name: 'Rain Gauge', unit: 'mm' },
	'sv1': { name: 'Downwelling Visible', unit: 'W/m²' },
	'si1': { name: 'Downwelling Infrared', unit: 'W/m²' },
	'su1': { name: 'Downwelling Ultraviolet', unit: 'W/m²' },
	'bpc': { name: 'Battery Percent', unit: '%' },
	'css': { name: 'Cell Signal Strength', unit: '%' }
};
const chartOptions = computed(() => ({
	...zentraOptions1,
	yaxis: {
		...zentraOptions1.yaxis,
		title: {
			text: `${currentSensorName.value} (${currentSensorUnit.value})`,
			style: {
				fontSize: '14px',
				fontWeight: 500
			}
		},
		labels: {
			formatter: (val: number) => `${val.toFixed(1)} ${currentSensorUnit.value}`
		}
	},
	xaxis: {
		...zentraOptions1.xaxis,
		type: 'datetime',
		labels: {
			formatter: (val: number) => {
				const date = new Date(val);
				return date.toLocaleString('en-US', {
					month: 'numeric',
					day: 'numeric',
					hour: '2-digit',
					minute: '2-digit',
					hour12: true
				});
			}
		}
	},
	tooltip: {
		x: {
			formatter: (val: number) => {
				const date = new Date(val);
				return date.toLocaleString('en-US', {
					month: 'numeric',
					day: 'numeric',
					hour: '2-digit',
					minute: '2-digit',
					hour12: true
				});
			}
		},
		y: {
			formatter: (val: number) => `${val.toFixed(1)} ${currentSensorUnit.value}`
		}
	}
}));

// Observe changes in pawsData.measurements and selectedSensorType to update chartData
watch([() => pawsData.measurements.value, () => selectedSensorType.value], 
	([newMeasurements, newSensorType]) => {
		if (!newMeasurements?.length) {
			chartData.value = [];
			return;
		}
		const filteredData = newMeasurements.filter(
			measurement => measurement.sensor_type === newSensorType
		);
		if (!filteredData.length) {
			chartData.value = [];
			return;
		}
		chartData.value = [{
			// Find the sensor name and unit from availableSensors for the current type
			name: availableSensors.value.find(s => s.type === newSensorType)?.name || newSensorType,
			data: filteredData.map(item => ({
				x: new Date(`${item.date}T${item.time}`).getTime(),
				y: parseFloat(item.value.toString())
			}))
		}];
	}, 
	{ immediate: true }
);

// Add debounce to prevent multiple rapid calls
let fetchTimeout: number | null = null;

// Watch for selectedStation and availableSensors changes
watch([() => props.selectedStation, () => availableSensors.value], ([newStationId, newAvailableSensors]) => {
	// Only fetch data if a station is selected AND we have fetched the available sensors
	if (newStationId && newAvailableSensors.length > 0) {
		if (fetchTimeout) {
			clearTimeout(fetchTimeout);
		}
		fetchTimeout = setTimeout(() => {
			// Fetch data for all available sensors for the selected station
			pawsData.fetchStationData(newStationId, newAvailableSensors.map(sensor => sensor.type).join(','), 12);
		}, 300); // 300ms debounce
	} else {
		// Clear measurements if no station or no available sensors
		pawsData.measurements.value = [];
	}
}, { immediate: true }); // Fetch data initially if station and sensors are available

// Fetch available sensors when the component is mounted or station changes
onMounted(() => {
	fetchAvailableSensors();
});

// We no longer need the separate watch for selectedStation to fetch sensors
// as it's handled by the combined watch above.
// watch(() => props.selectedStation, () => {
//     fetchAvailableSensors();
// });

// Clean up timeout on component unmount
onUnmounted(() => {
	if (fetchTimeout) {
		clearTimeout(fetchTimeout);
	}
});

const selectMeasurement = (sensorType: string) => {
	selectedSensorType.value = sensorType;
	// When a measurement is selected, we don't need to refetch all data,
	// the watch on pawsData.measurements and selectedSensorType will handle updating the chart.
};

// Expose the loading state from the composable
const isLoading = computed(() => pawsData.isLoading.value);

</script>

<style scoped>
.chart-container {
	min-height: 350px;
}

.dropdown-menu {
	max-height: 300px;
	overflow-y: auto;
}

.btn.dropdown-toggle {
	background-color: #f8f9fa;
	border: 1px solid #dee2e6;
	color: #495057;
	padding: 0.5rem 1rem;
	appearance: none;
	-webkit-appearance: none;
	-moz-appearance: none;
}

.btn.dropdown-toggle::after {
	display: none;
}

.dropdown-toggle-icon {
	border-left: 4px solid transparent;
	border-right: 4px solid transparent;
	border-top: 4px solid currentColor;
	display: inline-block;
	margin-left: 0.255em;
	vertical-align: middle;
}
</style>