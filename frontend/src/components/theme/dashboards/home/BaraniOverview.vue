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
import { ref, defineAsyncComponent, onMounted, computed } from 'vue'
import { BaraniOption } from "@/core/data/chart"
import axios from 'axios'

const Card1 = defineAsyncComponent(() => import("@/components/common/card/CardData1.vue"))

const stationTitle = ref('Barani Station')
const overviewData = ref([
    { bg: "bg-primary", title: "Wind Speed", value: "0 m/s" },
    { bg: "bg-secondary", title: "Wind Direction", value: "0°" },
    { bg: "bg-warning", title: "Dewpoint", value: "0°C" },
    { bg: "bg-tertiary", title: "Irradiation", value: "0W/m2" }
])

const chartSeries = ref([0, 0, 0, 0])

const chartOptions = computed(() => ({
    ...BaraniOption,
    tooltip: {
        y: {
            formatter: (value: number, { seriesIndex }: { seriesIndex: number }) => {
                const units = ['m/s', '°', '°C', 'W/m2']
                return `${value.toFixed(1)} ${units[seriesIndex]}`
            }
        }
    },
    labels: ['Wind Speed', 'Wind Direction', 'Dewpoint', 'Irradiation']
}))

const getDateTime = (date: string, time: string): number => {
    return new Date(`${date}T${time}`).getTime()
}

const filterLastTwoDaysData = (measurements: any[]) => {
    if (!measurements.length) return []
    
    // Sort measurements by date and time (newest first)
    const sortedMeasurements = measurements.sort((a, b) => {
        const dateA = getDateTime(a.date, a.time)
        const dateB = getDateTime(b.date, b.time)
        return dateB - dateA
    })

    // Get the latest timestamp
    const latestTime = getDateTime(sortedMeasurements[0].date, sortedMeasurements[0].time)
    
    // Calculate timestamp for 2 days ago
    const twoDaysAgo = latestTime - (2 * 24 * 60 * 60 * 1000)

    // Filter measurements within the last 2 days
    return sortedMeasurements.filter(measurement => {
        const measurementTime = getDateTime(measurement.date, measurement.time)
        return measurementTime >= twoDaysAgo
    })
}

const fetchData = async () => {
    try {
        // Get all stations
        const stationResponse = await axios.get('http://127.0.0.1:8000/stations/')
        const baraniStations = stationResponse.data.filter((station: any) => station.brand_name === "Allmeteo")
        
        if (!baraniStations.length) {
            console.log('No Barani stations found')
            return
        }

        // Select a random station
        const randomStation = baraniStations[Math.floor(Math.random() * baraniStations.length)]
        stationTitle.value = `Barani - ${randomStation.name}`

        // Get measurements
        const measurementsResponse = await axios.get('http://127.0.0.1:8000/measurements/')
        
        // Filter for this station's measurements
        const stationMeasurements = measurementsResponse.data.filter(
            (measurement: any) => measurement.station_name === randomStation.name
        )

        // Get last 2 days of data
        const recentMeasurements = filterLastTwoDaysData(stationMeasurements)

        // Get latest values for each measurement type
        const latestValues = {
            wind_speed: recentMeasurements.find((m: any) => m.sensor_type === 'wind_ave10')?.value || 0,
            wind_direction: recentMeasurements.find((m: any) => m.sensor_type === 'dir_ave10')?.value || 0,
            dewpoint: recentMeasurements.find((m: any) => m.sensor_type === 'dewpoint')?.value || 0,
            irradiation: recentMeasurements.find((m: any) => m.sensor_type === 'solar_irradiance')?.value || 0
        }

        // Update overview data with latest values
        overviewData.value = [
            { bg: "bg-primary", title: "Wind Speed", value: `${latestValues.wind_speed} m/s` },
            { bg: "bg-secondary", title: "Wind Direction", value: `${latestValues.wind_direction}°` },
            { bg: "bg-warning", title: "Dewpoint", value: `${latestValues.dewpoint}°C` },
            { bg: "bg-tertiary", title: "Irradiation", value: `${latestValues.irradiation}W/m2` }
        ]

        // Update chart series with moving window data
        chartSeries.value = [
            parseFloat(latestValues.wind_speed),
            parseFloat(latestValues.wind_direction),
            parseFloat(latestValues.dewpoint),
            parseFloat(latestValues.irradiation)
        ]

    } catch (error) {
        console.error('Error fetching Barani data:', error)
    }
}

// Refresh data every minute
const startDataRefresh = () => {
    fetchData() // Initial fetch
    setInterval(fetchData, 60000) // Refresh every minute
}

onMounted(startDataRefresh)
</script>