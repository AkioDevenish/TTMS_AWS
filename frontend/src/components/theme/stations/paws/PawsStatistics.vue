<template>
    <Card1 colClass="col-xl-12 col-md-12 proorder-xl-2 proorder-md-2" dropdown="true" headerTitle="true" title="T01 Rawin" cardhaderClass="card-no-border pb-0">
      <div class="studay-statistics">
        <ul class="d-flex align-item-center gap-2">
          <li><span class="bg-primary"></span>Rainfall</li>
          <li><span class="bg-secondary"></span>Wind Speed</li>
        </ul>
      </div>
      <div id="study-statistics">
        <apexchart type="area" height="230" ref="chart" :options="chartOptions12" :series="paws_stats"></apexchart>
      </div>
    </Card1>
  </template>
  
  <script lang="ts" setup>
  import { defineAsyncComponent, ref, onMounted } from 'vue'
  import axios from 'axios'
  import { chartOptions12} from '@/core/data/chart'
  
  const Card1 = defineAsyncComponent(() => import("@/components/common/card/CardData1.vue"))
  const paws_stats = ref<any[]>([])
  
 const getLatestHourlyData = (data: any[]) => {
  const hourlyData: { [key: number]: { value: number; timestamp: string } } = {}

  // Group data by hour and keep the latest measurement for each hour
  data.forEach((item: any) => {
    const timestamp = new Date(item.timestamp)
    const hour = timestamp.getHours()

    // Use the timestamp to determine the latest entry for each hour
    if (!hourlyData[hour] || timestamp > new Date(hourlyData[hour].timestamp)) {
      hourlyData[hour] = { value: item.value, timestamp: item.timestamp }
    }
  })

  // Create an array with the data points in the correct order
  return Array.from({ length: 24 }, (_, i) => hourlyData[i]?.value ?? null)
}
  
const fetchData = async () => {
  try {
    const response = await axios.get('http://127.0.0.1:8000/api/instrument_measurements/')
    const instrument1Data = response.data.filter((item: any) => item.name === 'Instrument 1')
    const rainGaugeData = instrument1Data.filter((item: any) => item.measurement_name === 'Rain Gauge')
    const windSpeedData = instrument1Data.filter((item: any) => item.measurement_name === 'Wind Speed')

    const rainGaugeHourlyData = getHourlyData(rainGaugeData)
    const windSpeedHourlyData = getHourlyData(windSpeedData)

    // Dynamically generate x-axis categories from timestamps
    const rainGaugeTimestamps = rainGaugeData.map((item: any) => roundToNearestHour(item.timestamp).toISOString())
    chartOptions12.xaxis.categories = rainGaugeTimestamps // Set the categories based on the timestamp

    paws_stats.value = [
      {
        name: 'Rainfall',
        data: rainGaugeHourlyData,
      },
      {
        name: 'Wind Speed',
        data: windSpeedHourlyData,
      },
    ]
  } catch (error) {
    console.error('Error fetching data:', error)
  }
}

const roundToNearestHour = (timestamp: string) => {
  const date = new Date(timestamp)
  const minutes = date.getMinutes()

  // Round to the nearest hour
  if (minutes >= 30) {
    // Round up
    date.setHours(date.getHours() + 1)
  }

  // Set minutes and seconds to zero for uniformity
  date.setMinutes(0, 0, 0)

  return date
}

// Function to group data by hour and return the latest value for each hour
const getHourlyData = (data: any[]) => {
  const hourlyData: { [key: string]: { value: number; timestamp: string } } = {}

  data.forEach((item: any) => {
    const roundedTimestamp = roundToNearestHour(item.timestamp).toISOString()

    // Check if we need to update the value for this hour
    if (!hourlyData[roundedTimestamp] || new Date(item.timestamp) > new Date(hourlyData[roundedTimestamp].timestamp)) {
      hourlyData[roundedTimestamp] = { value: item.value, timestamp: item.timestamp }
    }
  })

  // Create an array with the data points in the correct order of timestamps
  const hourlyKeys = Object.keys(hourlyData).sort()
  return hourlyKeys.map((key) => hourlyData[key].value)
}

  
  onMounted(() => {
    fetchData()
  })
  </script>