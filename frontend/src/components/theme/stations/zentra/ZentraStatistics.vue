<template>
  <Card1
    colClass="col-xl-12 col-md-12 proorder-xl-2 proorder-md-2"
    dropdown="true"
    cardhaderClass="card-no-border pb-0"
  >
    <!-- Title and Dropdown Section -->
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h4 class="mb-0">{{ stationInfo?.name || 'Station Statistics' }}</h4>
      <div class="dropdown position-relative">
        <button
          class="btn dropdown-toggle w-100 d-flex align-items-center justify-content-between"
          id="measurementDropdown"
          type="button"
          data-bs-toggle="dropdown"
          aria-expanded="false"
        >
          <span class="mx-auto">{{ currentSensorName }}</span>
          <span class="dropdown-toggle-icon ms-3"></span>
        </button>

        <div
          class="dropdown-menu dropdown-menu-end position-absolute"
          aria-labelledby="measurementDropdown"
        >
     
          <a class="dropdown-item" href="#" @click.prevent="selectMeasurement('Precipitation')">Precipitation</a>
          <a class="dropdown-item" href="#" @click.prevent="selectMeasurement('Wind Speed')">Wind Speed</a>
          <a class="dropdown-item" href="#" @click.prevent="selectMeasurement('Gust Speed')">Gust Speed</a>
          <a class="dropdown-item" href="#" @click.prevent="selectMeasurement('Wind Direction')">Wind Direction</a>
          <a class="dropdown-item" href="#" @click.prevent="selectMeasurement('Lightning Activity')">Lightning Activity</a>
          <a class="dropdown-item" href="#" @click.prevent="selectMeasurement('Lightning Distance')">Lightning Distance</a>
          <a class="dropdown-item" href="#" @click.prevent="selectMeasurement('Solar Radiation')">Solar Radiation</a>
          <a class="dropdown-item" href="#" @click.prevent="selectMeasurement('Air Temperature')">Air Temperature</a>
          <a class="dropdown-item" href="#" @click.prevent="selectMeasurement('Relative Humidity')">Relative Humidity</a>
          <a class="dropdown-item" href="#" @click.prevent="selectMeasurement('Atmospheric Pressure')">Atmospheric Pressure</a>
          <a class="dropdown-item" href="#" @click.prevent="selectMeasurement('X-axis Level')">X-axis Level</a>
          <a class="dropdown-item" href="#" @click.prevent="selectMeasurement('Y-axis Level')">Y-axis Level</a>
          <a class="dropdown-item" href="#" @click.prevent="selectMeasurement('Max Precipitation Rate')">Max Precipitation Rate</a>
          <a class="dropdown-item" href="#" @click.prevent="selectMeasurement('RH Sensor Temperature')">RH Sensor Temperature</a>
          <a class="dropdown-item" href="#" @click.prevent="selectMeasurement('Vapor Pressure Deficit')">Vapor Pressure Deficit</a>
          <a class="dropdown-item" href="#" @click.prevent="selectMeasurement('Battery Percent')">Battery Percent</a>
          <a class="dropdown-item" href="#" @click.prevent="selectMeasurement('Battery Voltage')">Battery Voltage</a>
          <a class="dropdown-item" href="#" @click.prevent="selectMeasurement('Reference Pressure')">Reference Pressure</a>
        </div>
      </div>
    </div>

    <!-- Chart Section -->
    <div class="chart-container">
      <apexchart
        v-if="chartData.length > 0"
        type="area"
        height="330"
        ref="chart"
        :options="chartOptions"
        :series="chartData"
      ></apexchart>
      <div v-else>
        <p>No data available to display.</p>
      </div>
    </div>
  </Card1>
</template>

<script lang="ts" setup>
import { defineAsyncComponent, ref, reactive, onMounted, watch, computed, defineProps } from 'vue';
import axios from 'axios';
import { zentraOptions1 } from '@/core/data/chart';

const Card1 = defineAsyncComponent(() => import('@/components/common/card/CardData1.vue'));

const props = defineProps({
  selectedStation: {
    type: Number,
    required: true
  }
});

const chartData = ref<any[]>([]);
const selectedSensorType = ref<string>('Air Temperature');
const sensors = ref<any[]>([]);
const stationInfo = ref<any>(null);

