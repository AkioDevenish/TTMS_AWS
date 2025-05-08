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
            <div v-if="!isLoading && paginatedStations.length === 0" class="text-center py-5">
                <div class="empty-state">
                    <VueFeather type="alert-circle" size="48" class="text-muted mb-3" />
                    <h5>No Data Available</h5>
                    <p class="text-muted">No stations found for the selected brand and sensor type.</p>
                </div>
            </div>

            <!-- Station Cards -->
            <div v-else class="row g-3">
                <div v-for="station in pawsStations" :key="station.id" class="col-xl-6 col-lg-6 col-md-12">
                    <div class="station-card h-100">
                        <div class="card-body p-4">
                            <div class="station-header mb-3">
                                <h5 class="station-name">{{ station.station_name }}</h5>
                            </div>
                            
                            <!-- Main info section -->
                            <div class="d-flex align-items-center gap-3 mb-4">
                                <div class="flex-shrink-0">
                                    <div class="temperature-icon-wrapper">
                                        <font-awesome-icon 
                                            :icon="['fas', currentSensorIcon]"
                                            class="sensor-icon"
                                        />
                                    </div>
                                </div>
                                <div class="flex-grow-1">
                                    <div class="d-flex align-items-center gap-2">
                                        <div class="station-reading">
                                            {{ formatValue(station.value, selectedSensorType) }}
                                            <span v-if="station.trend === 'increasing'" class="arrow-up">
                                                <i class="fas fa-arrow-up"></i>
                                            </span>
                                            <span v-else-if="station.trend === 'decreasing'" class="arrow-down">
                                                <i class="fas fa-arrow-down"></i>
                                            </span>
                                        </div>
                                    </div>
                                    <div class="last-updated-info">
                                        <i class="fa-regular fa-clock me-1"></i>
                                        <span>Last updated: {{ station.last_updated ? formatDateTime.date(station.last_updated) + ' ' + formatDateTime.time(station.last_updated) : 'No data' }}</span>
                                    </div>
                                </div>
                            </div>

                            <!-- Chart section -->
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
            <ul class="pagination mx-3 mt-3 justify-content-end" v-if="paginatedStations.length > 0">
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
import axios from 'axios';
import { useStationData } from '@/composables/useStationData';
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

// Get all the needed composables in one place at the top
const { formatDateTime } = useStationData();

// Initialize reactive variables
const pawsStations = ref([]);
const uniqueBrandsData = ref(['3D_Paws', 'Allmeteo', 'Zentra']); // Pre-populate with known brands
const selectedBrand = ref('3D_Paws'); // Default brand
const selectedSensorType = ref('bt1'); // Default to Temperature 1 for 3D_Paws
const currentPage = ref(1);
const itemsPerPage = 6;
const totalPages = ref(1);
const isLoading = ref(false);
const apiError = ref(null);
let refreshIntervalId = null; // Use a plain variable instead of ref for the interval

// Sensor configuration for each brand - COMPLETE CONFIGURATION
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

// Function to select a brand
function selectBrand(brand) {
  console.log(`Selecting brand: ${brand}`);
  if (selectedBrand.value !== brand) {
    selectedBrand.value = brand;
    
    // Reset sensor type to first available for this brand
    const sensorTypes = Object.keys(sensorConfigs[brand] || {});
    if (sensorTypes.length > 0) {
      selectedSensorType.value = sensorTypes[0];
      console.log(`Reset sensor type to: ${selectedSensorType.value}`);
    }
  }
}

// Function to select a sensor type
function selectSensorType(type) {
  console.log(`Selecting sensor type: ${type}`);
  if (selectedSensorType.value !== type) {
    selectedSensorType.value = type;
  }
}

