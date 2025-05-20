<template>
    <!-- Move Card1 to be the second component -->
    <div class="order-2">
        <Card1
        colClass="col-xl-12 col-md-12 proorder-xl-2 proorder-md-2 mb-30"
            headerTitle="true" 
            title="Station Overview"
            cardHeaderClass="card-no-border pb-0"
            cardBodyClass="designer-card"
        >
        
            <!-- Brand tabs and sensor dropdown in one row -->
            <div class="d-flex flex-wrap justify-content-between align-items-center mb-4">
                <ul class="nav nav-tabs border-tab mb-2 mb-md-0 nav-primary" id="brand-tabs" role="tablist">
                    <li class="nav-item" v-for="brand in uniqueBrandsData" :key="brand">
                        <button
                            class="nav-link"
                            :class="{ active: selectedBrand === brand }"
                            @click="selectBrand(brand)"
                            type="button"
                        >
                            {{ brand.replace('_', ' ') }}
                        </button>
                    </li>
                </ul>
                
                <!-- Improved sensor type selection dropdown -->
                <div class="sensor-dropdown" v-if="sensorConfig && Object.keys(sensorConfig).length">
                    <div class="dropdown w-100">
                        <button
                            class="btn btn-outline-primary dropdown-toggle w-100 text-truncate"
                            type="button"
                            id="sensorTypeDropdown"
                            data-bs-toggle="dropdown"
                            aria-expanded="false"
                        >
                            <span class="sensor-name">{{ sensorConfig[selectedSensorType]?.name || selectedSensorType }}</span>
                        </button>
                        <ul class="dropdown-menu dropdown-menu-end w-100" aria-labelledby="sensorTypeDropdown">
                            <li v-for="sensor in availableSensors" :key="sensor.value">
                                <a class="dropdown-item" href="#" @click.prevent="selectSensorType(sensor.value)">
                                    {{ sensor.label }}
                                </a>
                            </li>
                        </ul>
                    </div>
                </div>
            </div>

      
            <!-- Loading Indicator -->
            <div v-if="isLoading" class="text-center py-5">
                <div class="spinner-border text-primary" role="status">
                    <span class="visually-hidden">Loading...</span>
                </div>
            </div>

            <!-- No Results Message -->
            <div v-else-if="!pawsStations || pawsStations.length === 0" class="text-center py-5">
                <div class="empty-state">
                    <VueFeather type="alert-circle" size="48" class="text-muted mb-3" />
                    <h5>No Data Available</h5>
                    <p class="text-muted">No stations found for the selected brand and sensor type.</p>
                </div>
            </div>

            <!-- Station Cards with Virtual Scrolling -->
            <div v-else class="row g-3" ref="stationContainer">
                <div v-for="station in visibleStations" :key="station.id" class="col-xl-4 col-lg-6 col-md-6">
                    <div class="card station-card h-100">
                        <div class="card-body">
                            <div class="d-flex justify-content-between align-items-center mb-3">
                                <h5 class="card-title mb-0">{{ station.name }}</h5>
                                <span :class="getStatusClass(station)">
                                    {{ getStatusText(station) }}
                                </span>
                            </div>
                            <div class="station-info">
                                <p class="mb-2">
                                    <VueFeather :type="currentSensorIcon" size="16" class="me-2" />
                                    {{ formatValue(station.latest_measurement?.value) }}
                                </p>
                                <p class="mb-2 text-muted">
                                    <small>Last Updated: {{ formatDateTime(station.latest_measurement) }}</small>
                                </p>
                            </div>
                            <div class="chart-container">
                                <apexchart
                                    v-if="station.chartData && station.chartData[0].data.length > 0"
                                    type="area"
                                    height="160"
                                    :options="getChartOptions(station.sensor_unit, selectedSensorType)"
                                    :series="station.chartData"
                                ></apexchart>
                                <div v-else class="no-data-placeholder">
                                    <p>No historical data available</p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Pagination -->
            <ul class="pagination mx-3 mt-3 justify-content-end" v-if="pawsStations && pawsStations.length > 0">
                <li class="page-item" :class="{ disabled: currentPage === 1 || isLoading }">
                    <a class="page-link cursor-pointer" @click="prev">Previous</a>
                </li>
                <li class="page-item" v-for="i in totalPages" :key="i" 
                    :class="{ active: i === currentPage }">
                    <a class="page-link cursor-pointer" @click="() => {
                        currentPage = i;
                        fetchStationData();
                    }">{{ i }}</a>
                </li>
                <li class="page-item" :class="{ disabled: currentPage === totalPages || isLoading }">
                    <a class="page-link cursor-pointer" @click="next">Next</a>
                </li>
            </ul>
        </Card1>
    </div>
