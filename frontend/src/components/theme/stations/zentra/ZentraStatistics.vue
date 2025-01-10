<template>
	<Card1 colClass="col-xl-12 col-md-12 proorder-xl-2 proorder-md-2" dropdown="true" headerTitle="true" title="z6-26732" cardhaderClass="card-no-border pb-0">
		<div class="studay-statistics">
			<ul class="d-flex align-item-center gap-2">
				<li><span class="bg-primary"></span>Rainfall (mm)</li>
				<li><span class="bg-secondary"></span>Wind Speed (m/s)</li>
			</ul>
		</div>
		<div id="study-statistics">
			<apexchart type="area" height="230" ref="chart" :options="chartOptions12" :series="zentrastats"></apexchart>
		</div>
	</Card1>
</template>

<script lang="ts" setup>
import { defineAsyncComponent, ref, onMounted } from 'vue'
import axios from 'axios'
import { chartOptions12 } from "@/core/data/chart"

const Card1 = defineAsyncComponent(() => import("@/components/common/card/CardData1.vue"))
const zentrastats = ref<any[]>([])

// Keep the original sensor name mapping
const sensorNameMapping = {
	'Solar Radiation': 'Solar Radiation (W/m²)',
	'Precipitation': 'Precipitation (mm)',
	'Lightning Activity': 'Lightning Activity (Yes/No)',
	'Lightning Distance': 'Lightning Distance (km)',
	'Wind Direction': 'Wind Direction (°)',
	'Wind Speed': 'Wind Speed (m/s)',
	'Gust Speed': 'Gust Speed (m/s)',
	'Air Temperature': 'Air Temperature (°C)',
	'Relative Humidity': 'Relative Humidity (%)',
	'Atmospheric Pressure': 'Atmospheric Pressure (kPa)',
	'X-axis Level': 'X-axis Level (°)',
	'Y-axis Level': 'Y-axis Level (°)',
	'Max Precipitation Rate': 'Max Precipitation Rate (mm/h)',
	'RH Sensor Temperature': 'RH Sensor Temperature (°C)',
	'Vapor Pressure Deficit': 'Vapor Pressure Deficit (kPa)',
	'Battery Percent': 'Battery Percent (%)',
	'Battery Voltage': 'Battery Voltage (mV)',
	'Atmospheric Pressure (Reference Pressure)': 'Atmospheric Pressure (Reference Pressure) (kPa)',
};

// Keep the original utility functions
const roundToNearestHour = (timestamp: string) => {
	const date = new Date(timestamp)
	const minutes = date.getMinutes()

	if (minutes >= 30) {
		date.setHours(date.getHours() + 1)
	}

	date.setMinutes(0, 0, 0)

	return date
}

// Keep the original getHourlyData function
const getHourlyData = (data: any[]) => {
	const hourlyData: { [key: string]: { rain: number, wind: number, timestamp: string, sensors: any[] } } = {}

	data.forEach((item: any) => {
		const roundedTimestamp = roundToNearestHour(item.timestamp).toISOString()

		// Initialize the hour slot if it doesn't exist
		if (!hourlyData[roundedTimestamp]) {
			hourlyData[roundedTimestamp] = { rain: 0, wind: 0, timestamp: roundedTimestamp, sensors: [] }
		}

		// Add sensor data to the hourly data
		const sensorData = {
			name: item.sensor_name,
			value: item.value,
			units: item.units,
		}

		// Push the sensor data into the respective hour
		hourlyData[roundedTimestamp].sensors.push(sensorData)

		// Handle Rainfall (mm) - Store rainfall value
		if (item.sensor_name === 'Precipitation' && item.units === ' mm') {
			hourlyData[roundedTimestamp].rain += item.value
		}
		// Handle Wind Speed (m/s) - Store wind speed value
		else if (item.sensor_name === 'Wind Speed' && item.units === ' m/s') {
			hourlyData[roundedTimestamp].wind += item.value
		}
	})

	// Create the array of hourly values for Rainfall and Wind Speed
	const hourlyKeys = Object.keys(hourlyData).sort()

	const rainData = hourlyKeys.map((key) => hourlyData[key].rain)
	const windData = hourlyKeys.map((key) => hourlyData[key].wind)
	const timeStamps = hourlyKeys

	return {
		rainData,
		windData,
		timeStamps,
		sensors: hourlyKeys.map((key) => {
			return hourlyData[key].sensors.map(sensor => ({
				name: sensorNameMapping[sensor.name] || sensor.name,
				value: sensor.value,
				units: sensor.units,
			}))
		})
	}
}

// Main data fetching function
const fetchData = async () => {
	try {
		const response = await axios.get('http://167.88.45.83/api/allmeteo/measurements/')

		// Get hourly data for Rainfall and Wind Speed
		const { rainData, windData, timeStamps, sensors } = getHourlyData(response.data)

		// Update chart x-axis categories (timestamps)
		chartOptions12.xaxis.categories = timeStamps

		// Update chart series for Rainfall and Wind Speed
		zentrastats.value = [
			{
				name: 'Rainfall',
				data: rainData,
			},
			{
				name: 'Wind Speed',
				data: windData,
			},
		]

		// Log sensor data for debugging
		console.log('Sensors:', sensors)
	} catch (error) {
		console.error('Error fetching data:', error)
	}
}

// Fetch data when component is mounted
onMounted(() => {
	fetchData()
})
</script>