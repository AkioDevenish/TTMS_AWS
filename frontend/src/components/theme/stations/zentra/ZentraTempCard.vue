<template>
  <div>
    <div class="row g-2">
      <div class="col-xl-6 col-lg-12 box-col-12 proorder-md-3" v-for="(item, index) in localZentraData" :key="index">
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
import { ref, defineAsyncComponent, watch, defineProps } from 'vue';
import { getImages } from "@/composables/common/getImages";
const Card1 = defineAsyncComponent(() => import("@/components/common/card/CardData1.vue"));
const props = defineProps({
    selectedStation: {
        type: Number,
        required: true
    },
    measurements: {
        type: Array,
        default: () => []
    },
    stationInfo: {
        type: Object,
        default: () => ({})
    }
});
const localZentraData = ref<any[]>([]);
const fallbackImg = 'dashboard-4/icon/student.png';

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

const formatDateTime = {
  date: (timestamp: string) => {
    try {
      if (!timestamp) return 'Invalid Date';
      const date = new Date(timestamp);
      if (isNaN(date.getTime())) return 'Invalid Date';
      return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit'
      });
    } catch {
      return 'Invalid Date';
    }
  },
  time: (timestamp: string) => {
    try {
      const date = new Date(timestamp);
      if (isNaN(date.getTime())) return 'Invalid Time';
      return date.toLocaleTimeString('en-US', {
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit',
        hour12: true
      });
    } catch {
      return 'Invalid Time';
    }
  }
};

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

const sensorConfig: Record<string, { name: string; unit: string; threshold: number }> = {
  'Solar Radiation': { name: 'Solar Radiation', unit: 'W/m²', threshold: 1 },
  'Precipitation': { name: 'Precipitation', unit: 'mm', threshold: 0.1 },
  'Air Temperature': { name: 'Air Temperature', unit: '°C', threshold: 0.1 },
  'Relative Humidity': { name: 'Relative Humidity', unit: '%', threshold: 1 },
  'Atmospheric Pressure': { name: 'Atmospheric Pressure', unit: 'kPa', threshold: 0.5 },
  'Wind Speed': { name: 'Wind Speed', unit: 'm/s', threshold: 0.2 },
  'Wind Direction': { name: 'Wind Direction', unit: '°', threshold: 5 },
  'Battery Percent': { name: 'Battery Percent', unit: '%', threshold: 1 }
};

const calculateValueChange = (measurements: any[], sensorType: string) => {
  if (!measurements?.length || measurements.length < 2) {
    return { 
      change: '0',
      trend: 'stable',
      rateOfChange: '0',
      timeDiff: '2.0'
    };
  }

  const sortedMeasurements = measurements.sort(sortMeasurementsByDate);
  const latest = sortedMeasurements[0];
  const latestTime = getDateTime(latest.date, latest.time);
  
  const twoHoursAgo = latestTime - (2 * 60 * 60 * 1000);
  let previous = sortedMeasurements[1];
  
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

  const threshold = sensorConfig[sensorType]?.threshold || 0.1;
  const trend = Math.abs(change) < threshold ? 'stable' : 
               change > 0 ? 'increasing' : 'decreasing';

  return {
    change: change.toFixed(1),
    rateOfChange: (change / 2).toFixed(1),
    trend,
    timeDiff: '2.0'
  };
};

const transformMeasurements = (measurements: any[]): CardData[] => {
  if (!measurements?.length) return [];

  const measurementsByType = new Map<string, any[]>();
  for (const measurement of measurements) {
    const type = measurement.sensor_type;
    if (!measurementsByType.has(type)) {
      measurementsByType.set(type, []);
    }
    measurementsByType.get(type)!.push(measurement);
  }

  return Array.from(measurementsByType.entries())
    .map(([sensorType, sensorMeasurements]) => {
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
        month: formatDateTime.date(`${latest.date}T${latest.time}`) + ' ' + 
              formatDateTime.time(`${latest.date}T${latest.time}`),
        timestamp: `${latest.date}T${latest.time}`,
        change: changes.change,
        rateOfChange: `${changes.rateOfChange}${config.unit}`,
        timeDiff: changes.timeDiff,
        trend: changes.trend,
        unit: config.unit
      };
    })
    .filter(Boolean) as CardData[];
};

watch(() => props.measurements, (newMeasurements) => {
  localZentraData.value = transformMeasurements(newMeasurements).map(item => ({
    ...item,
    img: item.img || fallbackImg,
    month: formatDateTime.date(item.timestamp) + ' ' + formatDateTime.time(item.timestamp)
  }));
}, { immediate: true });
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