</template>

<script setup>
import { defineAsyncComponent, ref, onMounted, watch, computed, onUnmounted } from 'vue';
import { useStationOverviewStore } from '@/store/stationOverview';
import { useIntersectionObserver } from '@vueuse/core';
import VueFeather from "vue-feather";
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import { library } from '@fortawesome/fontawesome-svg-core';
import { 
  faTemperatureHalf, 
  faWind, 
  faCompass, 
  faCloudRain, 
  faGauge, 
  faSun, 
  faTemperatureHigh,
  faBatteryHalf,
  faSignal,
  faDroplet
} from '@fortawesome/free-solid-svg-icons';

// Register FontAwesome icons
library.add(
  faTemperatureHalf, 
  faWind, 
  faCompass, 
  faCloudRain, 
  faGauge, 
  faSun, 
  faTemperatureHigh,
  faBatteryHalf,
  faSignal,
  faDroplet
);

// Import Card component
const Card1 = defineAsyncComponent(() => import('@/components/common/card/CardData1.vue'));

// Initialize store
const store = useStationOverviewStore();

// Initialize reactive variables
const uniqueBrandsData = ref(['3D_Paws', 'Allmeteo', 'Zentra']); // Pre-populate with known brands
const stationContainer = ref(null);
const visibleStations = ref([]);
let refreshIntervalId = null;

// Add fetchStationData method
const fetchStationData = (isRefresh = false) => {
  store.fetchStationData(isRefresh);
};

// Computed properties
const selectedBrand = computed({
  get: () => store.selectedBrand,
  set: (value) => store.setBrand(value)
});

const selectedSensorType = computed({
  get: () => store.selectedSensorType,
  set: (value) => store.setSensorType(value)
});

const currentPage = computed({
  get: () => store.currentPage,
  set: (value) => store.setPage(value)
});

const totalPages = computed(() => store.totalPages);
const isLoading = computed(() => store.isLoading);
const pawsStations = computed(() => store.stations || []);

// Sensor configuration for each brand
const sensorConfigs = {
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
  'Allmeteo': {
    'wind_ave10': { name: 'Wind Speed (Average)', unit: 'm/s' },
    'dir_ave10': { name: 'Wind Direction (Average)', unit: '°' },
    'battery': { name: 'Battery', unit: 'V' }
  }
};

// Get the current sensor configuration based on selected brand
const currentSensorConfig = computed(() => {
  return sensorConfigs[selectedBrand.value] || {};
});

// For backward compatibility with existing template
const sensorConfig = computed(() => {
  return currentSensorConfig.value;
});

// Get available sensors for the current brand
const availableSensors = computed(() => {
  const sensors = currentSensorConfig.value;
  return Object.keys(sensors).map(key => ({
    value: key,
    label: sensors[key].name
  }));
});

// Get the current sensor icon
const currentSensorIcon = computed(() => {
  return getSensorIcon(selectedSensorType.value);
});

// Navigation methods
const next = () => {
  if (currentPage.value < totalPages.value) {
    currentPage.value++;
    store.fetchStationData();
  }
};

const prev = () => {
  if (currentPage.value > 1) {
    currentPage.value--;
    store.fetchStationData();
  }
};

// Virtual scrolling implementation
const updateVisibleStations = () => {
  console.log('Updating visible stations. Current page:', currentPage.value, 'Total pawsStations:', pawsStations.value.length);
  visibleStations.value = pawsStations.value;
  console.log('Visible stations after update:', visibleStations.value.length, visibleStations.value);
};

// Intersection Observer for lazy loading
const setupIntersectionObserver = () => {
  if (!stationContainer.value) return;
  
  const observer = useIntersectionObserver(stationContainer, ([{ isIntersecting }]) => {
    if (isIntersecting) {
      updateVisibleStations();
    }
  });
};

// Lifecycle hooks
onMounted(() => {
  store.fetchStationData();
  setupIntersectionObserver();
  
  // Set up refresh interval (every 5 minutes)
  refreshIntervalId = setInterval(() => {
    store.fetchStationData(true);
  }, 5 * 60 * 1000);
});

