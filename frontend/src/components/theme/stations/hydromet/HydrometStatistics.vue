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

        <div class="dropdown-menu dropdown-menu-end position-absolute" aria-labelledby="measurementDropdown">
          <a v-for="sensor in sensorTypes" :key="sensor" class="dropdown-item" href="#" 
             @click.prevent="selectedSensorType = sensor">
            {{ sensorConfig[sensor]?.name || sensor }}
          </a>
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
import { defineAsyncComponent, ref, computed, watch, defineProps } from 'vue';
import { OTTOptions1 } from '@/core/data/chart';
import { useStationData } from '@/composables/useStationData';

const Card1 = defineAsyncComponent(() => import('@/components/common/card/CardData1.vue'));

const props = defineProps({
  selectedStation: {
    type: Number,
    required: true
  }
});

const { measurements, stationInfo, getLast24HoursMeasurements, fetchStationData, fetchLast24HoursSensorData } = useStationData();

// Define a type for the sensor keys
type SensorType = keyof typeof sensorConfig;

// Initialize with proper type
const selectedSensorType = ref<SensorType>('Air Temperature');

// Define sensor configuration with names and units for OTT sensors
const sensorConfig = {
  '5 min rain': { name: '5 min Rain', unit: 'mm' },
  'Air Temperature': { name: 'Air Temperature', unit: '°C' },
  'Barometric Pressure': { name: 'Barometric Pressure', unit: 'hPa' },
  'Baro Tendency': { name: 'Baro Tendency', unit: 'hPa' },
  'Battery': { name: 'Battery', unit: 'V' },
  'Daily Rain': { name: 'Daily Rain', unit: 'mm' },
  'Dew Point': { name: 'Dew Point', unit: '°C' },
  'Gust Direction': { name: 'Gust Direction', unit: '°' },
  'Gust Speed': { name: 'Gust Speed', unit: 'knots' },
  'Hours of Sunshine': { name: 'Hours of Sunshine', unit: 'hr' },
  'Maximum Air Temperature': { name: 'Maximum Air Temperature', unit: '°C' },
  'Minimum Air Temperature': { name: 'Minimum Air Temperature', unit: '°C' },
  'Relative Humidity': { name: 'Relative Humidity', unit: '%' },
  'Solar Radiation Avg': { name: 'Solar Radiation Average', unit: 'Wh/m²' },
  'Solar Radiation Total': { name: 'Solar Radiation Total', unit: 'Wh/m²' },
  'Wind Dir Average': { name: 'Wind Direction Average', unit: '°' },
  'Wind Dir Inst': { name: 'Wind Direction Instantaneous', unit: '°' },
  'Wind Speed Average': { name: 'Wind Speed Average', unit: 'knots' },
  'Wind Speed Inst': { name: 'Wind Speed Instantaneous', unit: 'knots' }
};
const sensorTypes = computed(() => Object.keys(sensorConfig) as SensorType[]);
const currentSensorName = computed(() => sensorConfig[selectedSensorType.value].name || selectedSensorType.value);
const currentSensorUnit = computed(() => sensorConfig[selectedSensorType.value].unit || '');

const chartData = computed(() => {
  const filteredData = getLast24HoursMeasurements.value.filter(
    measurement => measurement.sensor_type === selectedSensorType.value
  );

  if (!filteredData.length) return [];

  return [{
    name: currentSensorName.value,
    data: filteredData.map(item => ({
      x: new Date(`${item.date}T${item.time}`).getTime(),
      y: parseFloat(item.value.toString())
    }))
  }];
});

const chartOptions = computed(() => ({
  ...OTTOptions1,
  yaxis: {
    ...OTTOptions1.yaxis,
    title: {
      text: `${currentSensorName.value} (${currentSensorUnit.value})`,
      style: {
        fontSize: '14px',
        fontWeight: 500
      }
    },
    labels: {
      formatter: (val: number) => `${val.toFixed(1)} ${currentSensorUnit.value}`
    }
  },
  xaxis: {
    ...OTTOptions1.xaxis,
    labels: {
      ...OTTOptions1.xaxis.labels,
      formatter: (val: string) => {
        const date = new Date(val);
        return date.toLocaleString('en-US', {
          month: 'numeric',
          day: 'numeric',
          hour: '2-digit',
          minute: '2-digit',
          hour12: true
        });
      }
    }
  },
  tooltip: {
    x: {
      formatter: (val: number) => {
        const date = new Date(val);
        return date.toLocaleString('en-US', {
          month: 'numeric',
          day: 'numeric',
          hour: '2-digit',
          minute: '2-digit',
          hour12: true
        });
      }
    },
    y: {
      formatter: (val: number) => `${val.toFixed(1)} ${currentSensorUnit.value}`
    }
  }
}));

watch([() => props.selectedStation, () => selectedSensorType.value], 
  ([newStationId, sensorType]) => {
    if (newStationId && sensorType) {
      fetchLast24HoursSensorData(newStationId, sensorType);
    }
  }, 
  { immediate: true }
);
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
}
</style>

