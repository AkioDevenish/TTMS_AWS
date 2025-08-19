<template>
    <!-- Move Card1 to be the second component -->
    <div class="order-3">
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
                                    v-if="station.chartData && station.chartData[0].data.length > 1"
                                    type="area"
                                    height="160"
                                    :options="getChartOptions(station.sensor_unit, selectedSensorType)"
                                    :series="station.chartData"
                                ></apexchart>
                                <div v-else-if="station.chartData && station.chartData[0].data.length === 1" class="single-data-point">
                                    <div class="text-center">
                                        <p class="mb-1"><strong>Current Value:</strong></p>
                                        <p class="h4 mb-0">{{ formatValue(station.chartData[0].data[0].y) }}</p>
                                        <small class="text-muted">{{ formatDateTime(station.latest_measurement) }}</small>
                                    </div>
                                </div>
                                <div v-else class="no-data-placeholder">
                                    <p>No historical data available</p>
                                    <small v-if="station.chartData" class="text-muted">
                                        Debug: Chart data length: {{ station.chartData[0]?.data?.length || 0 }}
                                    </small>
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
const uniqueBrandsData = ref(['3D_Paws', 'Allmeteo', 'Zentra', 'OTT']); // Add OTT
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

// Get paginated stations from store (these are already globally sorted)
const paginatedStations = computed(() => store.paginatedStations || []);

// Define status priority function (lower number = higher priority)
const getStatusPriority = (status) => {
  if (status === 'Offline') return 1;
  if (status === 'Online Erroneous Data') return 2;
  if (status === 'Online') return 3;
  return 4; // Default for unknown statuses
};

// Sort stations by status priority: Offline first, then Online Erroneous Data, then Online
const sortedStations = computed(() => {
  if (!pawsStations.value || pawsStations.value.length === 0) {
    return [];
  }
  
  const sorted = [...pawsStations.value].sort((a, b) => {
    const statusA = getStatusText(a);
    const statusB = getStatusText(b);
    
    const priorityA = getStatusPriority(statusA);
    const priorityB = getStatusPriority(statusB);
    
    return priorityA - priorityB;
  });
  
  // Debug logging
  console.log('Station sorting applied:', sorted.map(s => ({
    name: s.name,
    status: getStatusText(s),
    priority: getStatusPriority(getStatusText(s))
  })));
  
  return sorted;
});

// Get globally sorted stations for all pages
const allSortedStations = computed(() => {
  // This would need to fetch all stations from the store, not just the current page
  // For now, we'll work with what we have and improve the backend sorting
  return sortedStations.value;
});

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
    'wind_max10': { name: 'Wind Speed (Max)', unit: 'm/s' },
    'wind_min10': { name: 'Wind Speed (Min)', unit: 'm/s' },
    'dir_ave10': { name: 'Wind Direction (Average)', unit: '°' },
    'dir_max10': { name: 'Wind Direction (Max)', unit: '°' },
    'dir_hi10': { name: 'Wind Direction (High)', unit: '°' },
    'dir_lo10': { name: 'Wind Direction (Low)', unit: '°' },
    'Battery Percent': { name: 'Battery Percent', unit: '%' },
    'humidity': { name: 'Humidity', unit: '%' },
    'irradiation': { name: 'Irradiation', unit: 'W/m²' },
    'irr_max': { name: 'Irradiation (Max)', unit: 'W/m²' },
    'pressure': { name: 'Pressure', unit: 'Pa' },
    'temperature': { name: 'Temperature', unit: '°C' },
    'temperature_max': { name: 'Temperature (Max)', unit: '°C' },
    'temperature_min': { name: 'Temperature (Min)', unit: '°C' },
    'rain_counter': { name: 'Rain Counter', unit: 'mm' }
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
  visibleStations.value = paginatedStations.value;
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
watch([pawsStations, paginatedStations], (newStations) => {
  console.log('pawsStations or paginatedStations changed:', newStations);
  if (newStations[0] && newStations[0].length > 0) {
    updateVisibleStations();
  } else {
    visibleStations.value = [];
  }
}, { immediate: true });

// Get status class and text with three-tier system
const getStatusClass = (station) => {
  const status = getStatusText(station);
  
  switch (status?.toLowerCase()) {
    case 'online':
      return 'badge bg-light-success';
    case 'critical battery':
      return 'badge bg-light-danger';
    case 'low battery':
      return 'badge bg-light-warning';
    case 'battery warning':
      return 'badge bg-light-warning';
    case 'excellent signal':
      return 'badge bg-light-success';
    case 'good signal':
      return 'badge bg-light-success';
    case 'fair signal':
      return 'badge bg-light-warning';
    case 'poor signal':
      return 'badge bg-light-warning';
    case 'weak signal':
      return 'badge bg-light-danger';
    case 'online erroneous data':
      return 'badge bg-light-warning';
    case 'offline':
      return 'badge bg-light-danger';
    default:
      return 'badge bg-light-warning';
  }
};

