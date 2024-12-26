<template>
    <Card1 headerTitle="true" title="Scheduled Updates" cardhaderClass="card-no-border" cardbodyClass="pt-0">
        <div class="table-responsive theme-scrollbar">
            <table class="table display" style="width:100%">
                <thead>
                    <tr>
                        <th>Name</th>
                        <th></th>
                        <th>Time</th>
                        <th>Progress</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="(station, index) in stations" :key="index">
                        <td>
                            <div class="d-flex align-items-center">
                                <h5>{{ station.name }}</h5>
                            </div>
                        </td>
                        <td></td>
                        <td>{{ formatTime(station.nextUpdate) }}</td>
                        <td>
                            <div class="progress progress-striped-primary">
                                <div class="progress-bar" role="progressbar" 
                                     :style="{ width: `${station.progress}%` }"
                                     aria-valuenow="10" aria-valuemin="0" 
                                     aria-valuemax="100">
                                </div>
                            </div>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
    </Card1>
</template>

<script lang="ts" setup>
import { ref, defineAsyncComponent, onMounted, onUnmounted } from 'vue';
import axios from 'axios';

const Card1 = defineAsyncComponent(() => import("@/components/common/card/CardData1.vue"));

interface Station {
    id: number;
    name: string;
    lastUpdate: Date;
    nextUpdate: Date;
    progress: number;
}

const stations = ref<Station[]>([]);
let updateInterval: number;

const formatTime = (date: Date): string => {
    return date.toLocaleTimeString('en-US', {
        hour: '2-digit',
        minute: '2-digit',
        hour12: true
    });
};

const calculateNextUpdate = (lastUpdate: Date): Date => {
    const next = new Date(lastUpdate);
    next.setHours(next.getHours() + 1);
    return next;
};

const fetchStations = async () => {
    try {
        const [stationsResponse, measurementsResponse] = await Promise.all([
            axios.get('http://127.0.0.1:8000/stations/'),
            axios.get('http://127.0.0.1:8000/measurements/')
        ]);

        // Get latest measurement for each station
        const latestMeasurements = new Map();
        measurementsResponse.data.forEach((measurement: any) => {
            const stationId = measurement.station;
            const timestamp = new Date(`${measurement.date}T${measurement.time}`);
            const current = latestMeasurements.get(stationId);
            
            if (!current || timestamp > current) {
                latestMeasurements.set(stationId, timestamp);
            }
        });

        stations.value = stationsResponse.data.map((station: any) => {
            const lastUpdate = latestMeasurements.get(station.id) || new Date();
            return {
                id: station.id,
                name: station.name,
                lastUpdate: lastUpdate,
                nextUpdate: calculateNextUpdate(lastUpdate),
                progress: 0
            };
        });
    } catch (error) {
        console.error('Error fetching stations:', error);
    }
};

const updateProgress = () => {
    const now = new Date();
    stations.value.forEach(station => {
        const timeSinceLastUpdate = now.getTime() - station.lastUpdate.getTime();
        const totalInterval = 3600000; // 1 hour in milliseconds
        const progress = (timeSinceLastUpdate / totalInterval) * 100;
        
        if (progress >= 100) {
            station.lastUpdate = now;
            station.nextUpdate = calculateNextUpdate(now);
            station.progress = 0;
        } else {
            station.progress = progress;
        }
    });
};

onMounted(() => {
    fetchStations();
    updateInterval = setInterval(updateProgress, 1000) as unknown as number;
});

onUnmounted(() => {
    clearInterval(updateInterval);
});
</script>

<style scoped>
.progress {
    height: 8px;
    margin-bottom: 0;
}

.progress-striped-primary {
    background-color: rgba(99, 98, 231, 0.1);
    .progress-bar {
        background-color: #6362e7;
    }
}

.progress-striped-secondary {
    background-color: rgba(255, 197, 0, 0.1);
    .progress-bar {
        background-color: #ffc500;
    }
}

.progress-striped-success {
    background-color: rgba(81, 187, 37, 0.1);
    .progress-bar {
        background-color: #51bb25;
    }
}

.progress-striped {
    background-image: linear-gradient(45deg, rgba(255, 255, 255, 0.15) 25%, transparent 25%, transparent 50%, rgba(255, 255, 255, 0.15) 50%, rgba(255, 255, 255, 0.15) 75%, transparent 75%, transparent);
    background-size: 1rem 1rem;
    animation: progress-bar-stripes 1s linear infinite;
}

@keyframes progress-bar-stripes {
    0% { background-position: 1rem 0; }
    100% { background-position: 0 0; }
}
</style>