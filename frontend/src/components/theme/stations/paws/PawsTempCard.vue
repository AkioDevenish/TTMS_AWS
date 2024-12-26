<template>
    <div>
        <div class="row g-2">
            <!-- Loop through transformed data and display cards for each measurement -->
            <div class="col-xl-6 col-lg-12 box-col-12 proorder-md-3" v-for="(item, index) in localPawsData" :key="index">
                <Card1 :cardbodyClass="item.cardclass">
                    <div class="d-flex align-items-center justify-content-between">
                        <div>
                            <h4 class="mb-0">{{ item.number }}</h4>
                            <div class="d-flex align-items-center">
                                <span :class="item.fontclass" class="me-2">
                                    <i :class="item.icon"></i>
                                    {{ parseFloat(item.change) > 0 ? '+' : ''}}{{ item.change }}{{ item.unit }}
                                </span>
                            </div>
                            <h6 class="mb-0 mt-2">{{ item.text }}</h6>
                            <p class="f-light mb-0">Last updated: {{ item.month }}</p>
                        </div>
                        <div class="flex-shrink-0">
                            <img :src="getImages(item.img)" alt="" />
                        </div>
                    </div>
                </Card1>
            </div>
        </div>
    </div>
</template>

<script lang="ts" setup>
import { ref, onMounted, defineAsyncComponent, watch, defineProps } from 'vue';
import axios from 'axios';
import { getImages } from "@/composables/common/getImages";

const Card1 = defineAsyncComponent(() => import("@/components/common/card/CardData1.vue"));

interface CardData {
    number: string;
    text: string;
    iconclass: string;
    icon: string;
    img: string;
    cardclass: string;
    fontclass: string;
    total: string;
    month: string;
    timestamp: string;
    change: string;
    rateOfChange: string;
    timeDiff: string;
    trend: string;
    unit: string;
}

const props = defineProps({
    selectedStation: {
        type: Number,
        required: true
    }
});

const localPawsData = ref<CardData[]>([]);
const sensors = ref([]);

// Memoize date parsing to avoid repeated operations
const dateCache = new Map<string, number>();
const getDateTime = (date: string, time: string): number => {
    const key = `${date}T${time}`;
    if (!dateCache.has(key)) {
        dateCache.set(key, new Date(key).getTime());
    }
    return dateCache.get(key)!;
};

// Optimized sorting function
const sortMeasurementsByDate = (a: any, b: any): number => {
    const dateTimeA = getDateTime(a.date, a.time);
    const dateTimeB = getDateTime(b.date, b.time);
    return dateTimeB - dateTimeA;
};

// Optimized value change calculation
const calculateValueChange = (measurements: any[], sensorType: string) => {
    if (!measurements?.length || measurements.length < 2) {
        return { 
            change: '0',
            trend: 'stable',
            rateOfChange: '0',
            timeDiff: '2.0'
        };
    }

    // Sort measurements by date and time
    const sortedMeasurements = measurements.sort(sortMeasurementsByDate);
    const latest = sortedMeasurements[0];
    const latestTime = getDateTime(latest.date, latest.time);
    
    // Find measurement closest to 2 hours ago
    const twoHoursAgo = latestTime - (2 * 60 * 60 * 1000); // 2 hours in milliseconds
    let previous = sortedMeasurements[1]; // Default to second measurement
    
    for (let i = 1; i < sortedMeasurements.length; i++) {
        const measurement = sortedMeasurements[i];
        const measurementTime = getDateTime(measurement.date, measurement.time);
        if (measurementTime <= twoHoursAgo) {
            previous = measurement;
            break;
        }
    }

    const latestValue = parseFloat(latest.value);
    const previousValue = parseFloat(previous.value);
    const change = latestValue - previousValue;

    // Use predefined thresholds from sensor config
    const threshold = sensorConfig[sensorType]?.threshold || 0.1;
    const trend = Math.abs(change) < threshold ? 'stable' : 
                 change > 0 ? 'increasing' : 'decreasing';

    if (process.env.NODE_ENV === 'development') {
        console.log(`${sensorType} calculations:`, {
            latest: { value: latestValue, date: latest.date, time: latest.time },
            previous: { value: previousValue, date: previous.date, time: previous.time },
            change,
            trend
        });
    }

    return {
        change: change.toFixed(1),
        rateOfChange: (change / 2).toFixed(1),
        trend,
        timeDiff: '2.0'
    };
};

