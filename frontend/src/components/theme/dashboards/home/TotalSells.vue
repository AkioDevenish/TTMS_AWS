<template>
    <!-- Move Card1 to be the second component -->
    <div class="order-2">
        <Card1 headerTitle="true" title="Station Overview" cardhaderClass="card-no-border">
            <!-- Brand tabs section -->
            <ul class="nav nav-tabs border-tab nav-primary" role="tablist">
                <li class="nav-item" v-for="brand in uniqueBrands" :key="brand">
                    <a class="nav-link" :class="{ active: selectedBrand === brand }" @click="selectedBrand = brand">
                        {{ brand }}
                    </a>
                </li>
            </ul>

            <!-- Sensor Type Dropdown -->
            <div class="d-flex justify-content-end mb-3 mt-3">
                <div class="dropdown sensor-dropdown">
                    <button class="btn dropdown-toggle d-flex align-items-center" type="button" data-bs-toggle="dropdown" aria-expanded="false">
                        <span class="sensor-name">{{ sensorConfig[selectedSensorType]?.name || selectedSensorType }}</span>
                    </button>
                    <ul class="dropdown-menu dropdown-menu-end">
                        <li v-for="(config, type) in filteredSensorConfig" :key="type">
                            <a class="dropdown-item" 
                               href="#" 
                               @click.prevent="selectedSensorType = type"
                               :class="{ active: selectedSensorType === type }">
                                {{ config.name }}
                            </a>
                        </li>
                    </ul>
                </div>
            </div>

            <!-- Station Cards -->
            <div class="row g-4 mt-3">
                <div v-for="station in paginatedStations" 
                     :key="station.id" 
                     class="col-xl-4 col-md-6">
                    <div class="station-card h-100">
                        <div class="card-body p-4">
                            <div class="station-header mb-3">
                                <h5 class="station-name">{{ station.name }}</h5>
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
                                        <h2 class="mb-0">{{ formatValue(station.currentValue) }}</h2>
                                        <div class="trend-indicators d-flex align-items-center">
                                            <template v-if="calculateChange(station) !== 'No data'">
                                                <vue-feather 
                                                    :type="parseFloat(calculateChange(station)) > 0 ? 'arrow-up' : 'arrow-down'"
                                                    :class="['trend-arrow', getTrendTextClass(station)]"
                                                ></vue-feather>
                                                <span :class="getTrendTextClass(station)" class="trend-value">
                                                    {{ calculateChange(station) }}
                                                </span>
                                            </template>
                                            <vue-feather v-else type="minus" class="trend-arrow text-warning"></vue-feather>
                                        </div>
                                    </div>
                                    <div class="last-updated-info">
                                        <i class="fa-regular fa-clock me-1"></i>
                                        <span>Last updated: {{ station.lastUpdate ? formatDateTime.date(station.lastUpdate) + ' ' + formatDateTime.time(station.lastUpdate) : 'No data' }}</span>
                                    </div>
                                </div>
                            </div>

                            <!-- Chart section -->
                            <div class="chart-container">
                                <apexchart
                                    v-if="station.chartData && station.chartData.length > 0"
                                    type="area"
                                    height="100"
                                    :options="chartOptions"
                                    :series="station.chartData"
                                />
                                <div v-else class="text-center py-3">
                                    <p class="mb-0">No data available</p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Pagination -->
            <div class="d-flex justify-content-center mt-4">
                <ul class="pagination">
                    <li class="page-item" :class="{ disabled: currentPage === 1 }">
                        <a class="page-link" @click="prevPage">Previous</a>
                    </li>
                    <li class="page-item" v-for="page in totalPages" :key="page"
                        :class="{ active: currentPage === page }">
                        <a class="page-link" @click="currentPage = page">{{ page }}</a>
                    </li>
                    <li class="page-item" :class="{ disabled: currentPage === totalPages }">
                        <a class="page-link" @click="nextPage">Next</a>
                    </li>
                </ul>
            </div>
        </Card1>
    </div>
</template>

<script lang="ts" setup>
import { ref, onMounted, onUnmounted, computed, watch, nextTick } from 'vue';
import { defineAsyncComponent } from 'vue';
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

// Import Card component
const Card1 = defineAsyncComponent(() => import('@/components/common/card/CardData1.vue'));

// Get all the needed composables in one place at the top
const { measurements, stationInfo, getLast24HoursMeasurements, formatDateTime } = useStationData();

