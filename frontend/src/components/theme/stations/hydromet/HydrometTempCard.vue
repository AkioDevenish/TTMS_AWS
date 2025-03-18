<template>
    <div>
      <div class="row g-2">
        <div class="col-xl-6 col-lg-12 box-col-12 proorder-md-3" v-for="(item, index) in localOttData" :key="index">
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
  import { useStationData } from '@/composables/useStationData';
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
  
  const { 
    measurements,
    stationInfo,
    fetchStationData,
    formatDateTime
  } = useStationData();
  
  const localOttData = ref<CardData[]>([]);
  
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
    '5 min rain': { name: '5 min Rain', unit: 'mm', threshold: 0.1 },
    'Air Temperature': { name: 'Air Temperature', unit: '°C', threshold: 0.1 },
    'Barometric Pressure': { name: 'Barometric Pressure', unit: 'hPa', threshold: 0.5 },
    'Baro Tendency': { name: 'Baro Tendency', unit: 'hPa', threshold: 0.5 },
    'Battery': { name: 'Battery', unit: 'V', threshold: 0.1 },
    'Daily Rain': { name: 'Daily Rain', unit: 'mm', threshold: 0.1 },
    'Dew Point': { name: 'Dew Point', unit: '°C', threshold: 0.1 },
    'Gust Direction': { name: 'Gust Direction', unit: '°', threshold: 5 },
    'Gust Speed': { name: 'Gust Speed', unit: 'knots', threshold: 0.2 },
    'Hours of Sunshine': { name: 'Hours of Sunshine', unit: 'hr', threshold: 0.1 },
    'Maximum Air Temperature': { name: 'Maximum Air Temperature', unit: '°C', threshold: 0.1 },
    'Minimum Air Temperature': { name: 'Minimum Air Temperature', unit: '°C', threshold: 0.1 },
    'Relative Humidity': { name: 'Relative Humidity', unit: '%', threshold: 1 },
    'Solar Radiation Avg': { name: 'Solar Radiation Average', unit: 'Wh/m²', threshold: 1 },
    'Solar Radiation Total': { name: 'Solar Radiation Total', unit: 'Wh/m²', threshold: 1 },
    'Wind Dir Average': { name: 'Wind Direction Average', unit: '°', threshold: 5 },
    'Wind Dir Inst': { name: 'Wind Direction Instantaneous', unit: '°', threshold: 5 },
    'Wind Speed Average': { name: 'Wind Speed Average', unit: 'knots', threshold: 0.2 },
    'Wind Speed Inst': { name: 'Wind Speed Instantaneous', unit: 'knots', threshold: 0.2 }
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
  
  // Watch for station changes
  watch(() => props.selectedStation, (newStationId) => {
    if (newStationId) {
      fetchStationData(newStationId);
    }
  }, { immediate: true });
  
  // Watch for measurements changes
  watch(() => measurements.value, (newMeasurements) => {
    if (!newMeasurements?.length) {
      localOttData.value = [];
      return;
    }
    localOttData.value = transformMeasurements(newMeasurements);
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