const getStatusText = (station) => {
  // Debug logging
  console.log(`Status detection for ${station.name}:`, {
    hasChartData: !!(station.chartData && station.chartData[0] && station.chartData[0].data),
    chartDataLength: station.chartData?.[0]?.data?.length || 0,
    hasLatestMeasurement: !!station.latest_measurement,
    latestValue: station.latest_measurement?.value,
    latestStatus: station.latest_measurement?.status,
    lastUpdateTime: station.latest_measurement?.date
  });

  // FIRST: Check if sensor is actually communicating (not offline)
  if (!station.latest_measurement) {
    console.log(`  ${station.name}: No latest measurement -> Offline`);
    return 'Offline'; // No recent data = offline
  }

  // Check if the last update is recent (within last 2 hours = online, beyond = offline)
  const lastUpdate = new Date(`${station.latest_measurement.date}T${station.latest_measurement.time}`);
  const now = new Date();
  const hoursSinceUpdate = (now - lastUpdate) / (1000 * 60 * 60);
  
  console.log(`  ${station.name} time check:`, {
    lastUpdate: lastUpdate.toISOString(),
    now: now.toISOString(),
    hoursSinceUpdate: hoursSinceUpdate,
    willBeOffline: hoursSinceUpdate > 2
  });
  
  // Check if date parsing failed (invalid date)
  if (isNaN(lastUpdate.getTime())) {
    console.log(`  ${station.name}: Invalid date format -> Offline`);
    return 'Offline'; // Invalid date = offline
  }
  
  if (hoursSinceUpdate > 2) {
    console.log(`  ${station.name}: Last update ${hoursSinceUpdate.toFixed(1)} hours ago -> Offline`);
    return 'Offline'; // No recent communication = offline
  }
  
  // SPECIAL HANDLING FOR UV SENSORS - if it's 0.0W/m² during daytime, check if it's actually offline
  const sensorType = selectedSensorType.value;
  const uvSensors = ['su1', 'Downwelling Ultraviolet', 'uv', 'ultraviolet'];
  
  if (uvSensors.includes(sensorType)) {
    const value = parseFloat(station.latest_measurement?.value);
    if (value === 0) {
      // Check if it's daytime (UV should be > 0 during day)
      const hour = now.getHours();
      const isDaytime = hour >= 6 && hour <= 18; // 6 AM to 6 PM
      
      if (isDaytime) {
        console.log(`  ${station.name}: UV sensor reading 0.0W/m² during daytime - checking if offline`);
        // If UV is 0 during day and hasn't updated recently, it's likely offline
        if (hoursSinceUpdate > 0.1) { // More strict for UV sensors - 6 minutes
          console.log(`  ${station.name}: UV sensor offline during daytime -> Offline`);
          return 'Offline';
        }
      }
    }
  }

  // SECOND: If sensor is communicating, check data quality
  if (station.chartData && station.chartData[0] && station.chartData[0].data && station.chartData[0].data.length > 0) {
    // Station has data and is communicating - now determine if data is valid
    const value = parseFloat(station.latest_measurement?.value);
    const isInvalidValue = isNaN(value) || 
      value === -999 || value === -999.0 || value === 999 || value === 999.0 ||
      value === -9999 || value === -9999.0 || value === 9999 || value === 9999.0 ||
      value === -32768 || value === -32768.0;
    
    // SPECIAL HANDLING FOR BATTERY SENSORS
    const sensorType = selectedSensorType.value;
    const batterySensors = ['bpc', 'Battery Percent', 'battery_percent', 'battery'];
    const cellSignalSensors = ['css', 'Cell Signal Strength', 'cell_signal', 'signal_strength'];
    
    if (batterySensors.includes(sensorType)) {
      if (value === 0) {
        return 'Critical Battery'; // 0% battery is critical, not erroneous
      } else if (value <= 10) {
        return 'Low Battery'; // 1-10% battery is low
      } else if (value <= 25) {
        return 'Battery Warning'; // 11-25% battery needs attention
      } else {
        return 'Online'; // 26%+ battery is healthy
      }
    }
    
    if (cellSignalSensors.includes(sensorType)) {
      if (value >= 80) {
        return 'Excellent Signal'; // 80%+ signal strength is excellent
      } else if (value >= 60) {
        return 'Good Signal'; // 60-79% signal strength is good
      } else if (value >= 40) {
        return 'Fair Signal'; // 40-59% signal strength is fair
      } else if (value >= 20) {
        return 'Poor Signal'; // 20-39% signal strength is poor
      } else {
        return 'Weak Signal'; // Below 20% signal strength is weak
      }
    }
    
    // Check if sensor is stuck (always reading same value) - but NOT for battery/cell signal sensors
    const isStuckSensor = checkStuckSensor(station);
    
    console.log(`  ${station.name} data validation:`, {
      value,
      isInvalidValue,
      isStuckSensor,
      sensorType,
      hoursSinceUpdate,
      finalStatus: (isInvalidValue || isStuckSensor) ? 'Online Erroneous Data' : 'Online'
    });
    
    if (isInvalidValue || isStuckSensor) {
      return 'Online Erroneous Data'; // Station transmitting but data fails validation
    } else {
      return 'Online'; // Station reporting valid data
    }
  }
  
  // Fallback: if we have some measurement but no chart data, still consider online
  console.log(`  ${station.name}: Has measurement but no chart data -> Online (fallback)`);
  return 'Online';
};

