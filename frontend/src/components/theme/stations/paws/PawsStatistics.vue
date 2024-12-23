<template>
  <Card1
    colClass="col-xl-12 col-md-12 proorder-xl-2 proorder-md-2"
    dropdown="true"
    cardhaderClass="card-no-border pb-0"
  >
    <!-- Title and Dropdown Section -->
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h4 class="mb-0">{{ selectedStationName }}</h4>
      <div class="dropdown position-relative">
        <button
          class="btn dropdown-toggle w-100 d-flex align-items-center justify-content-between"
          id="measurementDropdown"
          type="button"
          data-bs-toggle="dropdown"
          aria-expanded="false"
        >
          <span class="mx-auto">{{ selectedMeasurement || 'Select Measurement' }}</span>
          <span class="dropdown-toggle-icon ms-3"></span>
        </button>

        <div
          class="dropdown-menu dropdown-menu-end position-absolute"
          aria-labelledby="measurementDropdown"
        >
          <template v-for="(measurements, sensorType) in groupedMeasurements" :key="sensorType">
            <h6 class="dropdown-header">{{ sensorType }}</h6>
            <a
              class="dropdown-item"
              href="#"
              v-for="measurement in measurements"
              :key="measurement.id"
              @click.prevent="selectMeasurement(measurement.name)"
            >
              {{ measurement.display_name }}
            </a>
            <div class="dropdown-divider" v-if="sensorType !== lastSensorType"></div>
          </template>
        </div>
      </div>
    </div>

    <!-- Statistics Section -->
    <div class="studay-statistics mb-4">
      <div class="d-flex justify-content-end align-items-center mb-4">
        <ul class="d-flex align-items-center gap-3 mb-0">
          <li><span class="bg-primary"></span>{{ selectedMeasurement || 'No Measurement Selected' }}</li>
        </ul>
      </div>
    </div>

    <!-- Chart Section -->
    <div class="chart-container">
      <apexchart
        v-if="paws_stats.length > 0"
        type="area"
        height="330"
        ref="chart"
        :options="pawsOptions"
        :series="paws_stats"
      ></apexchart>
      <div v-else>
        <p>No data available to display.</p>
      </div>
    </div>

    <!-- Example using a simple alert -->
    <div v-if="errorMessage" class="alert alert-danger">
      {{ errorMessage }}
    </div>
  </Card1>
</template>

<script lang="ts" setup>
import { defineAsyncComponent, ref, reactive, onMounted, watch, computed } from 'vue';
import axios from 'axios';
import { pawsOptions1 as initialPawsOptions1 } from '@/core/data/chart';

// Define the props expected from the parent component
const props = defineProps({
  selectedStation: {
    type: Number,
    required: true
  }
});

// Ref to store the selected station's name
const selectedStationName = ref<string>('');

// Async component import
const Card1 = defineAsyncComponent(() => import('@/components/common/card/CardData1.vue'));
const paws_stats = ref<any[]>([]);

// Selected measurement and its units
const selectedMeasurement = ref<string>(''); // Initially no measurement selected

const measurementUnits: Record<string, string> = {
  'BMX280 Temperature': '°C',
  'MCP9808 Temperature': '°C',
  'Wind Speed': 'm/s',
  'Wind Direction': '°',
  'Rain Gauge': 'mm',
  'BMX280 Pressure': 'hPa',
  'SI1145 Visible': 'lux',
  'SI1145 Infrared': 'lux',
  'SI1145 Ultraviolet': 'UV Index',
  'Battery Percent Charge': '%',
  'Cell Signal Strength': 'dBm'
};

// Reactive options for the chart
const pawsOptions1 = reactive({ ...initialPawsOptions1 });

// Fetch sensor types
const sensorTypes = ref<any[]>([]);
const fetchSensorTypes = async () => {
  try {
    const response = await axios.get<any[]>('http://127.0.0.1:8000/sensors/');
    sensorTypes.value = response.data;
  } catch (error) {
    console.error('Error fetching sensor types:', error);
  }
};

// Fetch all measurements
const allMeasurements = ref<any[]>([]);
const fetchAllMeasurements = async () => {
  try {
    const response = await axios.get<any[]>('http://127.0.0.1:8000/api/measurements/');
    allMeasurements.value = response.data;
  } catch (error) {
    console.error('Error fetching all measurements:', error);
  }
};

// Compute grouped measurements by sensor type
const groupedMeasurements = computed(() => {
  const grouped: Record<string, any[]> = {};
  if (!sensorTypes.value || sensorTypes.value.length === 0) return grouped;

  // Create a mapping of sensor types to their measurements
  sensorTypes.value.forEach(sensor => {
    const measurements = allMeasurements.value.filter(
      measurement => measurement.sensor.type === sensor.type
    );
    if (measurements.length > 0) {
      grouped[sensor.type] = measurements;
    }
  });

  return grouped;
});

// Get the last sensor type for handling dividers
const lastSensorType = computed(() => {
  const types = Object.keys(groupedMeasurements.value);
  return types.length > 0 ? types[types.length - 1] : '';
});

// Initialize data by fetching sensor types and measurements
const initializeData = async () => {
  await Promise.all([fetchSensorTypes(), fetchAllMeasurements()]);
};

