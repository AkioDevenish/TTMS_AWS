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
                        <td>{{ station.name }}</td>
                        <td>{{ station.brand_name }}</td>
                        <td>{{ formatTime(station.lastUpdate) }}</td>
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
import { ref, computed, onMounted, onUnmounted } from 'vue';
import Card1 from '@/components/common/card/CardData1.vue';
import axios from 'axios';
import { useStationData } from '@/composables/useStationData';

const { measurements, stationInfo, getLatestMeasurement } = useStationData();
const searchQuery = ref('');
const stations = ref<any[]>([]);
let updateInterval: number;

const calculateNextUpdate = (lastUpdate: Date): Date => {
    const next = new Date(lastUpdate);
    next.setHours(next.getHours() + 1);
    return next;
};

const formatTime = (date: Date): string => {
    return date.toLocaleTimeString();
};

const filteredStations = computed(() => {
    return stations.value.filter(station => 
        station.name.toLowerCase().includes(searchQuery.value.toLowerCase())
    );
});

const fetchStations = async () => {
    try {
        const response = await axios.get('http://127.0.0.1:8000/stations/');
        const stationsData = response.data;
        
        // Get latest measurement for each station
        const measurementPromises = stationsData.map(station => 
            axios.get(`http://127.0.0.1:8000/measurements/by_station/?station_id=${station.id}&limit=1`)
        );
        
        const measurements = await Promise.all(measurementPromises);
        
        stations.value = stationsData.map((station: any, index: number) => {
            const measurement = measurements[index].data[0];
            const timestamp = measurement ? new Date(`${measurement.date}T${measurement.time}`) : new Date();
            
            return {
                ...station,
                lastUpdate: timestamp,
                nextUpdate: calculateNextUpdate(timestamp),
                progress: 0
            };
        });
    } catch (error) {
        console.error('Error fetching stations:', error);
    }
};

// Start data refresh
const startDataRefresh = () => {
    fetchStations(); // Initial fetch
    updateInterval = setInterval(fetchStations, 60000); // Refresh every minute
};

onMounted(startDataRefresh);

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