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
             @click.prevent="selectMeasurement(sensor)">
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
import { zentraOptions1 } from '@/core/data/chart';
import { useStationData } from '@/composables/useStationData';

const Card1 = defineAsyncComponent(() => import('@/components/common/card/CardData1.vue'));

const props = defineProps({
  selectedStation: {
    type: Number,
    required: true
  }
});

const { measurements, stationInfo, getLast24HoursMeasurements, fetchStationData } = useStationData();
const selectedSensorType = ref<string>('Air Temperature');
const chartData = ref<any[]>([]);

// Sensor configuration
const sensorConfig: Record<string, { name: string; unit: string }> = {
  'Solar Radiation': { name: 'Solar Radiation', unit: 'W/m²' },
  'Precipitation': { name: 'Precipitation', unit: 'mm' },
  'Wind Speed': { name: 'Wind Speed', unit: 'm/s' },
  'Air Temperature': { name: 'Air Temperature', unit: '°C' },
  'Relative Humidity': { name: 'Relative Humidity', unit: '%' },
  'Atmospheric Pressure': { name: 'Atmospheric Pressure', unit: 'kPa' }
};

const sensorTypes = computed(() => Object.keys(sensorConfig));
const currentSensorName = computed(() => sensorConfig[selectedSensorType.value]?.name || selectedSensorType.value);
const currentSensorUnit = computed(() => sensorConfig[selectedSensorType.value]?.unit || '');

const selectMeasurement = (type: string) => {
  selectedSensorType.value = type;
};

const chartOptions = computed(() => ({
  ...zentraOptions1,
  yaxis: {
    ...zentraOptions1.yaxis,
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
    ...zentraOptions1.xaxis,
    type: 'datetime',
    labels: {
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

// Watch for station changes
watch(() => props.selectedStation, (newStationId) => {
  if (newStationId) {
    console.log('Fetching data for station:', newStationId);
    fetchStationData(newStationId);
  }
}, { immediate: true });

// Watch for data changes
watch([() => getLast24HoursMeasurements.value, () => selectedSensorType.value], 
  ([newMeasurements, newSensorType]) => {
    console.log('New measurements:', newMeasurements);
    console.log('Selected sensor type:', newSensorType);
    
    if (!newMeasurements?.length) {
      console.log('No measurements available');
      chartData.value = [];
      return;
    }

    const filteredData = newMeasurements.filter(
      measurement => measurement.sensor_type === newSensorType
    );
    
    console.log('Filtered data:', filteredData);

    if (!filteredData.length) {
      console.log('No data for selected sensor type');
      chartData.value = [];
      return;
    }

    chartData.value = [{
      name: sensorConfig[newSensorType]?.name || newSensorType,
      data: filteredData.map(item => ({
        x: new Date(`${item.date}T${item.time}`).getTime(),
        y: parseFloat(item.value.toString())
      }))
    }];
    
    console.log('Chart data:', chartData.value);
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