// Adjust to UTC+3
const adjustToTimeZone = (timestamp: string, offset: number = 3) => {
  const date = new Date(timestamp);
  const timeZoneAdjustedDate = new Date(date.getTime() + offset * 60 * 60 * 1000); // Offset in hours
  return timeZoneAdjustedDate;
};

// Round timestamp to the nearest hour, adjusting for a specific offset
const roundToNearestHour = (timestamp: string, offset: number = 3) => {
  const date = adjustToTimeZone(timestamp, offset);
  const minutes = date.getMinutes();
  if (minutes >= 30) {
    date.setHours(date.getHours() + 1);
  }
  date.setMinutes(0, 0, 0); // Round minutes to zero
  return date.getTime(); // Return as Unix timestamp (milliseconds)
};

// Format timestamp for display
const formatTimestamp = (timestamp: number) => {
  const date = new Date(timestamp);
  return date.toLocaleString('en-US', {
    hour: '2-digit',
    minute: '2-digit',
    hour12: true,
    day: 'numeric',
    month: 'numeric',
    year: 'numeric'
  });
};

// Aggregate hourly data by rounding timestamps to the nearest hour
const getHourlyData = (data: any[]) => {
  const hourlyData: { [key: string]: { value: number; timestamp: number } } = {};
  data.forEach((item: any) => {
    const roundedTimestamp = roundToNearestHour(item.timestamp, 3);
    if (!hourlyData[roundedTimestamp] || new Date(item.timestamp) > new Date(hourlyData[roundedTimestamp].timestamp)) {
      hourlyData[roundedTimestamp] = { value: item.value, timestamp: item.timestamp };
    }
  });
  const hourlyKeys = Object.keys(hourlyData).sort();
  return hourlyKeys.map((key) => hourlyData[key].value);
};

// Fetch station details to get the station's name
const fetchStationDetails = async () => {
  try {
    const response = await axios.get(`http://127.0.0.1:8000/stations/${props.selectedStation}/`);
    if (response.status === 200 && response.data) {
      selectedStationName.value = response.data.name;
    } else {
      console.warn('No data found for the selected station.');
      selectedStationName.value = 'Unknown Station';
    }
  } catch (error) {
    console.error('Error fetching station details:', error);
    selectedStationName.value = 'Error Fetching Station';
  }
};

const isLoading = ref<boolean>(false);
const errorMessage = ref<string>('');

// Fetch data and update chart based on the selected station and measurement
const fetchData = async () => {
  isLoading.value = true;
  try {
    const response = await axios.get('http://127.0.0.1:8000/api/measurements/');
    const currentUnit = measurementUnits[selectedMeasurement.value] || '';
    const instrumentData = response.data.filter((item: any) =>
      item.station_id === props.selectedStation && item.name === selectedMeasurement.value
    );

    if (instrumentData.length === 0) {
      console.warn('No data found for selected instrument and measurement');
      pawsOptions1.xaxis.categories = [];
      paws_stats.value = [];
      return;
    }

    const hourlyData = getHourlyData(instrumentData);

    pawsOptions1.yaxis.labels.formatter = (val: number) => `${val.toFixed(2)} ${currentUnit}`;
    pawsOptions1.yaxis.title.text = `${selectedMeasurement.value} (${currentUnit})`;
    pawsOptions1.tooltip.y.formatter = (val: number) => `${val.toFixed(2)} ${currentUnit}`;

    paws_stats.value = [
      {
        name: selectedMeasurement.value,
        data: hourlyData
      }
    ];

    pawsOptions1.xaxis.categories = instrumentData.map((item: { timestamp: string }) => {
      const roundedTime = roundToNearestHour(item.timestamp, 3);
      return formatTimestamp(roundedTime);
    });
  } catch (error: any) {
    console.error('Error fetching data:', error);
    pawsOptions1.xaxis.categories = [];
    paws_stats.value = [];
    errorMessage.value = 'Failed to load data. Please try again later.';
  } finally {
    isLoading.value = false;
  }
};

// Handler for dropdown selection
const selectMeasurement = (measurement: string) => {
  selectedMeasurement.value = measurement;
};

// Watch for changes to selectedStation prop and selectedMeasurement
watch(
  () => props.selectedStation,
  async (newStation, oldStation) => {
    await fetchStationDetails();
    fetchData();
  },
  { immediate: true }
);

watch(selectedMeasurement, fetchData);

// Initial data load on component mount
onMounted(async () => {
  await initializeData();
  await fetchStationDetails();
  fetchData();
});

// Computed properties for pawsOptions (chart configuration)
const pawsOptions = computed(() => {
  const currentUnit = measurementUnits[selectedMeasurement.value] || '';

  return {
    ...pawsOptions1,
    yaxis: {
      ...pawsOptions1.yaxis,
      labels: {
        ...pawsOptions1.yaxis.labels,
        formatter: (val: number) => `${val.toFixed(2)} ${currentUnit}`
      },
      title: {
        ...pawsOptions1.yaxis.title,
        text: `${selectedMeasurement.value} (${currentUnit})`
      }
    },
    tooltip: {
      ...pawsOptions1.tooltip,
      y: {
        ...pawsOptions1.tooltip.y,
        formatter: (val: number) => `${val.toFixed(2)} ${currentUnit}`
      }
    }
  };
});
</script>

<style scoped>
.studay-statistics {
  margin-top: 45px;
}

.dropdown-menu {
  margin-top: 10px;
  z-index: 100;
}
</style>