// Get icon for sensor type
function getSensorIcon(sensorType) {
  const iconMap = {
    // Temperature sensors
    'bt1': 'temperatureHalf',
    'mt1': 'temperatureHigh',
    'Air Temperature': 'temperatureHalf',
    'Dew Point': 'temperatureQuarter',
    'Maximum Air Temperature': 'temperatureHigh',
    'Minimum Air Temperature': 'temperatureLow',
    
    // Wind sensors
    'ws': 'wind',
    'wd': 'compass',
    'Wind Speed': 'wind',
    'wind_ave10': 'wind',
    'dir_ave10': 'compass',
    'Wind Dir Average': 'compass',
    'Wind Dir Inst': 'compass',
    'Wind Speed Average': 'wind',
    'Wind Speed Inst': 'wind',
    'Gust Direction': 'compass',
    'Gust Speed': 'wind',
    
    // Precipitation
    'rg': 'cloudRain',
    'Precipitation': 'cloudRain',
    '5 min rain': 'cloudRain',
    'Daily Rain': 'cloudRain',
    
    // Pressure
    'bp1': 'gauge',
    'Atmospheric Pressure': 'gauge',
    'Barometric Pressure': 'gauge',
    'Baro Tendency': 'gauge',
    
    // Solar/radiation
    'sv1': 'sun',
    'si1': 'sun',
    'su1': 'sun',
    'Solar Radiation': 'sun',
    'Solar Radiation Avg': 'sun',
    'Solar Radiation Total': 'sun',
    'Hours of Sunshine': 'sun',
    
    // Battery/signal
    'bpc': 'batteryHalf',
    'css': 'signal',
    'battery': 'batteryHalf',
    'Battery': 'batteryHalf',
    
    // Humidity
    'Relative Humidity': 'droplet'
  };
  
  return iconMap[sensorType] || 'sensor'; // Default to generic sensor icon
}

// Format value with unit
function formatValue(value, sensorType) {
  if (value === null || value === undefined) {
    return 'N/A';
  }
  
  const config = currentSensorConfig.value[sensorType];
  if (!config) return value;
  
  return `${parseFloat(value).toFixed(1)}${config.unit}`;
}

// Calculate change text with proper sign and unit
const calculateChange = (station) => {
  if (station.valueChange === null || station.valueChange === undefined) {
    return 'No data';
  }
  
  // Format the value change with sign and 2 decimal places
  const change = parseFloat(station.valueChange).toFixed(2);
  return change > 0 ? `+${change}` : `${change}`;
};

// Get text class based on trend direction
const getTrendTextClass = (station) => {
  if (station.valueChange === null || station.valueChange === undefined) {
    return 'text-warning';
  }
  
  // Using absolute values to determine significance
  if (Math.abs(station.valueChange) < 0.1) {
    return 'text-warning'; // For very small changes, show as warning/stable
  }
  
  return station.valueChange > 0 ? 'text-success' : 'text-danger';
};

// Computed for showing paginated stations
const paginatedStations = computed(() => {
  return pawsStations.value;
});

// Enhanced function to fetch station data with chart history
async function fetchStationData(forceRefresh = false) {
  if (!selectedBrand.value || !selectedSensorType.value) {
    console.warn("Missing brand or sensor type, cannot fetch data");
    return;
  }
  
  console.log(`Fetching data for brand: ${selectedBrand.value}, sensor: ${selectedSensorType.value}, page: ${currentPage.value}`);
  
  isLoading.value = true;
  apiError.value = null;
  
  try {
    // Fetch the station overview data with pagination
    const params = {
      brand: selectedBrand.value,
      sensor_type: selectedSensorType.value,
      page: currentPage.value,
      page_size: itemsPerPage,
      latest: true,
      _t: new Date().getTime()
    };
    
    // Fetch the overview data
    const response = await axios.get('/measurements/station_overview/', { params });
    console.log("Overview response:", response.data);
    
    // Process the response
    if (response.data && response.data.stations) {
      totalPages.value = response.data.total_pages || 1;
      
      // Create a list of stations to fetch historical data for
      const stationIds = response.data.stations.map(station => station.id);
      
      // Fetch historical data for these stations (last 12 hours)
      const historicalData = {};
      
      if (stationIds.length > 0) {
        const historyResponse = await axios.get('/measurements/history/', {
          params: {
            station_ids: stationIds.join(','),
            sensor_type: selectedSensorType.value,
            hours: 12,
            _t: new Date().getTime()
          }
        });
        
        // Process historical data by station
        if (historyResponse.data && historyResponse.data.measurements) {
          historyResponse.data.measurements.forEach(measurement => {
            if (!historicalData[measurement.station_id]) {
              historicalData[measurement.station_id] = [];
            }
            
            historicalData[measurement.station_id].push({
              x: new Date(`${measurement.date}T${measurement.time}`).getTime(),
              y: measurement.value // Value is already converted to float in backend
            });
          });
        }
      }
      
      // Update stations with chart data
      pawsStations.value = response.data.stations.map(station => ({
        ...station,
        value: station.latest_value,
        last_updated: station.latest_date && station.latest_time ? `${station.latest_date}T${station.latest_time}` : null,
        chartData: [{
          name: currentSensorConfig.value[selectedSensorType.value]?.name || selectedSensorType.value,
          data: historicalData[station.id] || []
        }]
      }));
      
      console.log(`Loaded ${pawsStations.value.length} stations for ${selectedBrand.value} (Page ${currentPage.value} of ${totalPages.value})`);
    } else {
      pawsStations.value = [];
    }
  } catch (error) {
    console.error('Error fetching station overview data:', error);
    apiError.value = error.message || "Failed to fetch data";
    pawsStations.value = [];
  } finally {
    isLoading.value = false;
  }
}

