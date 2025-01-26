<template>
	<Card1 colClass="col-xl-6 col-md-6 proorder-xl-3 proorder-md-3" location="true" headerTitle="true" :title="stationTitle" cardClass="shifts-char-box" cardhaderClass="card-no-border pb-0">
		<div class="row">
			<div class="col-5">
				<div class="overview" id="shifts-overview">
					<apexchart type="donut" height="200" :options="chartOptions" :series="chartSeries">
					</apexchart>
				</div>
			</div>
			<div class="col-7 shifts-overview">
				<div class="d-flex gap-2" v-for="(item, index) in overviewData" :key="index">
					<div class="flex-shrink-0"><span :class="item.bg"> </span></div>
					<div class="flex-grow-1">
						<h6>{{ item.title }}</h6>
					</div>
					<span>{{ item.value }}</span>
				</div>
			</div>
		</div>
	</Card1>
</template>

<script lang="ts" setup>
import { ref, defineAsyncComponent, computed, onMounted, watch } from 'vue'
import { ZentraOption } from "@/core/data/chart"
import { useStationData } from '@/composables/useStationData'
import axios from 'axios'

const Card1 = defineAsyncComponent(() => import("@/components/common/card/CardData1.vue"))

const { measurements, stationInfo, getLatestMeasurement, fetchStationData } = useStationData()
const stationTitle = ref('Zentra Station')
const selectedStationId = ref<number | null>(null)

// Define consistent colors
const colors = {
	airTemp: '#7366ff',      // primary
	humidity: '#f73164',     // secondary
	windSpeed: '#51bb25',    // warning
	solar: '#f8d62b'         // tertiary
}

const latestValues = computed(() => ({
	temperature: measurements.value.find(m => m.sensor_type === 'Air Temperature')?.value || 0,
	humidity: measurements.value.find(m => m.sensor_type === 'Relative Humidity')?.value || 0,
	windSpeed: measurements.value.find(m => m.sensor_type === 'Wind Speed')?.value || 0,
	solar: measurements.value.find(m => m.sensor_type === 'Solar Radiation')?.value || 0
}))

const overviewData = ref([
	{ bg: "bg-primary", title: "Air Temperature", value: "0°C" },
	{ bg: "bg-secondary", title: "Relative Humidity", value: "0%" },
	{ bg: "bg-warning", title: "Wind Speed", value: "0 m/s" },
	{ bg: "bg-tertiary", title: "Solar Radiation", value: "0 W/m²" }
])

const chartSeries = ref([0, 0, 0, 0])

const chartOptions = computed(() => ({
	...ZentraOption,
	colors: [colors.airTemp, colors.humidity, colors.windSpeed, colors.solar],
	tooltip: {
		y: {
			formatter: (value: number, { seriesIndex }: { seriesIndex: number }) => {
				const units = ['°C', '%', 'm/s', 'W/m²']
				return `${value.toFixed(1)} ${units[seriesIndex]}`
			}
		}
	},
	labels: ['Air Temperature', 'Relative Humidity', 'Wind Speed', 'Solar Radiation']
}))

const updateData = () => {
	if (!measurements.value?.length) return

	const latestValues = {
		temperature: measurements.value.find(m => m.sensor_type === 'Air Temperature')?.value || 0,
		humidity: measurements.value.find(m => m.sensor_type === 'Relative Humidity')?.value || 0,
		wind_speed: measurements.value.find(m => m.sensor_type === 'Wind Speed')?.value || 0,
		solar_radiation: measurements.value.find(m => m.sensor_type === 'Solar Radiation')?.value || 0
	}

	overviewData.value = [
		{ bg: "bg-primary", title: "Air Temperature", value: `${latestValues.temperature}°C` },
		{ bg: "bg-secondary", title: "Relative Humidity", value: `${latestValues.humidity}%` },
		{ bg: "bg-warning", title: "Wind Speed", value: `${latestValues.wind_speed} m/s` },
		{ bg: "bg-tertiary", title: "Solar Radiation", value: `${latestValues.solar_radiation} W/m²` }
	]

	chartSeries.value = [
		parseFloat(latestValues.temperature.toString()),
		parseFloat(latestValues.humidity.toString()),
		parseFloat(latestValues.wind_speed.toString()),
		parseFloat(latestValues.solar_radiation.toString())
	]
}

const fetchZentraStations = async () => {
	try {
		const response = await axios.get('/stations/')
		const zentraStations = response.data.filter((station: any) => station.brand_name === "Zentra")

		if (zentraStations.length > 0) {
			const firstStation = zentraStations[0]
			selectedStationId.value = firstStation.id
			stationTitle.value = `Zentra - ${firstStation.name}`
		}
	} catch (error) {
		console.error('Error fetching stations:', error)
	}
}

watch(() => selectedStationId.value, (newId) => {
	if (newId) {
		fetchStationData(newId)
	}
})

watch(() => measurements.value, (newMeasurements) => {
	if (!newMeasurements?.length) return
	const values = latestValues.value
	overviewData.value = [
		{ bg: "bg-primary", title: "Air Temperature", value: `${parseFloat(values.temperature.toString()).toFixed(1)}°C` },
		{ bg: "bg-secondary", title: "Relative Humidity", value: `${parseFloat(values.humidity.toString()).toFixed(1)}%` },
		{ bg: "bg-warning", title: "Wind Speed", value: `${parseFloat(values.windSpeed.toString()).toFixed(1)} m/s` },
		{ bg: "bg-tertiary", title: "Solar Radiation", value: `${parseFloat(values.solar.toString()).toFixed(1)} W/m²` }
	]
	chartSeries.value = [
		parseFloat(values.temperature.toString()),
		parseFloat(values.humidity.toString()),
		parseFloat(values.windSpeed.toString()),
		parseFloat(values.solar.toString())
	]
}, { immediate: true })

onMounted(async () => {
	await fetchZentraStations()
	// Refresh data every minute
	setInterval(async () => {
		if (selectedStationId.value) {
			await fetchStationData(selectedStationId.value)
		}
	}, 60000)
})
</script>

<style scoped>
.bg-primary {
	background-color: #7366ff !important;
}

.bg-secondary {
	background-color: #f73164 !important;
}

.bg-warning {
	background-color: #51bb25 !important;
}

.bg-tertiary {
	background-color: #f8d62b !important;
}
</style>