// Station interface
interface Station {
    id: number;
    name: string;
    brand_name: string;
    lastUpdate: string;
    measurements: {
        value: number;
        date_time: string;
        created_at: string;
    }[];
    valueHistory: number[];
    timeHistory: string[];
    currentValue: number | null;
    chartData: any[];
}

// Initialize reactive variables
const pawsStations = ref<Station[]>([]);
const selectedBrand = ref<string>('3D_Paws');
const currentPage = ref(1);
const itemsPerPage = 6;

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
]

// Get color scheme based on station index
const getColorScheme = (stationId: string) => {
    const index = parseInt(stationId) % colorSchemes.length
    return colorSchemes[index]
}

// Fetch station data
const fetchStationData = async () => {
    try {
        const [stationsResponse, measurementsResponse] = await Promise.all([
            axios.get('/stations/'),
            axios.get('/measurements/')
        ]);

        // Process stations data
        const stationsData = stationsResponse.data
            .map((station: any) => ({
                id: station.id,
                name: station.name,
                brand_name: station.brand_name,
                lastUpdate: station.last_updated,
                measurements: measurementsResponse.data.filter((m: any) => 
                    m.station === station.id &&
                    m.sensor_type === selectedSensorType.value &&
                    m.value !== null &&
                    m.status === 'Successful'
                ).map((m: any) => ({
                    value: parseFloat(m.value),
                    date_time: `${m.date}T${m.time}`,
                    date: m.date,
                    time: m.time,
                    sensor_type: m.sensor_type,
                    created_at: m.created_at
                })).sort((a: any, b: any) => 
                    new Date(b.date_time).getTime() - new Date(a.date_time).getTime()
                ),
                currentValue: null,
                chartData: [] as any[]
            }));

        // Update stations with processed data
        pawsStations.value = stationsData.map(station => {
            const latestMeasurement = station.measurements[0];
            const last24Hours = station.measurements.slice(0, 24).reverse();

            return {
                ...station,
                currentValue: latestMeasurement?.value ?? null,
                lastUpdate: latestMeasurement?.date_time ?? null,
                chartData: [{
                    name: sensorConfig[selectedSensorType.value]?.name || selectedSensorType.value,
                    data: last24Hours.map(m => ({
                        x: new Date(m.date_time).getTime(),
                        y: m.value
                    }))
                }]
            };
        });

        console.log('Processed stations data:', pawsStations.value);
    } catch (error) {
        console.error('Error fetching station data:', error);
        pawsStations.value = [];
    }
};

// Format temperature
const formatTemperature = (temp: number | null): string => {
    if (temp === null || temp === undefined) return 'N/A'
    return `${temp.toFixed(1)}°C`
}

// Calculate temperature change
const calculateTempChange = (station: Station): string => {
    console.log('calculateTempChange input:', {
        station,
        tempHistory: station.tempHistory,
        hasHistory: station.tempHistory && station.tempHistory.length >= 2
    });

    if (!station.tempHistory || station.tempHistory.length < 2) {
        console.log('No sufficient temperature history');
        return 'No data';
    }
    
    const latest = station.tempHistory[station.tempHistory.length - 1];
    const previous = station.tempHistory[0];
    const change = ((latest - previous) / previous) * 100;
    
    console.log('Temperature change calculation:', {
        latest,
        previous,
        change,
        formattedChange: `${change > 0 ? '+' : ''}${change.toFixed(2)}%`
    });
    
    return `${change > 0 ? '+' : ''}${change.toFixed(2)}%`;
};

// Get temperature trend classes
const getTempTrendClass = (station: Station): string => {
    if (!station.tempHistory || station.tempHistory.length < 2) return 'mb-0 up-arrow bg-light-primary'
    const change = station.tempHistory[station.tempHistory.length - 1] - station.tempHistory[0]
    return `mb-0 up-arrow ${change >= 0 ? 'bg-light-success' : 'bg-light-danger'}`
}

// Update the icon function to use simple classes
const getTempTrendIcon = (station: Station) => {
    const change = calculateTempChange(station);
    if (!change || change === 'No data') return 'minus';
    return change > 0 ? 'arrow-up' : 'arrow-down';
};

// Add debugging for icon classes
const getTempTrendColor = (station: Station) => {
    const change = calculateTempChange(station);
    const result = !change || change === 'No data' ? 'text-warning' 
                  : parseFloat(change) > 0 ? 'text-success' 
                  : 'text-danger';
                  
    console.log('getTempTrendColor:', {
        station: station.name,
        change,
        resultClass: result
    });
    
    return result;
};