// Enhanced sensor configuration with thresholds
const sensorConfig: Record<string, { name: string; unit: string; threshold: number }> = {
    // PAWS sensors
    'bp1': { name: 'BMX280 Pressure', unit: 'hPa', threshold: 0.5 },
    'bt1': { name: 'BMX280 Temperature', unit: '°C', threshold: 0.1 },
    'mt1': { name: 'MCP9808 Temperature', unit: '°C', threshold: 0.1 },
    'ws': { name: 'Wind Speed', unit: 'm/s', threshold: 0.5 },
    'wd': { name: 'Wind Direction', unit: '°', threshold: 5 },
    'rg': { name: 'Rain Gauge', unit: 'mm', threshold: 0.1 },
    'sv1': { name: 'SI1145 Visible', unit: 'W/m²', threshold: 1 },
    'si1': { name: 'SI1145 Infrared', unit: 'W/m²', threshold: 1 },
    'su1': { name: 'SI1145 Ultraviolet', unit: 'W/m²', threshold: 1 },
    'bpc': { name: 'Battery Percent', unit: '%', threshold: 1 },
    'css': { name: 'Cell Signal Strength', unit: '%', threshold: 1 }
};

// Optimized measurements transformation
const transformMeasurements = (measurements: any[]): CardData[] => {
    if (!measurements?.length) return [];

    // Group measurements by sensor type in a single pass
    const measurementsByType = new Map<string, any[]>();
    for (const measurement of measurements) {
        const type = measurement.sensor_type;
        if (!measurementsByType.has(type)) {
            measurementsByType.set(type, []);
        }
        measurementsByType.get(type)!.push(measurement);
    }

    // Transform grouped measurements
    return Array.from(measurementsByType.entries()).map(([sensorType, sensorMeasurements]) => {
        const config = sensorConfig[sensorType];
        if (!config) return null;

        const changes = calculateValueChange(sensorMeasurements, sensorType);
        const latest = sensorMeasurements.sort(sortMeasurementsByDate)[0];
        const value = parseFloat(latest.value);

        return {
            number: `${value.toFixed(1)} ${config.unit}`,
            text: config.name,
            iconclass: `bg-light-${changes.trend === 'increasing' ? 'success' : 
                                   changes.trend === 'decreasing' ? 'danger' : 'warning'}`,
            icon: `icon-${changes.trend === 'increasing' ? 'arrow-up font-success' : 
                         changes.trend === 'decreasing' ? 'arrow-down font-danger' : 'minus font-warning'}`,
            img: 'dashboard-4/icon/student.png',
            cardclass: "student",
            fontclass: `font-${changes.trend === 'increasing' ? 'success' : 
                               changes.trend === 'decreasing' ? 'danger' : 'warning'}`,
            total: Math.abs(value).toFixed(1),
            month: new Date(`${latest.date}T${latest.time}`).toLocaleString('en-US', {
                year: 'numeric',
                month: '2-digit',
                day: '2-digit',
                hour: '2-digit',
                minute: '2-digit',
                hour12: true
            }),
            timestamp: `${latest.date}T${latest.time}`,
            change: changes.change,
            rateOfChange: `${changes.rateOfChange}${config.unit}`,
            timeDiff: changes.timeDiff,
            trend: changes.trend,
            unit: config.unit
        };
    }).filter(Boolean) as CardData[];
};

// Optimized data fetching with better error handling
const fetchData = async () => {
    if (!props.selectedStation) return;

    try {
        if (process.env.NODE_ENV === 'development') {
            console.log('Fetching data for station:', props.selectedStation);
        }

        const [sensorsResponse, measurementsResponse] = await Promise.all([
            axios.get('http://127.0.0.1:8000/sensors/'),
            axios.get(`http://127.0.0.1:8000/measurements/by_station/?station_id=${props.selectedStation}`)
        ]);

        sensors.value = sensorsResponse.data;
        localPawsData.value = transformMeasurements(measurementsResponse.data);
    } catch (error: any) {
        console.error('Error fetching data:', {
            message: error.message,
            status: error.response?.status,
            data: error.response?.data
        });
        localPawsData.value = [];
    }
};

// Watch for station changes
watch(() => props.selectedStation, (newVal) => {
    console.log('Selected station changed to:', newVal);
    fetchData();
});

// Initial data fetch
onMounted(fetchData);
</script>

<style scoped>
/* Custom styles for the dropdown and cards */
.instrument-tabs .nav-link.active {
    background-color: #007bff;
    color: white;
}

.instrument-tabs .nav-item {
    cursor: pointer;
}

.studay-statistics {
    margin-top: 10px;
}

.dropdown-menu {
    max-height: 300px; /* Optional: add scroll if there are too many options */
    overflow-y: auto;
}
</style>
  