// Update the navigation methods to fetch new data
const next = () => {
    if (currentPage.value < totalPages.value) {
        currentPage.value++;
        fetchStationData();
    }
};

const prev = () => {
    if (currentPage.value > 1) {
        currentPage.value--;
        fetchStationData();
    }
};

// FIXED WATCHERS - Separate watchers for better control
watch(() => selectedBrand.value, (newBrand, oldBrand) => {
  console.log(`Brand changed from ${oldBrand} to ${newBrand}`);
  currentPage.value = 1; // Reset to first page
  fetchStationData(true); // Force refresh when changing brand
}, { immediate: false });

watch(() => selectedSensorType.value, (newSensorType, oldSensorType) => {
  console.log(`Sensor type changed from ${oldSensorType} to ${newSensorType}`);
  currentPage.value = 1; // Reset to first page
  fetchStationData(true); // Force refresh when changing sensor type
}, { immediate: false });

// Initialize on component mount
onMounted(() => {
  console.log("Component mounted, fetching initial data");
  fetchStationData();
  
  // Set up refresh interval (every 5 minutes)
  refreshIntervalId = setInterval(() => {
    fetchStationData(true);
  }, 5 * 60 * 1000);
});

// Clean up on component unmount
onUnmounted(() => {
  if (refreshIntervalId) {
    clearInterval(refreshIntervalId);
    refreshIntervalId = null;
  }
});

// Get the current sensor icon
const currentSensorIcon = computed(() => {
    return sensorConfig[selectedSensorType.value]?.icon || 'temperature-half';
});

// Define an array of color schemes
const colorSchemes = [
    { main: '#1e88e5', // Blue
      gradient: { from: '#1e88e5', to: '#1e88e5' }
    },
    { main: '#00acc1', // Teal
      gradient: { from: '#00acc1', to: '#00acc1' }
    },
    { main: '#43a047', // Green
      gradient: { from: '#43a047', to: '#43a047' }
    },
    { main: '#fb8c00', // Orange
      gradient: { from: '#fb8c00', to: '#fb8c00' }
    }
];

// Get color scheme based on station index
const getColorScheme = (stationId) => {
    const index = stationId % colorSchemes.length;
    return colorSchemes[index];
};

// Update the getChartOptions function to accept stationId
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
                enabled: false // Changed to false to show axes
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
                    // Get the value from the series
                    const value = series[seriesIndex][dataPointIndex];
                    
                    // Get the data point from the chart's raw data
                    const dataPoint = w.config.series[seriesIndex].data[dataPointIndex];
                    
                    // Format timestamp from x value
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
            },
            x: {
                formatter: function(val) {
                    const date = new Date(val);
                    return date.toLocaleString('en-US', {
                        month: 'numeric',
                        day: 'numeric',
                        year: 'numeric',
                        hour: '2-digit',
                        minute: '2-digit',
                        hour12: true
                    });
                }
            }
        },
        colors: [colorScheme.main]
    };
};

