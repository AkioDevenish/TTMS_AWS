<template>
    <Card1 headerTitle="true" title="Scheduled Updates" cardhaderClass="card-no-border" cardbodyClass="pt-0">
        <div class="input-group mb-3">
            <input type="text" class="form-control" v-model="searchQuery" placeholder="Search stations...">
        </div>
        <div class="table-responsive theme-scrollbar">
            <table class="table display" style="width:100%">
                <thead>
                    <tr>
                        <th>Name</th>
                        <th>Brand</th>
                        <th>Time</th>
                        <th>Progress</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="station in filteredStations" :key="station.id">
                        <td>
                            <div class="d-flex align-items-center">
                                <h5>{{ station.name }}</h5>
                            </div>
                        </td>
                        <td>{{ station.brand_name }}</td>
                        <td>{{ formatTime(station.nextUpdate) }}</td>
                        <td>
                            <div class="progress progress-striped-primary">
                                <div class="progress-bar" role="progressbar" 
                                     :style="{ width: `${station.progress}%` }">
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
import { ref, computed, defineAsyncComponent, onMounted, onUnmounted } from 'vue';
import axios from 'axios';

const Card1 = defineAsyncComponent(() => import("@/components/common/card/CardData1.vue"));

interface Station {
    id: number;
    name: string;
    brand_name: string;
    lastUpdate: Date;
    nextUpdate: Date;
    progress: number;
}

const stations = ref<Station[]>([]);
const searchQuery = ref('');
let updateInterval: number;

// Computed property for filtered stations using Map for better performance
const stationsMap = new Map<string, Station>();
const filteredStations = computed(() => {
    if (!searchQuery.value) return stations.value;
    const query = searchQuery.value.toLowerCase();
    return Array.from(stationsMap.values()).filter(station => 
        station.name.toLowerCase().includes(query) ||
        station.brand_name.toLowerCase().includes(query)
    );
});

const formatTime = (date: Date): string => {
    return date.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit', hour12: true });
};

const calculateNextUpdate = (lastUpdate: Date): Date => {
    const next = new Date(lastUpdate);
    next.setHours(next.getHours() + 1);
    return next;
};

// Optimized fetch using single endpoint and Promise.all
const fetchStations = async () => {
    try {
        const response = await axios.get('http://127.0.0.1:8000/stations/');
        const stationsData = response.data;
        
        // Pre-populate the stations with basic info
        stations.value = stationsData.map((station: any) => ({
            id: station.id,
            name: station.name,
            brand_name: station.brand_name,
            lastUpdate: new Date(),
            nextUpdate: calculateNextUpdate(new Date()),
            progress: 0
        }));

        // Update the Map for faster lookups
        stations.value.forEach(station => {
            stationsMap.set(station.id.toString(), station);
        });

        // Fetch latest measurements in parallel
        const measurementPromises = stationsData.map((station: any) => 
            axios.get(`http://127.0.0.1:8000/measurements/by_station/?station_id=${station.id}&limit=1`)
        );

        const measurements = await Promise.all(measurementPromises);
        
        // Update stations with measurement data
        measurements.forEach((response, index) => {
            if (response.data.length > 0) {
                const measurement = response.data[0];
                const station = stationsMap.get(stationsData[index].id.toString());
                if (station) {
                    station.lastUpdate = new Date(`${measurement.date}T${measurement.time}`);
                    station.nextUpdate = calculateNextUpdate(station.lastUpdate);
                }
            }
        });
    } catch (error) {
        console.error('Error fetching stations:', error);
    }
};

const updateProgress = () => {
    const now = new Date();
    stations.value.forEach(station => {
        const timeSinceLastUpdate = now.getTime() - station.lastUpdate.getTime();
        const totalInterval = 3600000;
        station.progress = Math.min((timeSinceLastUpdate / totalInterval) * 100, 100);
    });
};

onMounted(() => {
    fetchStations();
    updateInterval = setInterval(updateProgress, 1000);
});

onUnmounted(() => {
    clearInterval(updateInterval);
});
</script>

<style scoped>
.input-group {
    margin: 1rem;
    max-width: 300px;
}

.form-control {
    border-radius: 0.375rem;
    border: 1px solid #dee2e6;
    padding: 0.5rem;
}

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