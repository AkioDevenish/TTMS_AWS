<template>
	<Card1 colClass="col-xl-12 col-md-12 proorder-xl-2 proorder-md-2" dropdown="true" headerTitle="true" title="T01 Rawin" cardhaderClass="card-no-border pb-0">
		<!-- Dropdown for selecting Instrument -->
		<div class="dropdown">
			<button class="btn btn-secondary dropdown-toggle" type="button" id="instrumentDropdown" data-bs-toggle="dropdown" aria-expanded="false">
				Instrument {{ selectedInstrument }}
			</button>
			<ul class="dropdown-menu" aria-labelledby="instrumentDropdown">
				<li v-for="instrument in instrument_ids" :key="instrument">
					<a class="dropdown-item" href="#" @click="changeInstrument(instrument)">Instrument {{ instrument }}</a>
				</li>
			</ul>
		</div>
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
						<a class="dropdown-item" href="#" @click.prevent="selectMeasurement('bt1')">Temperature 1</a>
						<a class="dropdown-item" href="#" @click.prevent="selectMeasurement('mt1')">Temperature 2</a>
						<a class="dropdown-item" href="#" @click.prevent="selectMeasurement('ws')">Wind Speed</a>
						<a class="dropdown-item" href="#" @click.prevent="selectMeasurement('wd')">Wind Direction</a>
						<a class="dropdown-item" href="#" @click.prevent="selectMeasurement('rg')">Precipitation</a>
						<a class="dropdown-item" href="#" @click.prevent="selectMeasurement('bp1')">Pressure</a>
						<a class="dropdown-item" href="#" @click.prevent="selectMeasurement('sv1')">Downwelling Visible</a>
						<a class="dropdown-item" href="#" @click.prevent="selectMeasurement('si1')">Downwelling Infrared</a>
						<a class="dropdown-item" href="#" @click.prevent="selectMeasurement('su1')">Downwelling Ultraviolet</a>
						<a class="dropdown-item" href="#" @click.prevent="selectMeasurement('bpc')">Battery Percent</a>
						<a class="dropdown-item" href="#" @click.prevent="selectMeasurement('css')">Cell Signal Strength</a>
					</div>
				</div>
			</div>

			<div class="studay-statistics">
				<ul class="d-flex align-item-center gap-2">
					<li><span class="bg-primary"></span>Rainfall</li>
					<li><span class="bg-secondary"></span>Wind Speed</li>
				</ul>
			</div>

			<div id="study-statistics">
				<apexchart type="area" height="230" ref="chart" :options="pawsOptions1" :series="paws_stats"></apexchart>
			</div>
		</Card1>
		<!-- Chart Section -->
		<div class="chart-container">
			<apexchart v-if="chartData.length > 0" type="area" height="330" ref="chart" :options="chartOptions" :series="chartData"></apexchart>
			<div v-else>
				<p>No data available to display.</p>
			</div>
		</div>
	</Card1>
</template>

<script lang="ts" setup>
import { defineAsyncComponent, ref, onMounted, watch, computed, defineProps, onUnmounted, PropType } from 'vue';
import { zentraOptions1 } from '@/core/data/chart';

const Card1 = defineAsyncComponent(() => import("@/components/common/card/CardData1.vue"))
const paws_stats = ref<any[]>([])

const instrument_ids = [1, 3, 4, 6, 11, 12, 18, 24, 27, 28, 29, 31, 32, 33, 36, 37, 38, 41, 42] // List of instrument IDs
const selectedInstrument = ref<number>(instrument_ids[0]) // Default to the first instrument in the list

const getLatestHourlyData = (data: any[]) => {
	const hourlyData: { [key: number]: { value: number; timestamp: string } } = {}

	data.forEach((item: any) => {
		const timestamp = new Date(item.timestamp)
		const hour = timestamp.getHours()

		if (!hourlyData[hour] || timestamp > new Date(hourlyData[hour].timestamp)) {
			hourlyData[hour] = { value: item.value, timestamp: item.timestamp }
		}
	})

	return Array.from({ length: 24 }, (_, i) => hourlyData[i]?.value ?? null)
}

const fetchData = async () => {
	try {
		const response = await axios.get('http://127.0.0.1:8000/api/Measurements/')
		const instrumentData = response.data.filter((item: any) => item.name === `Instrument ${selectedInstrument.value}`)
		const rainGaugeData = instrumentData.filter((item: any) => item.measurement_name === 'Rain Gauge')
		const windSpeedData = instrumentData.filter((item: any) => item.measurement_name === 'Wind Speed')

		const rainGaugeHourlyData = getHourlyData(rainGaugeData)
		const windSpeedHourlyData = getHourlyData(windSpeedData)

		const rainGaugeTimestamps = rainGaugeData.map((item: any) => roundToNearestHour(item.timestamp).toISOString())
		pawsOptions1.xaxis.categories = rainGaugeTimestamps

		paws_stats.value = [
			{ name: 'Rainfall', data: rainGaugeHourlyData },
			{ name: 'Wind Speed', data: windSpeedHourlyData },
		]
	} catch (error) {
		console.error('Error fetching data:', error)
	}
}

const roundToNearestHour = (timestamp: string) => {
	const date = new Date(timestamp)
	const minutes = date.getMinutes()

	if (minutes >= 30) {
		date.setHours(date.getHours() + 1)
	}

	date.setMinutes(0, 0, 0)
	return date
}

const getHourlyData = (data: any[]) => {
	const hourlyData: { [key: string]: { value: number; timestamp: string } } = {}

	data.forEach((item: any) => {
		const roundedTimestamp = roundToNearestHour(item.timestamp).toISOString()

		if (!hourlyData[roundedTimestamp] || new Date(item.timestamp) > new Date(hourlyData[roundedTimestamp].timestamp)) {
			hourlyData[roundedTimestamp] = { value: item.value, timestamp: item.timestamp }
		}
	})

	const hourlyKeys = Object.keys(hourlyData).sort()
	return hourlyKeys.map((key) => hourlyData[key].value)
}

const changeInstrument = (instrument: number) => {
	selectedInstrument.value = instrument
	fetchData() // Fetch new data based on the selected instrument
}

onMounted(() => {
	refreshInterval = setInterval(() => {
		// Just trigger a re-render of the chart
		if (props.measurements.length > 0) {
			chartData.value = [...chartData.value];
		}
	}, 60000);
});

onUnmounted(() => {
	if (refreshInterval) {
		clearInterval(refreshInterval);
	}
});
</script>

<style scoped>
.instrument-tabs .nav-link.active {
	background-color: #007bff;
	color: white;
}

.instrument-tabs .nav-item {
	cursor: pointer;
}

.studay-statistics {
	margin-top: 10px;
}

.dropdown-menu {
	max-height: 300px;
	/* Optional: add scroll if there are too many options */
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