// Helper function to get sensor unit
function getSensorUnit(sensorType) {
  const sensorUnits = {
    'bt1': '°C',
    'mt1': '°C',
    'rh': '%',
    'bp1': 'hPa',
    'ws': 'm/s',
    'rg': 'mm',
    // Add more sensor types as needed
  };
  
  return sensorUnits[sensorType] || '';
}

// Debug function
function debugData() {
    console.log('Current brand:', selectedBrand.value);
    console.log('Current sensor type:', selectedSensorType.value);
    console.log('Stations data:', pawsStations.value);
}

const getSensorColorScheme = (sensorType) => {
    const colorSchemes = {
        'bt1': { main: '#48A3D7', gradient: { from: '#48A3D7', to: '#48A3D7' } }, // Temperature blue
        'mt1': { main: '#48A3D7', gradient: { from: '#48A3D7', to: '#48A3D7' } }, // Temperature blue
        'rh': { main: '#7A70BA', gradient: { from: '#7A70BA', to: '#7A70BA' } },  // Humidity purple
        'ws': { main: '#D77748', gradient: { from: '#D77748', to: '#D77748' } },  // Wind Speed orange
        'rg': { main: '#C95E9E', gradient: { from: '#C95E9E', to: '#C95E9E' } },  // Rainfall pink
        'bp': { main: '#51bb25', gradient: { from: '#51bb25', to: '#51bb25' } }   // Pressure green
    };

    return colorSchemes[sensorType] || { main: '#7A70BA', gradient: { from: '#7A70BA', to: '#7A70BA' } };
};
</script>
<style scoped>
.cursor-pointer {
    cursor: pointer;
}

.nav-tabs .nav-link {
    cursor: pointer;
}

.nav-tabs .nav-link.active {
    color: #7A70BA;
    border-bottom: 2px solid #7A70BA;
}

.pagination {
    margin-bottom: 0;
}

.page-link {
    color: #7A70BA;
    background-color: #fff;
    border: 1px solid #dee2e6;
}

.page-item.active .page-link {
    background-color: #7A70BA;
    border-color: #7A70BA;
    color: #fff;
}

.page-item.disabled .page-link {
    color: #6c757d;
    pointer-events: none;
    background-color: #fff;
    border-color: #dee2e6;
}

.temperature-icon-wrapper {
    width: 48px;
    height: 48px;
    display: flex;
    align-items: center;
    justify-content: center;
    background-color: transparent !important;
    border-radius: 50%;
    transition: background-color 0.3s ease;
}

.sensor-icon {
    font-size: 24px;
    color: var(--bs-primary);
    width: 1em !important;
    height: 1em !important;
    transition: transform 0.3s ease;
}

.trend-arrow {
    margin-left: 5px;
    font-size: 16px;
    animation: pulse 2s infinite;
}

.trend-arrow.increase {
    color: #f44336; /* red for increasing */
}

.trend-arrow.decrease {
    color: #2196f3; /* blue for decreasing */
}

@keyframes pulse {
    0% {
        opacity: 0.6;
    }
    50% {
        opacity: 1;
    }
    100% {
        opacity: 0.6;
    }
}

.fa-solid {
    font-family: "Font Awesome 6 Free" !important;
    font-weight: 900 !important;
    -webkit-font-smoothing: antialiased;
    display: inline-block;
    font-style: normal;
    font-variant: normal;
    text-rendering: auto;
    line-height: 1;
}

.text-success {
    color: #28c76f !important;
}

.text-danger {
    color: #ea5455 !important;
}

.text-warning {
    color: #ff9f43 !important;
}

.trend-value {
    font-size: 0.875rem;
    font-weight: 500;
    margin-left: 4px;
}

.total-icon {
    display: flex;
    align-items: center;
    gap: 4px;
}

.dropdown-toggle {
    padding: 0.5rem 1rem;
    border-radius: 6px;
    background: transparent;
    border: 1px solid #dee2e6;
    color: #6c757d;
}

.dropdown-toggle:hover {
    background-color: #f8f9fa;
}

.dropdown-menu {
    min-width: 200px;
    padding: 0.5rem 0;
}

.dropdown-item {
    padding: 0.5rem 1rem;
    cursor: pointer;
    display: flex;
    align-items: center;
}

