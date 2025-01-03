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
          <a class="dropdown-item" href="#" @click.prevent="selectMeasurement('wind_ave10')">Wind Speed (Average)</a>
          <a class="dropdown-item" href="#" @click.prevent="selectMeasurement('dir_ave10')">Wind Direction (Average)</a>
          <a class="dropdown-item" href="#" @click.prevent="selectMeasurement('battery')">Battery</a>
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
import { baraniOptions1 } from '@/core/data/chart';

const Card1 = defineAsyncComponent(() => import('@/components/common/card/CardData1.vue'));


const props = defineProps({
  selectedStation: {
    type: Number,
    required: true
  }
});

const chartData = ref<any[]>([]);
const selectedSensorType = ref<string>('wind_ave10');
const stationInfo = ref<any>(null);

// Mapping of sensor types to display names and units
const sensorConfig: Record<string, { name: string; unit: string }> = {
  'battery': { name: 'Battery', unit: 'V' },
  'wind_ave10': { name: 'Wind Speed (Average)', unit: 'm/s' },
  'wind_max10': { name: 'Wind Speed (Max)', unit: 'm/s' },
  'wind_min10': { name: 'Wind Speed (Min)', unit: 'm/s' },
  'dir_ave10': { name: 'Wind Direction (Average)', unit: '°' },
  'dir_max10': { name: 'Wind Direction (Max)', unit: '°' },
  'dir_hi10': { name: 'Wind Direction (High)', unit: '°' },
  'dir_lo10': { name: 'Wind Direction (Low)', unit: '°' }
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
  ...baraniOptions1,
  yaxis: {
    ...baraniOptions1.yaxis,
    title: {
      ...baraniOptions1.yaxis.title,
      text: `${currentSensorName.value} (${currentSensorUnit.value})`,
      style: {
        ...baraniOptions1.yaxis.title.style,
        fontSize: '14px',
        fontWeight: 500
      }
    },
    labels: {
      ...baraniOptions1.yaxis.labels,
      formatter: (val: number) => `${val.toFixed(1)} ${currentSensorUnit.value}`
    }
  },
  xaxis: {
    ...baraniOptions1.xaxis,
    labels: {
      ...baraniOptions1.xaxis.labels,
      formatter: (val: string) => formatTimestamp(val)
    }
  },
  tooltip: {
    ...baraniOptions1.tooltip,
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

    // Get measurements using the station-specific endpoint
    const measurementsResponse = await axios.get(`http://127.0.0.1:8000/measurements/by_station/?station_id=${props.selectedStation}`);
    console.log('All measurements:', measurementsResponse.data);
    
    // Filter measurements for current station and selected sensor type
    const filteredData = measurementsResponse.data.filter((measurement: any) => 
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