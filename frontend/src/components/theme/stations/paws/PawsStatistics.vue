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
</template>

<script lang="ts" setup>
import { defineAsyncComponent, ref, onMounted } from 'vue'
import axios from 'axios'
import { pawsOptions1 } from '@/core/data/chart'

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
		const response = await axios.get('http://167.88.45.83/api/Measurements/')
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
	fetchData()
})
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
</style>