.dropdown-item i {
    width: 1.25em;
    text-align: center;
    font-size: 1rem;
    margin-right: 0.5rem;
}

.dropdown-toggle i {
    width: 1.25em;
    text-align: center;
    font-size: 1rem;
}

.dropdown-item span {
    margin-left: 0.25rem;
}

.dropdown-item:hover {
    background-color: #f8f9fa;
}

.dropdown-item.active {
    background-color: #7A70BA;
    color: white;
}
.station-name {
    color: #495057;  /* Grey color for better readability */
    font-size: 1.1rem;
    font-weight: 500;

}

.last-updated-info {
    color: #6c757d;
    font-size: 0.875rem;
    margin-top: 0.5rem;
    display: flex;
    align-items: center;
    gap: 0.25rem;
}

.last-updated-info i {
    font-size: 0.875rem;
    color: #6c757d;
}

.chart-wrapper {
    margin-top: 1rem;
    padding-top: 0.5rem;
}

.row {
    margin: 0 -1rem;  /* Negative margin to counteract padding */
}

.station-card {
    background: #fff;
    border-radius: 12px;
    box-shadow: 0 2px 6px rgba(0,0,0,0.08);
    transition: all 0.3s ease;
    contain: content; /* CSS containment for better performance */
    will-change: transform; /* Optimize for animations */
    overflow: visible !important;
}

.station-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 5px 15px rgba(0,0,0,0.1);
}

.card-body {
    height: 100%;
    display: flex;
    flex-direction: column;
    overflow: visible !important;
}

.chart-container {
    margin-top: 1rem;
    height: 160px;
    border-radius: 8px;
    padding: 10px;
}

.sensor-dropdown {
    min-width: 200px;
    max-width: 100%;
}

.sensor-dropdown .btn {
    width: 100%;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    background-color: #f8f9fa;
    border: 1px solid #dee2e6;
    color: #495057;
    padding: 0.5rem 1rem;
}

.sensor-name {
    display: block;
    text-align: left;
    margin-right: 1.5rem;
    overflow: hidden;
    text-overflow: ellipsis;
}

.dropdown-menu {
    min-width: 100%;
    max-height: 300px;
    overflow-y: auto;
}

.dropdown-item {
    white-space: normal;
    word-wrap: break-word;
    padding: 0.5rem 1rem;
}

/* Update tooltip styles */
:deep(.apexcharts-tooltip) {
    z-index: 100;
    background: #fff;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    position: absolute;
    transform: translateY(-100%);
    pointer-events: none;
}

:deep(.apexcharts-tooltip-series-group) {
    padding: 8px;
}

/* Remove any overflow restrictions from parent containers */
.station-card, .card-body {
    overflow: visible;
    position: relative;
    z-index: 1;
}

/* Ensure the chart's parent containers don't clip */
.row > * {
    overflow: visible;
}

.row {
    overflow: visible;
}

.icon-update {
    animation: iconUpdate 0.3s ease;
}

@keyframes iconUpdate {
    0% {
        transform: scale(0.9);
        opacity: 0.5;
    }
    100% {
        transform: scale(1);
        opacity: 1;
    }
}

/* Add hover effect */
.temperature-icon-wrapper:hover {
    background-color: rgba(var(--bs-primary-rgb), 0.2);
}

.temperature-icon-wrapper:hover .sensor-icon {
    transform: scale(1.1);
}

.station-overview-header {
    padding-bottom: 1rem;
    border-bottom: 1px solid #eee;
}

.section-title {
    font-size: 1.5rem;
    font-weight: 600;
    color: #333;
    margin-bottom: 0.5rem;
}

.section-subtitle {
    color: #6c757d;
    margin-bottom: 0;
}

.sensor-dropdown {
    width: 220px;
    max-width: 100%;
}

.sensor-name {
    display: inline-block;
    max-width: 100%;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}

.station-card {
    background: #fff;
    border-radius: 12px;
    box-shadow: 0 2px 6px rgba(0,0,0,0.08);
    transition: all 0.3s ease;
    border: none;
}

.station-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 5px 15px rgba(0,0,0,0.1);
}

