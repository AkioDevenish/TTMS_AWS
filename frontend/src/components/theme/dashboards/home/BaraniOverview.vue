<template>
    <Card1 colClass="col-xl-6 col-md-6 proorder-xl-3 proorder-md-3" location="true" headerTitle="true"
        :title="stationTitle" cardClass="shifts-char-box" cardhaderClass="card-no-border pb-0">
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
import { BaraniOption } from "@/core/data/chart"
import { useStationData } from '@/composables/useStationData'
import axios from 'axios'

const Card1 = defineAsyncComponent(() => import("@/components/common/card/CardData1.vue"))

const { measurements, stationInfo, fetchStationData } = useStationData()
const stationTitle = ref('Barani Station')
const selectedStationId = ref<number | null>(null)

const colors = {
    windSpeed: '#7366ff',
    windDir: '#f73164',
    temperature: '#51bb25',
    humidity: '#f8d62b',
    solar: '#7366ff',
    pressure: '#f73164',
    rainfall: '#51bb25',
    rainIntensity: '#f8d62b'
}

// Only get available data
const availableData = computed(() => {
    if (!measurements.value?.length) return []
    
    const data = []
    const sensorTypes = {
        wind_ave10: { bg: "bg-primary", title: "Wind Speed", unit: "m/s" },
        dir_ave10: { bg: "bg-secondary", title: "Wind Direction", unit: "°" },
        temperature: { bg: "bg-warning", title: "Temperature", unit: "°C" },
        humidity: { bg: "bg-tertiary", title: "Humidity", unit: "%" },
        irradiation: { bg: "bg-primary", title: "Solar Radiation", unit: "W/m²" },
        pressure: { bg: "bg-secondary", title: "Pressure", unit: "hPa" },
        rain_counter: { bg: "bg-warning", title: "Rainfall", unit: "mm" },
        rain_intensity_max: { bg: "bg-tertiary", title: "Rain Intensity", unit: "mm/h" }
    }

    for (const [sensorType, config] of Object.entries(sensorTypes)) {
        const measurement = measurements.value.find(m => m.sensor_type === sensorType)
        if (measurement?.value !== undefined) {
            data.push({
                bg: config.bg,
                title: config.title,
                value: `${parseFloat(measurement.value.toString()).toFixed(1)}${config.unit}`
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
    ...BaraniOption,
    colors: Object.values(colors).slice(0, availableData.value.length),
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
        const response = await axios.get('http://127.0.0.1:8000/stations/')
        const baraniStations = response.data.filter((station: any) => station.brand_name === "Allmeteo")
        
        if (baraniStations.length) {
            const randomStation = baraniStations[Math.floor(Math.random() * baraniStations.length)]
            selectedStationId.value = randomStation.id
            stationTitle.value = `Barani - ${randomStation.name}`
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

watch([() => measurements.value, () => stationInfo.value], () => {
    // No need to update data as availableData is computed
})

onMounted(async () => {
    await fetchRandomStation()
    // Refresh data every minute
    setInterval(async () => {
        if (selectedStationId.value) {
            await fetchStationData(selectedStationId.value)
        }
    }, 60000)
})
</script>

<style scoped>
.bg-primary { background-color: #7366ff !important; }
.bg-secondary { background-color: #f73164 !important; }
.bg-warning { background-color: #51bb25 !important; }
.bg-tertiary { background-color: #f8d62b !important; }
</style>