onUnmounted(() => {
  if (refreshIntervalId) {
    clearInterval(refreshIntervalId);
    refreshIntervalId = null;
  }
});

// Watch for changes in pawsStations to update visibleStations
watch(pawsStations, (newStations) => {
  console.log('pawsStations changed:', newStations);
  if (newStations && newStations.length > 0) {
    updateVisibleStations();
  } else {
    visibleStations.value = [];
  }
}, { immediate: true });

// Get status class and text
const getStatusClass = (station) => {
  if (!station.latest_measurement) return 'badge bg-light-danger';
  return station.latest_measurement.status === 'Successful' 
    ? 'badge bg-light-success' 
    : 'badge bg-light-danger';
};

const getStatusText = (station) => {
  if (!station.latest_measurement) return 'No Data';
  return station.latest_measurement.status === 'Successful' ? 'Online' : 'Offline';
};

// Format value with unit
function formatValue(value) {
  if (value === null || value === undefined) {
    return 'N/A';
  }
  
  const config = currentSensorConfig.value[selectedSensorType.value];
  if (!config) return value;
  
  return `${parseFloat(value).toFixed(1)}${config.unit}`;
}

// Format date and time
function formatDateTime(measurement) {
  if (!measurement) return 'N/A';
  const date = new Date(`${measurement.date}T${measurement.time}`);
  return date.toLocaleString();
}

// Get sensor icon
const getSensorIcon = (sensorType) => {
  const iconMap = {
    'bt1': 'thermometer',
    'mt1': 'thermometer',
    'bp1': 'bar-chart-2',
    'ws': 'wind',
    'wd': 'compass',
    'rg': 'droplet',
    'sv1': 'sun',
    'si1': 'sun',
    'su1': 'sun',
    'bpc': 'battery',
    'css': 'wifi',
    'Air Temperature': 'thermometer',
    'Wind Speed': 'wind',
    'Solar Radiation': 'sun',
    'Precipitation': 'droplet',
    'Relative Humidity': 'droplet',
    'Atmospheric Pressure': 'bar-chart-2',
    'wind_ave10': 'wind',
    'dir_ave10': 'compass',
    'battery': 'battery'
  };
  return iconMap[sensorType] || 'activity';
};

// Get chart options
const getChartOptions = (sensorUnit, sensorType) => {
  const colorScheme = getSensorColorScheme(sensorType);

  return {
    chart: {
      type: 'area',
      height: 160,
      toolbar: {
        show: false
      },
      sparkline: {
        enabled: false
      },
      background: 'transparent',
      animations: {
        enabled: true,
        easing: 'easeinout',
        speed: 800
      }
    },
    grid: {
      show: true,
      borderColor: '#f0f0f0',
      strokeDashArray: 0,
      position: 'back',
      xaxis: {
        lines: {
          show: true
        }
      },
      yaxis: {
        lines: {
          show: true
        }
      },
      padding: {
        top: 0,
        right: 0,
        bottom: 0,
        left: 0
      }
    },
    stroke: {
      curve: 'smooth',
      width: 2
    },
    fill: {
      type: 'gradient',
      gradient: {
        shadeIntensity: 1,
        opacityFrom: 0.45,
        opacityTo: 0.05,
        stops: [50, 100],
        colorStops: [
          {
            offset: 0,
            color: colorScheme.gradient.from,
            opacity: 0.45
          },
          {
            offset: 100,
            color: colorScheme.gradient.to,
            opacity: 0.05
          }
        ]
      }
    },
    xaxis: {
      type: 'datetime',
      labels: {
        show: true,
        style: {
          fontSize: '10px',
          fontFamily: 'Inter, sans-serif',
          color: '#666'
        },
        formatter: function(val) {
          const date = new Date(val);
          return date.toLocaleString('en-US', {
            hour: '2-digit',
            minute: '2-digit',
            hour12: true
          });
        },
        datetimeUTC: false
      },
      axisBorder: {
        show: true,
        color: '#f0f0f0'
      },
      axisTicks: {
        show: true,
        color: '#f0f0f0'
      }
    },
    yaxis: {
      show: true,
      labels: {
        show: true,
        style: {
          fontSize: '10px',
          fontFamily: 'Inter, sans-serif',
          color: '#666'
        },
        formatter: (value) => `${value.toFixed(1)}${sensorUnit}`
      },
      axisBorder: {
        show: true,
        color: '#f0f0f0'
      }
    },
    tooltip: {
      enabled: true,
      shared: true,
      intersect: false,
      followCursor: false,
      fixed: {
        enabled: false,
        position: 'topRight',
        offsetX: 0,
        offsetY: 0,
      },
      onDatasetHover: {
        highlightDataSeries: false,
      },
      marker: {
        show: true,
      },
      items: {
        display: 'flex',
      },
      x: {
        show: true,
      },
      custom: ({ series, seriesIndex, dataPointIndex, w }) => {
        try {
          const value = series[seriesIndex][dataPointIndex];
          const dataPoint = w.config.series[seriesIndex].data[dataPointIndex];
          const timestamp = new Date(dataPoint.x);
          const formattedTime = timestamp.toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});
          const formattedDate = timestamp.toLocaleDateString([], {month: 'numeric', day: 'numeric', year: 'numeric'});
          
          return `
            <div class="nier-tooltip">
              <div class="tooltip-header">
                <div class="tooltip-date">${formattedDate}</div>
                <div class="tooltip-time">${formattedTime}</div>
              </div>
              <div class="tooltip-value">${value.toFixed(1)} ${sensorUnit}</div>
            </div>
          `;
        } catch (err) {
          console.error('Error in tooltip formatter:', err);
          return '';
        }
      }
    },
    colors: [colorScheme.main]
  };
};