// Add this function with the other trend-related functions
const getTempTrendTextClass = (station: Station) => {
    const change = calculateTempChange(station);
    if (!change || change === 'No data') return 'text-warning';
    return parseFloat(change) > 0 ? 'text-success' : 'text-danger';
};

// Add this near the top of your script section with other refs
const selectedSensorType = ref<string>('bt1'); // Initialize with default sensor type

// Update the chart series to use the selected sensor type
const getChartSeries = (station: any) => {
    if (!station?.measurements?.length) return [];

    const filteredData = station.measurements
        .filter((m: any) => 
            m.sensor_type === selectedSensorType.value &&
            m.value !== null &&
            m.status === 'Successful'
        )
        .map((item: any) => ({
            x: new Date(`${item.date}T${item.time}`).getTime(),
            y: parseFloat(item.value)
        }));

    return [{
        name: sensorConfig[selectedSensorType.value]?.name || selectedSensorType.value,
        data: filteredData
    }];
};

// Update the chart options
const chartOptions = computed(() => ({
    chart: {
        sparkline: { enabled: true },
        toolbar: { show: false },
        animations: {
            enabled: true
        },
        stacked: false
    },
    dataLabels: { enabled: false },
    stroke: { 
        curve: 'smooth', 
        width: 2
    },
    xaxis: {
        type: 'datetime',
        labels: {
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
        fixed: {
            enabled: true,
            position: 'topLeft',
            offsetY: 30,
            offsetX: 60
        },
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
            formatter: (val: number) => `${val.toFixed(1)} ${sensorConfig[selectedSensorType.value]?.unit || ''}`
        }
    },
    markers: {
        size: 0,
        hover: {
            size: 5
        }
    }
}));

// Add cleanup for any intervals or watchers
let refreshInterval: number | null = null;

onMounted(() => {
    console.log('Checking Font Awesome loading:');
    
    // Check if Font Awesome stylesheet is loaded
    const faStylesheet = document.querySelector('link[href*="font-awesome"]');
    console.log('Font Awesome stylesheet:', faStylesheet);
    
    // Check if Font Awesome classes are working
    const testIcon = document.createElement('i');
    testIcon.className = 'fa-solid fa-temperature-half';
    document.body.appendChild(testIcon);
    
    // Get computed styles
    const computedStyle = window.getComputedStyle(testIcon);
    console.log('Test icon computed styles:', {
        fontFamily: computedStyle.fontFamily,
        content: computedStyle.content,
        display: computedStyle.display,
        width: computedStyle.width,
        height: computedStyle.height
    });
    
    // Cleanup test icon
    document.body.removeChild(testIcon);
    
    // Check actual icons in the component
    const actualIcons = document.querySelectorAll('.temperature-icon-wrapper i, .trend-arrow');
    console.log('Actual icons in component:', {
        count: actualIcons.length,
        elements: Array.from(actualIcons).map(icon => ({
            className: icon.className,
            computedStyle: window.getComputedStyle(icon)
        }))
    });
    
    fetchStationData()
    // Set up refresh interval
    refreshInterval = window.setInterval(() => {
        fetchStationData()
    }, 60000) // Refresh every minute

    // Ensure 3D_Paws is selected by default
    selectedBrand.value = '3D_Paws';

    // Add a small delay to ensure the DOM is fully loaded
    setTimeout(() => {
        const icons = document.querySelectorAll('.temperature-icon-wrapper i');
        icons.forEach(icon => {
            // Force a reflow
            icon.style.display = 'none';
            icon.offsetHeight; // Trigger reflow
            icon.style.display = '';
        });
    }, 100);
})

onUnmounted(() => {
    // Clean up the interval
    if (refreshInterval) {
        clearInterval(refreshInterval)
        refreshInterval = null
    }
})

// Get unique brands from stations
const uniqueBrands = computed(() => {
    const brands = pawsStations.value.map(station => station.brand_name);
    return [...new Set(brands)];
});

// Filter stations by selected brand
const filteredStations = computed(() => {
    if (!selectedBrand.value || !pawsStations.value.length) return [];
    return pawsStations.value.filter(station => 
        station.brand_name === selectedBrand.value
    );
})

