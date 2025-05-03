<template>
    <div>
        <div class="row g-2">
            <div class="col-xl-6 col-lg-12 box-col-12 proorder-md-3" v-for="(item, index) in localBaraniData" :key="index">
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
import { ref, defineAsyncComponent, watch } from 'vue';
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
    formatDateTime,
    getLast24HoursMeasurements
} = useStationData();

const localBaraniData = ref<CardData[]>([]);

// Enhanced sensor configuration with thresholds
const sensorConfig: Record<string, { name: string; unit: string; threshold: number }> = {
    'wind_ave10': { name: 'Wind Speed (Average)', unit: 'm/s', threshold: 0.5 },
    'wind_max10': { name: 'Wind Speed (Max)', unit: 'm/s', threshold: 0.5 },
    'wind_min10': { name: 'Wind Speed (Min)', unit: 'm/s', threshold: 0.5 },
    'dir_ave10': { name: 'Wind Direction (Average)', unit: '°', threshold: 5 },
    'dir_max10': { name: 'Wind Direction (Max)', unit: '°', threshold: 5 },
    'dir_hi10': { name: 'Wind Direction (High)', unit: '°', threshold: 5 },
    'dir_lo10': { name: 'Wind Direction (Low)', unit: '°', threshold: 5 },
    'battery': { name: 'Battery', unit: 'V', threshold: 5 }
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

    const sortedMeasurements = [...measurements].sort((a, b) => 
        new Date(`${b.date}T${b.time}`).getTime() - new Date(`${a.date}T${a.time}`).getTime()
    );
    
    const latest = sortedMeasurements[0];
    const previous = sortedMeasurements[1];

    const latestValue = parseFloat(latest.value);
    const previousValue = parseFloat(previous.value);
    const timeDiffHours = (new Date(`${latest.date}T${latest.time}`).getTime() - 
                          new Date(`${previous.date}T${previous.time}`).getTime()) / (1000 * 60 * 60);

    const valueDiff = latestValue - previousValue;
    const rateOfChange = valueDiff / timeDiffHours;

    return {
        change: valueDiff.toFixed(1),
        trend: valueDiff > 0 ? 'increasing' : valueDiff < 0 ? 'decreasing' : 'stable',
        rateOfChange: rateOfChange.toFixed(2),
        timeDiff: timeDiffHours.toFixed(1)
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
            const latest = sensorMeasurements[0];
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

watch(() => props.selectedStation, (newStationId) => {
    if (newStationId) {
        fetchStationData(newStationId);
    }
}, { immediate: true });

watch(() => getLast24HoursMeasurements.value, (newMeasurements) => {
    if (!newMeasurements?.length) {
        localBaraniData.value = [];
        return;
    }
    localBaraniData.value = transformMeasurements(newMeasurements);
}, { immediate: true });
</script>

<style scoped>
/* Custom styles for the cards */
.card {
    margin-bottom: 1rem;
}

.student {
    background-color: var(--light);
}
</style>