// Get sensor color scheme
const getSensorColorScheme = (sensorType) => {
  const colorSchemes = {
    'bt1': { main: '#48A3D7', gradient: { from: '#48A3D7', to: '#48A3D7' } },
    'mt1': { main: '#48A3D7', gradient: { from: '#48A3D7', to: '#48A3D7' } },
    'rh': { main: '#7A70BA', gradient: { from: '#7A70BA', to: '#7A70BA' } },
    'ws': { main: '#D77748', gradient: { from: '#D77748', to: '#D77748' } },
    'rg': { main: '#C95E9E', gradient: { from: '#C95E9E', to: '#C95E9E' } },
    'bp': { main: '#51bb25', gradient: { from: '#51bb25', to: '#51bb25' } }
  };

  return colorSchemes[sensorType] || { main: '#7A70BA', gradient: { from: '#7A70BA', to: '#7A70BA' } };
};

// Function to select a brand
function selectBrand(brand) {
  console.log(`Selecting brand: ${brand}`);
  if (selectedBrand.value !== brand) {
    // Update brand first
    selectedBrand.value = brand;

    // Reset sensor type to first available for this brand
    const sensorTypes = Object.keys(sensorConfigs[brand] || {});
    if (sensorTypes.length > 0) {
      // Update sensor type
      selectedSensorType.value = sensorTypes[0];
      console.log(`Reset sensor type to: ${selectedSensorType.value}`);
      // Fetch data after both brand and sensor type are set
      store.fetchStationData(true);
    } else {
      // If no sensors for the brand, clear stations and stop loading
      store.stations = [];
      store.isLoading = false;
      console.log('No sensors found for this brand, clearing stations.');
    }
  }
}

// Function to select a sensor type
function selectSensorType(type) {
  console.log(`Selecting sensor type: ${type}`);
  if (selectedSensorType.value !== type) {
    selectedSensorType.value = type;
    // Fetch data after sensor type is set
    store.fetchStationData(true);
  }
}
</script>

<style scoped>
.station-card {
  transition: transform 0.2s ease-in-out;
}

.station-card:hover {
  transform: translateY(-2px);
}

.sensor-dropdown {
  min-width: 200px;
}

.sensor-name {
  display: inline-block;
  max-width: 100%;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.chart-container {
  position: relative;
  height: 160px;
}

.no-data-placeholder {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  text-align: center;
  color: #666;
}

.empty-state {
  padding: 2rem;
  text-align: center;
}

.empty-state h5 {
  margin-bottom: 0.5rem;
}

.nier-tooltip {
  background: white;
  border-radius: 4px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  padding: 8px;
}

.tooltip-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 4px;
  font-size: 12px;
  color: #666;
}

.tooltip-value {
  font-size: 14px;
  font-weight: 500;
  color: #333;
}
</style> 