// Calculate total pages
const totalPages = computed(() => {
    return Math.ceil(filteredStations.value.length / itemsPerPage)
})

// Remove the duplicate paginatedStations declaration and merge the optimizations
const paginatedStations = computed(() => {
    const start = (currentPage.value - 1) * itemsPerPage;
    const stations = filteredStations.value.slice(start, start + itemsPerPage);
    
    // Process chart data for each station
    return stations.map(station => ({
        ...station,
        chartData: processStationData(station)
    }));
});

// Pagination methods
const nextPage = () => {
    if (currentPage.value < totalPages.value) {
        currentPage.value++
    }
}

const prevPage = () => {
    if (currentPage.value > 1) {
        currentPage.value--
    }
}

// Watch for brand changes to reset pagination
watch(selectedBrand, (newBrand) => {
    currentPage.value = 1;
    
    // Set default sensor type for each brand
    switch (newBrand) {
        case '3D_Paws':
            selectedSensorType.value = 'bt1';
            break;
        case 'Zentra':
            selectedSensorType.value = 'Air Temperature';
            break;
        case 'Allmeteo':
            selectedSensorType.value = 'wind_ave10';
            break;
    }
}, { immediate: true });

// Update the sensorConfig object
const sensorConfig = {
    // PAWS sensors
    'bt1': { name: 'Temperature 1', unit: '°C', icon: 'temperature-half' },
    'mt1': { name: 'Temperature 2', unit: '°C', icon: 'temperature-half' },
    'ws': { name: 'Wind Speed', unit: 'm/s', icon: 'wind' },
    'wd': { name: 'Wind Direction', unit: '°', icon: 'compass' },
    'rg': { name: 'Precipitation', unit: 'mm', icon: 'cloud-rain' },
    'bp1': { name: 'Pressure', unit: 'hPa', icon: 'gauge' },
    'sv1': { name: 'Downwelling Visible', unit: 'W/m²', icon: 'sun' },
    'si1': { name: 'Downwelling Infrared', unit: 'W/m²', icon: 'temperature-high' },
    'su1': { name: 'Downwelling Ultraviolet', unit: 'W/m²', icon: 'sun' },
    'bpc': { name: 'Battery Percent', unit: '%', icon: 'battery-half' },
    'css': { name: 'Cell Signal Strength', unit: '%', icon: 'signal' },
    
    // Zentra sensors
    'Solar Radiation': { name: 'Solar Radiation', unit: 'W/m²', icon: 'sun' },
    'Precipitation': { name: 'Precipitation', unit: 'mm', icon: 'cloud-rain' },
    'Wind Speed': { name: 'Wind Speed', unit: 'm/s', icon: 'wind' },
    'Air Temperature': { name: 'Air Temperature', unit: '°C', icon: 'temperature-half' },
    'Relative Humidity': { name: 'Relative Humidity', unit: '%', icon: 'droplet' },
    'Atmospheric Pressure': { name: 'Atmospheric Pressure', unit: 'kPa', icon: 'gauge' },
    
    // Allmeteo sensors
    'wind_ave10': { name: 'Wind Speed (Average)', unit: 'm/s', icon: 'wind' },
    'dir_ave10': { name: 'Wind Direction (Average)', unit: '°', icon: 'compass' },
    'battery': { name: 'Battery', unit: 'V', icon: 'battery-half' }
};

// Add icons to library
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

// Format value based on sensor type
const formatValue = (value: number | null): string => {
    if (value === null || value === undefined) return 'N/A';
    const config = sensorConfig[selectedSensorType.value];
    if (!config) return 'N/A';
    return `${value.toFixed(1)}${config.unit}`;
};

// Calculate change for the selected sensor
const calculateChange = (station: Station): string => {
    if (!station.measurements || station.measurements.length < 2) return 'No data';
    const latest = station.measurements[0]?.value;
    const previous = station.measurements[1]?.value;
    if (latest === undefined || previous === undefined) return 'No data';
    const change = latest - previous;
    return `${change.toFixed(1)}${sensorConfig[selectedSensorType.value]?.unit || ''}`;
};

// Get trend text class
const getTrendTextClass = (station: Station): string => {
    const change = calculateChange(station);
    if (!change || change === 'No data') return 'text-warning';
    return parseFloat(change) > 0 ? 'text-success' : 'text-danger';
};

