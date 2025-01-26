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
				<div class="d-flex gap-2" v-for="(item, index) in availableData" :key="index">
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
import { pawsoption } from "@/core/data/chart"
import { useStationData } from '@/composables/useStationData'
import axios from 'axios'

const Card1 = defineAsyncComponent(() => import("@/components/common/card/CardData1.vue"))

const { measurements, stationInfo, fetchStationData } = useStationData()
const stationTitle = ref('PAWS Station 2')
const selectedStationId = ref<number | null>(null)
const excludeStationId = ref<number | null>(null)

const colors = {
	windSpeed: '#7366ff',
	windDir: '#f73164',
	temp: '#51bb25',
	humidity: '#f8d62b'
}

// Get the exclude station ID from PawsOverview
watch(() => excludeStationId.value, () => {
	fetchRandomStation()
})

const availableData = computed(() => {
	if (!measurements.value?.length) return []

	const data = []
	const sensorTypes = {
		ws: { bg: "bg-primary", title: "Wind Speed", unit: "m/s", color: colors.windSpeed },
		wd: { bg: "bg-secondary", title: "Wind Direction", unit: "°", color: colors.windDir },
		bt1: { bg: "bg-warning", title: "Temperature", unit: "°C", color: colors.temp },
		rh1: { bg: "bg-tertiary", title: "Humidity", unit: "%", color: colors.humidity }
	}

	for (const [sensorType, config] of Object.entries(sensorTypes)) {
		const measurement = measurements.value.find(m => m.sensor_type === sensorType)
		if (measurement?.value !== undefined) {
			data.push({
				bg: config.bg,
				title: config.title,
				value: `${parseFloat(measurement.value.toString()).toFixed(1)}${config.unit}`,
				color: config.color
			})
		}
	}

	return data
})

const chartSeries = computed(() =>
	availableData.value.map(item =>
		parseFloat(item.value.replace(/[^0-9.-]+/g, ""))
	)
)

const chartOptions = computed(() => ({
	...pawsoption,
	colors: availableData.value.map(item => item.color),
	tooltip: {
		y: {
			formatter: (value: number, { seriesIndex }: { seriesIndex: number }) => {
				return availableData.value[seriesIndex]?.value || `${value.toFixed(1)}`
			}
		}
	},
	labels: availableData.value.map(item => item.title)
}))

const fetchRandomStation = async () => {
	try {
		const response = await axios.get('/stations/')
		const pawsStations = response.data.filter((station: any) =>
			station.brand_name === "3D_Paws" && station.id !== excludeStationId.value
		)

		if (pawsStations.length) {
			const randomStation = pawsStations[Math.floor(Math.random() * pawsStations.length)]
			selectedStationId.value = randomStation.id
			stationTitle.value = `PAWS - ${randomStation.name}`
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

onMounted(async () => {
	await fetchRandomStation()
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