.station-name {
    color: #495057;
    font-size: 1.1rem;
    font-weight: 500;
    margin-bottom: 1rem;
}

.sensor-icon {
    width: 48px;
    height: 48px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 50%;
    background-color: rgba(var(--bs-primary-rgb), 0.1);
}

.chart-container {
    margin-top: 1rem;
    height: 160px;
    border-radius: 8px;
    padding: 10px;
}

.nav-tabs .nav-link {
    cursor: pointer;
    padding: 0.75rem 1.25rem;
    border: none;
    border-bottom: 2px solid transparent;
    transition: all 0.3s ease;
}

.nav-tabs .nav-link.active {
    color: var(--bs-primary);
    border-bottom: 2px solid var(--bs-primary);
    background-color: transparent;
}

.dropdown-menu {
    max-height: 300px;
    overflow-y: auto;
}

.dropdown-item {
    white-space: normal;
    word-wrap: break-word;
    padding: 0.5rem 1rem;
}

.badge {
    padding: 0.35em 0.65em;
    font-size: 0.75em;
}

@media (max-width: 768px) {
    .sensor-dropdown {
        width: 100%;
        margin-top: 1rem;
    }
}

.trend-indicator {
    font-size: 14px;
    margin-left: 5px;
}
.trend-indicator.up {
    color: #f44336; /* red for increasing */
}
.trend-indicator.down {
    color: #2196f3; /* blue for decreasing */
}
.trend-indicator.stable {
    color: #9e9e9e; /* gray for stable */
}

.station-reading {
    display: flex;
    align-items: center;
    font-size: 1.5rem;
    font-weight: 600;
}

.arrow-up, .arrow-down {
    display: inline-flex;
    margin-left: 8px;
    font-size: 1rem;
}

.arrow-up {
    color: #f44336; /* Red */
}

.arrow-down {
    color: #2196f3; /* Blue */
}

.temperature-icon-wrapper {
    background: transparent !important;
}

/* Modern tooltip styles - add to your <style> section */
:deep(.nier-tooltip) {
  background: rgba(255, 255, 255, 0.95);
  border-radius: 8px;
  padding: 8px 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  border-left: 3px solid #e74c3c;
  color: #333;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
  min-width: 120px;
  backdrop-filter: blur(4px);
  transition: all 0.2s ease;
  animation: tooltipFade 0.2s ease-in-out;
}

@keyframes tooltipFade {
  from { opacity: 0; transform: translateY(4px); }
  to { opacity: 1; transform: translateY(0); }
}

:deep(.tooltip-header) {
  display: flex;
  flex-direction: column;
  margin-bottom: 5px;
  border-bottom: 1px solid rgba(0, 0, 0, 0.08);
  padding-bottom: 5px;
}

:deep(.tooltip-date) {
  font-weight: 600;
  color: #333;
  font-size: 13px;
}

:deep(.tooltip-time) {
  color: #666;
  font-size: 12px;
  margin-top: 2px;
}

:deep(.tooltip-value) {
  font-size: 16px;
  font-weight: 700;
  color: #111;
  padding-top: 2px;
}

.no-data-placeholder {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #f8f9fa;
  border-radius: 8px;
  color: #6c757d;
  font-size: 14px;
}

/* Add these to your CSS to improve the tooltip experience */
:deep(.apexcharts-xcrosshairs) {
  stroke-width: 20px;
  stroke: rgba(0, 0, 0, 0.05);
  stroke-dasharray: 0;
  pointer-events: auto;
  cursor: pointer;
}

:deep(.apexcharts-tooltip) {
  pointer-events: none;
  transition: none !important;
}

:deep(.nier-tooltip) {
  background: rgba(255, 255, 255, 0.95);
  border-radius: 8px;
  padding: 8px 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  border-left: 3px solid #e74c3c;
  color: #333;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
  min-width: 120px;
  backdrop-filter: blur(4px);
  transition: none;
  animation: none;
}

:deep(.apexcharts-xaxis-label),
:deep(.apexcharts-yaxis-label) {
    fill: #666;
}

:deep(.apexcharts-grid-borders line) {
    stroke: #f0f0f0;
    stroke-width: 1;
}
</style>