// Update the watch section to use the station data directly
watch([() => selectedSensorType.value], () => {
    if (pawsStations.value.length > 0) {
        pawsStations.value.forEach(station => {
            station.chartData = getChartSeries(station);
        });
    }
}, { immediate: true });

// Add this computed property
const filteredSensorConfig = computed(() => {
    const config = {};
    
    switch (selectedBrand.value) {
        case '3D_Paws':
            Object.entries(sensorConfig).forEach(([key, value]) => {
                if (['bt1', 'mt1', 'ws', 'wd', 'rg', 'bp1', 'sv1', 'si1', 'su1', 'bpc', 'css'].includes(key)) {
                    config[key] = value;
                }
            });
            break;
        case 'Zentra':
            Object.entries(sensorConfig).forEach(([key, value]) => {
                if (['Solar Radiation', 'Precipitation', 'Wind Speed', 'Air Temperature', 
                     'Relative Humidity', 'Atmospheric Pressure'].includes(key)) {
                    config[key] = value;
                }
            });
            break;
        case 'Allmeteo':
            Object.entries(sensorConfig).forEach(([key, value]) => {
                if (['wind_ave10', 'dir_ave10', 'battery'].includes(key)) {
                    config[key] = value;
                }
            });
            break;
    }
    return config;
});

// Keep the debounce function
const debounce = (fn: Function, wait: number) => {
    let timeout: NodeJS.Timeout;
    return function executedFunction(...args: any[]) {
        const later = () => {
            clearTimeout(timeout);
            fn(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
};

// Optimize the station data processing
const processStationData = (station: Station) => {
    if (!station.measurements?.length) return null;

    const last24Hours = station.measurements
        .filter(m => m.sensor_type === selectedSensorType.value)
        .slice(-24); // Only take last 24 points

    return [{
        name: sensorConfig[selectedSensorType.value]?.name || selectedSensorType.value,
        data: last24Hours.map(item => ({
            x: new Date(`${item.date}T${item.time}`).getTime(),
            y: parseFloat(item.value.toString())
        }))
    }];
};

// Update the watch to use the optimized approach
watch([selectedSensorType, () => measurements.value], () => {
    // The chart data will update automatically through the computed property
}, { deep: true });

// Add this computed property to get the current sensor's icon
const currentSensorIcon = computed(() => {
    const icon = sensorConfig[selectedSensorType.value]?.icon || 'temperature-half';
    // Remove 'fa-' prefix if it exists
    return icon.replace('fa-', '');
});

// Update the watch for selectedSensorType
watch([selectedSensorType, selectedBrand], ([newSensorType, newBrand]) => {
    // Your existing watch logic...
    
    // Force icon update
    nextTick(() => {
        const iconWrapper = document.querySelector('.temperature-icon-wrapper');
        if (iconWrapper) {
            // Force a DOM reflow
            iconWrapper.classList.remove('icon-update');
            void iconWrapper.offsetWidth;
            iconWrapper.classList.add('icon-update');
        }
    });
}, { immediate: true });
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
    gap: 0.5rem;
}

.page-link {
    border-radius: 6px;
    padding: 0.5rem 1rem;
    color: #6c757d;
    background-color: #f8f9fa;
    border: none;
    transition: all 0.3s ease;
}

.page-link:hover {
    color: #7A70BA;
    background-color: #e9ecef;
}

.page-item.active .page-link {
    background-color: #7A70BA;
    color: white;
}

.page-item.disabled .page-link {
    background-color: #e9ecef;
    color: #adb5bd;
    cursor: not-allowed;
}

.temperature-icon-wrapper {
    width: 48px;
    height: 48px;
    display: flex;
    align-items: center;
    justify-content: center;
    background-color: rgba(var(--bs-primary-rgb), 0.1);
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
    width: 18px !important;
    height: 18px !important;
    stroke-width: 2.5;
    vertical-align: middle;
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
    margin-top: auto;
    min-height: 100px;
    contain: strict;
    transform: translateZ(0); /* Force GPU acceleration */
    overflow: visible !important;
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

/* Add these styles to handle tooltip positioning */
:deep(.apexcharts-tooltip) {
    z-index: 100;
    background: #fff;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

:deep(.apexcharts-tooltip-series-group) {
    padding: 8px;
}

/* Ensure chart container doesn't clip tooltips */
.chart-container {
    overflow: visible !important;
}

/* Ensure parent containers don't clip tooltips */
.station-card {
    overflow: visible !important;
}

.card-body {
    overflow: visible !important;
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
</style>