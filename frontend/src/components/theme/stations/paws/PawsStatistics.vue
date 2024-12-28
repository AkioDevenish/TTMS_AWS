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
import { defineAsyncComponent, ref, reactive, onMounted, watch, computed, defineProps, onUnmounted } from 'vue';
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
const selectedSensorType = ref<string>('bt1');
const sensors = ref<any[]>([]);
const stationInfo = ref<any>(null);

// Mapping of sensor types to display names and units
const sensorConfig: Record<string, { name: string; unit: string }> = {
  'bp1': { name: 'Pressure', unit: 'hPa' },
  'bt1': { name: 'Temperature 1', unit: '°C' },
  'mt1': { name: 'Temperature 2', unit: '°C' },
  'ws': { name: 'Wind Speed', unit: 'm/s' },
  'wd': { name: 'Wind Direction', unit: '°' },
  'rg': { name: 'Precipitation', unit: 'mm' },
  'sv1': { name: 'Downwelling Visible', unit: 'W/m²' },
  'si1': { name: 'Downwelling Infrared', unit: 'W/m²' },
  'su1': { name: 'Downwelling Ultraviolet', unit: 'W/m²' },
  'bpc': { name: 'Battery Percent', unit: '%' },
  'css': { name: 'Cell Signal Strength', unit: '%' }
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

// Declare fetchData function before using it in watchers
const fetchData = async () => {
  try {
    if (!props.selectedStation) {
      console.log('No station selected');
      return;
    }

    // Get station info and measurements in parallel
    const [stationResponse, measurementsResponse] = await Promise.all([
      axios.get('http://127.0.0.1:8000/stations/'),
      axios.get(`http://127.0.0.1:8000/measurements/by_station/?station_id=${props.selectedStation}`)
    ]);

    const currentStation = stationResponse.data.find((station: any) => station.id === props.selectedStation);
    if (!currentStation) {
      console.log('Station not found');
      return;
    }
    stationInfo.value = currentStation;
    console.log('Station info:', currentStation);

    if (!measurementsResponse.data || measurementsResponse.data.length === 0) {
      console.log('No measurements found for station');
      chartData.value = [];
      return;
    }

    // Filter measurements for selected sensor type only
    const filteredData = measurementsResponse.data.filter((measurement: any) => 
      measurement.sensor_type === selectedSensorType.value
    );

    console.log('Filtered measurements:', filteredData);

    if (filteredData.length === 0) {
      console.log('No measurements found for selected sensor type:', selectedSensorType.value);
      chartData.value = [];
      return;
    }

    // Sort and transform data for the chart
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
  await fetchData();
};

// Single watcher for station changes with immediate option
watch(() => props.selectedStation, (newStation) => {
  console.log('Station changed in PawsStatistics:', newStation);
  if (newStation) {
    fetchData();
  }
}, { immediate: true });

// Add auto-refresh interval
let refreshInterval: number | undefined;

onMounted(() => {
  refreshInterval = setInterval(fetchData, 60000);
});

onUnmounted(() => {
  if (refreshInterval) {
    clearInterval(refreshInterval);
  }
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