// Function to check if a sensor is stuck (always reading the same value)
const checkStuckSensor = (station) => {
  if (!station.chartData || !station.chartData[0] || !station.chartData[0].data || station.chartData[0].data.length < 5) {
    return false; // Need at least 5 data points to determine if stuck
  }
  
  const dataPoints = station.chartData[0].data;
  const values = dataPoints.map(point => point.y);
  
  // Check if all values are within 0.1 tolerance of the first value
  const firstValue = values[0];
  const tolerance = 0.1;
  
  for (let i = 1; i < values.length; i++) {
    if (Math.abs(values[i] - firstValue) > tolerance) {
      return false; // Found a different value, sensor is not stuck
    }
  }
  
  // CRITICAL FIX: Battery sensors should NOT be flagged as stuck
  const sensorType = selectedSensorType.value;
  const batterySensors = ['bpc', 'Battery Percent', 'battery_percent', 'battery'];
  const cellSignalSensors = ['css', 'Cell Signal Strength', 'cell_signal', 'signal_strength'];
  
  if (batterySensors.includes(sensorType)) {
    console.log(`${station.name}: Battery sensor detected - steady readings are GOOD, not stuck`);
    return false; // Battery sensors with steady readings are healthy
  }
  
  if (cellSignalSensors.includes(sensorType)) {
    console.log(`${station.name}: Cell signal sensor detected - steady readings are GOOD, not stuck`);
    return false; // Cell signal sensors with steady readings are healthy
  }
  
  // For solar radiation sensors, check if it's during daylight hours
  if (sensorType === 'sv1' || sensorType === 'si1' || sensorType === 'Solar Radiation') {
    const now = new Date();
    const hour = now.getHours();
    const isDaytime = hour >= 6 && hour <= 18; // 6 AM to 6 PM
    
    console.log(`Solar sensor debug for ${station.name}:`, {
      sensorType,
      currentHour: hour,
      isDaytime,
      firstValue,
      willBeStuck: isDaytime && Math.abs(firstValue) < 0.1
    });
    
    // If it's daytime and all values are 0.0, that's suspicious
    if (isDaytime && Math.abs(firstValue) < 0.1) {
      return true; // Sensor stuck at 0.0 during daytime = suspicious
    }
    
    // If it's nighttime and all values are 0.0, that's normal
    if (!isDaytime && Math.abs(firstValue) < 0.1) {
      return false; // Normal for solar sensors at night
    }
  }
  
  // Additional check: Don't flag sensors where zero values are normal
  const zeroValueSensors = ['rg', 'Precipitation', 'rain_counter', 'rain_intensity_max'];
  
  if (zeroValueSensors.includes(sensorType) && Math.abs(firstValue) < 0.1) {
    return false; // Precipitation sensors reading 0.0mm is normal (no rain)
  }
  
  return true; // All values are the same, sensor is stuck
};

// Format value with unit
function formatValue(value) {
  if (value === null || value === undefined) {
    return 'No Data';
  }
  
  const config = currentSensorConfig.value[selectedSensorType.value];
  if (!config) return value;
  
  return `${parseFloat(value).toFixed(1)}${config.unit}`;
}

// Format date and time
function formatDateTime(measurement) {
  if (!measurement) return 'No Recent Data';
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
    'Battery Percent': 'battery'
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
    'rg': { main: '#C95E9E', gradient: { from: '#C95E9E', to: '#7A70BA' } },
    'bp': { main: '#51bb25', gradient: { from: '#51bb25', to: '#51bb25' } },
    'Battery Percent': { main: '#51bb25', gradient: { from: '#51bb25', to: '#51bb25' } }
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

.single-data-point {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  text-align: center;
  width: 100%;
  padding: 1rem;
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

/* Custom status badge colors */
.badge.bg-light-danger {
  background-color: rgba(220, 53, 69, 0.15) !important;
  color: #dc3545 !important;
  border: 1px solid rgba(220, 53, 69, 0.3);
}

.badge.bg-light-warning {
  background-color: rgba(255, 193, 7, 0.15) !important;
  color: #ffc107 !important;
  border: 1px solid rgba(255, 193, 7, 0.3);
}

.badge.bg-light-success {
  background-color: rgba(40, 167, 69, 0.15) !important;
  color: #28a745 !important;
  border: 1px solid rgba(40, 167, 69, 0.3);
}
</style>