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
					<a class="dropdown-item" href="#" @click.prevent="selectMeasurement('bt1')">BMX280 Temperature</a>
					<a class="dropdown-item" href="#" @click.prevent="selectMeasurement('mt1')">MCP9808 Temperature</a>
					<a class="dropdown-item" href="#" @click.prevent="selectMeasurement('ws')">Wind Speed</a>
					<a class="dropdown-item" href="#" @click.prevent="selectMeasurement('wd')">Wind Direction</a>
					<a class="dropdown-item" href="#" @click.prevent="selectMeasurement('rg')">Rain Gauge</a>
					<a class="dropdown-item" href="#" @click.prevent="selectMeasurement('bp1')">Pressure</a>
					<a class="dropdown-item" href="#" @click.prevent="selectMeasurement('sv1')">Downwelling Visible</a>
					<a class="dropdown-item" href="#" @click.prevent="selectMeasurement('si1')">Downwelling Infrared</a>
					<a class="dropdown-item" href="#" @click.prevent="selectMeasurement('su1')">Downwelling Ultraviolet</a>
					<a class="dropdown-item" href="#" @click.prevent="selectMeasurement('bpc')">Battery Percent</a>
					<a class="dropdown-item" href="#" @click.prevent="selectMeasurement('css')">Cell Signal Strength</a>
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
import { defineAsyncComponent, ref, onMounted, watch, computed, defineProps, onUnmounted, PropType } from 'vue';
import VueApexCharts from 'vue3-apexcharts';
import { zentraOptions1 } from '@/core/data/chart';
import { useStationData } from '@/composables/useStationData';

const Card1 = defineAsyncComponent(() => import('@/components/common/card/CardData1.vue'));

const props = defineProps({
	selectedStation: {
		type: Number,
		required: true
	},
	measurements: {
		type: Array as PropType<any[]>,
		default: () => []
	},
	stationInfo: {
		type: Object,
		default: () => ({})
	}
});

const { measurements: stationMeasurements, stationInfo: stationInfoData, getLast24HoursMeasurements, fetchStationData } = useStationData();
const selectedSensorType = ref<string>('bt1');
const chartData = ref<any[]>([]);
const isLoading = ref(false);

// Mapping of sensor types to display names and units
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

// Get the current sensor's display name
const currentSensorName = computed(() => {
	return sensorConfig[selectedSensorType.value]?.name || selectedSensorType.value;
});

// Get the current sensor's unit
const currentSensorUnit = computed(() => {
	return sensorConfig[selectedSensorType.value]?.unit || '';
});

// Chart options
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

// Watch for measurements and selected sensor type changes
watch([() => getLast24HoursMeasurements.value, () => selectedSensorType.value], 
	([newMeasurements, newSensorType]) => {
		console.log('New measurements:', newMeasurements);
		console.log('Selected sensor type:', newSensorType);
		
		if (!newMeasurements?.length) {
			console.log('No measurements available');
			chartData.value = [];
			return;
		}

		const filteredData = newMeasurements.filter(
			measurement => measurement.sensor_type === newSensorType
		);
		
		console.log('Filtered data:', filteredData);

		if (!filteredData.length) {
			console.log('No data for selected sensor type');
			chartData.value = [];
			return;
		}

		chartData.value = [{
			name: sensorConfig[newSensorType]?.name || newSensorType,
			data: filteredData.map(item => ({
				x: new Date(`${item.date}T${item.time}`).getTime(),
				y: parseFloat(item.value.toString())
			}))
		}];
		
		console.log('Chart data:', chartData.value);
	}, 
	{ immediate: true }
);

// Handle measurement selection
const selectMeasurement = (sensorType: string) => {
	selectedSensorType.value = sensorType;
};

// Add auto-refresh interval
let refreshInterval: number | undefined;

onMounted(() => {
	refreshInterval = setInterval(() => {
		if (chartData.value.length > 0) {
			chartData.value = [...chartData.value];
		}
	}, 1000);
});

onUnmounted(() => {
	if (refreshInterval) {
		clearInterval(refreshInterval);
	}
});

// Watch for station changes
watch(() => props.selectedStation, (newStationId) => {
	if (newStationId) {
		console.log('Fetching data for station:', newStationId);
		fetchStationData(newStationId);
	}
}, { immediate: true });
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