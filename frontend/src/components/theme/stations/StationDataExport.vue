<template>
  <div class="station-data-export">
    <!-- Station Name Display -->
    <div class="mb-3">
      <label class="form-label">Station Name</label>
      <input 
        type="text" 
        class="form-control" 
        :value="stationName"
        disabled
        readonly
      >
    </div>
    
    <!-- Sensor Selection -->
    <div class="sensor-selection mb-3">
      <label class="form-label">Select Sensors to Export</label>
      <div class="sensor-checkboxes">
        <div v-for="sensor in availableSensors" :key="sensor.type" class="form-check">
          <input 
            type="checkbox" 
            class="form-check-input"
            :id="sensor.type"
            v-model="selectedSensors"
            :value="sensor.type"
          >
          <label class="form-check-label" :for="sensor.type">
            {{ sensor.name }} ({{ sensor.unit }})
          </label>
        </div>
      </div>
    </div>

    <!-- Format Selection -->
    <div class="format-selection mb-3">
      <label class="form-label">Select Export Format</label>
      <div class="format-radio-group">
        <div class="form-check form-check-inline">
          <input 
            type="radio" 
            class="form-check-input"
            id="formatJson"
            value="json"
            v-model="selectedFormat"
          >
          <label class="form-check-label" for="formatJson">JSON</label>
        </div>
        <div class="form-check form-check-inline">
          <input 
            type="radio" 
            class="form-check-input"
            id="formatXml"
            value="xml"
            v-model="selectedFormat"
          >
          <label class="form-check-label" for="formatXml">XML</label>
        </div>
        <div class="form-check form-check-inline">
          <input 
            type="radio" 
            class="form-check-input"
            id="formatCsv"
            value="csv"
            v-model="selectedFormat"
          >
          <label class="form-check-label" for="formatCsv">CSV</label>
        </div>
      </div>
    </div>

    <!-- Export Button -->
    <button 
      class="btn btn-primary"
      :disabled="!canExport"
      @click="exportData"
    >
      Export Data
    </button>
  </div>
</template>

<script lang="ts" setup>
import { ref, computed } from 'vue';
import axios from 'axios';
import { toast } from 'vue3-toastify';

interface SensorConfig {
  name: string;
  unit: string;
}

interface SensorConfigs {
  [brand: string]: {
    [sensorType: string]: SensorConfig;
  };
}

interface SensorInfo {
  type: string;
  name: string;
  unit: string;
}

const props = defineProps({
  stationId: {
    type: Number,
    required: true
  },
  stationName: {
    type: String,
    required: true
  },
  sensors: {
    type: Array as () => string[],
    required: true,
    default: () => []
  },
  brand: {
    type: String,
    required: true
  }
});

// State
const selectedSensors = ref<string[]>([]);
const selectedFormat = ref('json');

// Get sensor configuration based on brand
const sensorConfigs: SensorConfigs = {
  '3D_Paws': {
    'bt1': { name: 'Temperature 1', unit: '°C' },
    'mt1': { name: 'Temperature 2', unit: '°C' },
    'bp1': { name: 'Pressure', unit: 'hPa' },
    'ws': { name: 'Wind Speed', unit: 'm/s' },
    'wd': { name: 'Wind Direction', unit: '°' },
    'rg': { name: 'Precipitation', unit: 'mm' },
    'sv1': { name: 'Downwelling Visible', unit: 'W/m²' },
    'si1': { name: 'Downwelling Infrared', unit: 'W/m²' },
    'su1': { name: 'Downwelling Ultraviolet', unit: 'W/m²' },
    'bpc': { name: 'Battery Percent', unit: '%' },
    'css': { name: 'Cell Signal Strength', unit: '%' }
  },
  'Zentra': {
    'Air Temperature': { name: 'Air Temperature', unit: '°C' },
    'Wind Speed': { name: 'Wind Speed', unit: 'm/s' },
    'Solar Radiation': { name: 'Solar Radiation', unit: 'W/m²' },
    'Precipitation': { name: 'Precipitation', unit: 'mm' },
    'Relative Humidity': { name: 'Relative Humidity', unit: '%' },
    'Atmospheric Pressure': { name: 'Atmospheric Pressure', unit: 'kPa' }
  },
  'Barani': {
    'wind_ave10': { name: 'Wind Speed (Average)', unit: 'm/s' },
    'dir_ave10': { name: 'Wind Direction (Average)', unit: '°' },
    'battery': { name: 'Battery', unit: 'V' }
  },
  'OTT': {
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
  }
};

// Get available sensors based on brand and provided sensors
const availableSensors = computed<SensorInfo[]>(() => {
  const brandConfig = sensorConfigs[props.brand] || {};
  return props.sensors.map(sensorType => ({
    type: sensorType,
    name: brandConfig[sensorType]?.name || sensorType,
    unit: brandConfig[sensorType]?.unit || ''
  }));
});

// Computed property to check if export is possible
const canExport = computed(() => selectedSensors.value.length > 0);

// Export function
const exportData = async () => {
  try {
    const response = await axios.get('/measurements/get_readings/', {
      params: {
        station_id: props.stationId,
        sensor_type: selectedSensors.value.join(',')
      },
      headers: {
        'Accept': selectedFormat.value === 'json' ? 'application/json' : 
                 selectedFormat.value === 'xml' ? 'application/xml' : 
                 'text/csv'
      },
      responseType: selectedFormat.value === 'csv' ? 'blob' : 'json'
    });

    // Handle the response based on format
    if (selectedFormat.value === 'csv') {
      // For CSV, create and trigger download
      const blob = new Blob([response.data], { type: 'text/csv' });
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = `${props.stationName}_data.csv`;
      link.click();
      window.URL.revokeObjectURL(url);
    } else {
      // For JSON/XML, trigger download
      const blob = new Blob(
        [selectedFormat.value === 'json' ? 
          JSON.stringify(response.data, null, 2) : 
          response.data
        ],
        { type: selectedFormat.value === 'json' ? 'application/json' : 'application/xml' }
      );
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = `${props.stationName}_data.${selectedFormat.value}`;
      link.click();
      window.URL.revokeObjectURL(url);
    }

    toast.success('Data exported successfully!', {
      hideProgressBar: true,
      autoClose: 2000,
      theme: 'colored'
    });
  } catch (error) {
    console.error('Error exporting data:', error);
    toast.error('Failed to export data. Please try again.', {
      hideProgressBar: true,
      autoClose: 2000,
      theme: 'colored'
    });
  }
};
</script>

<style scoped>
.station-data-export {
  padding: 1rem;
  background-color: #fff;
  border-radius: 0.5rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.sensor-checkboxes {
  max-height: 200px;
  overflow-y: auto;
  padding: 0.5rem;
  border: 1px solid #dee2e6;
  border-radius: 0.25rem;
}

.form-check {
  margin-bottom: 0.5rem;
}

.format-radio-group {
  margin-top: 0.5rem;
}

/* Style for disabled input */
.form-control:disabled {
  background-color: #f8f9fa;
  cursor: not-allowed;
  color: #495057;
  border: 1px solid #dee2e6;
}
</style> 