// Mapping of sensor types to units only
const sensorConfig: Record<string, { unit: string }> = {
  'Solar Radiation': { unit: 'W/m²' },
  'Precipitation': { unit: 'mm' },
  'Lightning Activity': { unit: 'binary' },
  'Lightning Distance': { unit: 'km' },
  'Wind Direction': { unit: '°' },
  'Wind Speed': { unit: 'm/s' },
  'Gust Speed': { unit: 'm/s' },
  'Air Temperature': { unit: '°C' },
  'Relative Humidity': { unit: '%' },
  'Atmospheric Pressure': { unit: 'kPa' },
  'X-axis Level': { unit: '°' },
  'Y-axis Level': { unit: '°' },
  'Max Precipitation Rate': { unit: 'mm/h' },
  'RH Sensor Temperature': { unit: '°C' },
  'Vapor Pressure Deficit': { unit: 'kPa' },
  'Battery Percent': { unit: '%' },
  'Battery Voltage': { unit: 'mV' },
  'Reference Pressure': { unit: 'kPa' }
};

// Format timestamp for display
const formatTimestamp = (timestamp: string) => {
  const date = new Date(timestamp);
  return date.toLocaleString('en-US', {
    month: 'numeric',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
    hour12: true
  });
};

// Get the current sensor's display name
const currentSensorName = computed(() => {
  return selectedSensorType.value;
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
      ...zentraOptions1.yaxis.title,
      text: `${currentSensorName.value} (${currentSensorUnit.value})`,
      style: {
        ...zentraOptions1.yaxis.title.style,
        fontSize: '14px',
        fontWeight: 500
      }
    },
    labels: {
      ...zentraOptions1.yaxis.labels,
      formatter: (val: number) => `${val.toFixed(1)} ${currentSensorUnit.value}`
    }
  },
  xaxis: {
    ...zentraOptions1.xaxis,
    labels: {
      ...zentraOptions1.xaxis.labels,
      formatter: (val: string) => formatTimestamp(val)
    }
  },
  tooltip: {
    ...zentraOptions1.tooltip,
    y: {
      formatter: (val: number) => `${val.toFixed(1)} ${currentSensorUnit.value}`
    }
  }
}));

// Fetch all required data
const fetchData = async () => {
  try {
    console.log('Fetching data for station:', props.selectedStation);
    
    // Get station info
    const stationResponse = await axios.get('http://127.0.0.1:8000/stations/');
    const currentStation = stationResponse.data.find((station: any) => station.id === props.selectedStation);
    if (!currentStation) {
      console.log('Station not found');
      return;
    }
    stationInfo.value = currentStation;
    console.log('Station info:', currentStation);

    // Get measurements
    const measurementsResponse = await axios.get('http://127.0.0.1:8000/measurements/');
    console.log('All measurements:', measurementsResponse.data);
    
    // Filter measurements for current station and selected sensor type
    const filteredData = measurementsResponse.data.filter((measurement: any) => 
      measurement.station_name === currentStation.name && 
      measurement.sensor_type === selectedSensorType.value
    );

    console.log('Filtered measurements:', filteredData);

    if (filteredData.length === 0) {
      console.log('No measurements found for selected sensor type:', selectedSensorType.value);
      chartData.value = [];
      return;
    }

    // Sort data by date and time
    const sortedData = filteredData.sort((a: any, b: any) => {
      const dateA = new Date(`${a.date}T${a.time}`);
      const dateB = new Date(`${b.date}T${b.time}`);
      return dateA.getTime() - dateB.getTime();
    });

    // Transform data for the chart
    chartData.value = [{
      name: currentSensorName.value,
      data: sortedData.map((item: any) => ({
        x: new Date(`${item.date}T${item.time}`).getTime(),
        y: parseFloat(item.value)
      }))
    }];

    console.log('Chart data updated:', chartData.value);
  } catch (error) {
    console.error('Error fetching data:', error);
    if (axios.isAxiosError(error)) {
      console.error('Response status:', error.response?.status);
      console.error('Response data:', error.response?.data);
    }
    chartData.value = [];
  }
};

// Handler for measurement selection
const selectMeasurement = async (sensorType: string) => {
  selectedSensorType.value = sensorType;
  await fetchData(); // Fetch new data for the selected sensor type
};

// Watch for changes to station only, not sensor type
watch(() => props.selectedStation, () => {
  fetchData();
});

// Initial data load
onMounted(() => {
  fetchData();
});
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