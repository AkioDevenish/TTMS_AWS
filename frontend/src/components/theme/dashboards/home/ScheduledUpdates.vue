<template>
    <Card1 colClass="col-xl-6 col-lg-6 col-md-6 order-last" 
        headerTitle="true"
        title="Task Execution Status" 
        cardhaderClass="card-no-border pb-0" 
        cardbodyClass="active-members px-0">
        <!-- Station Table with Progress -->
        <div class="table-responsive theme-scrollbar" style="height: 300px;">
            <table class="table table-sm display mb-0" style="width:100%">
                <thead>
                    <tr>
                        <th class="py-2">Station Name</th>
                        <th class="py-2">Status</th>
                        <th class="py-2">Last Update</th>
                        <th class="py-2">Next Update In</th>
                        <th class="py-2">Progress</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="station in stations" :key="station.id">
                        <td>{{ station.name }}</td>
                        <td>
                            <p class="members-box text-center" 
                               :class="getStatusClass(station)">
                                {{ getDisplayStatus(station) }}
                            </p>
                        </td>
                        <td>{{ formatLastUpdate(station.last_updated) }}</td>
                        <td>{{ formatTimeUntilNext(station.time_until_next) }}</td>
                        <td>
                            <div v-if="hasStarted(station)" class="progress progress-striped-primary">
                                <div class="progress-bar" 
                                     :class="getProgressClass(station)"
                                     role="progressbar" 
                                     :style="{ width: `${station.progress}%` }"
                                     :aria-valuenow="station.progress"
                                     aria-valuemin="0"
                                     aria-valuemax="100">
                                    {{ Math.round(station.progress) }}%
                                </div>
                            </div>
                            <div v-else class="text-muted">
                                Not Started
                            </div>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
    </Card1>
</template>

<script lang="ts" setup>
import { ref, onMounted, onUnmounted } from 'vue';
import Card1 from '@/components/common/card/CardData1.vue';
import axios from 'axios';

interface Station {
    id: number;
    name: string;
    brand: string;
    status: string;
    last_updated: string | null;
    time_until_next: number;
    progress: number;
}

// State
const stations = ref<Station[]>([]);

// Methods
const hasStarted = (station: Station): boolean => {
    return station.last_updated !== null && station.status !== 'Not Started';
};

const formatLastUpdate = (lastUpdate: string | null): string => {
    if (!lastUpdate) return 'Never';
    return new Date(lastUpdate).toLocaleString();
};

const formatTimeUntilNext = (timeInSeconds: number): string => {
    const station = stations.value.find(s => s.time_until_next === timeInSeconds);
    if (!station || !hasStarted(station)) {
        return 'Not Scheduled';
    }
    if (timeInSeconds <= 0) return 'Due now';
    const minutes = Math.floor(timeInSeconds / 60);
    const seconds = Math.floor(timeInSeconds % 60);
    return `${minutes}:${seconds.toString().padStart(2, '0')}`;
};

const getDisplayStatus = (station: Station): string => {
    if (!hasStarted(station)) return 'Not Started';
    return station.status;
};

const getStatusClass = (station: Station) => {
    if (!hasStarted(station)) {
        return 'bg-light-secondary font-secondary';
    }
    return {
        'bg-light-primary font-primary': station.status === 'success',
        'bg-light-warning font-warning': station.status === 'running',
        'bg-light-danger font-danger': station.status === 'failed'
    }
};

const getProgressClass = (station: Station) => {
    return {
        'bg-primary': station.status === 'success',
        'bg-warning': station.status === 'running',
        'bg-danger': station.status === 'failed'
    }
};

const fetchStations = async () => {
    try {
        const response = await axios.get('/task-execution-status/');
        stations.value = response.data;
    } catch (error) {
        console.error('Error fetching stations:', error);
    }
};

// Lifecycle hooks
onMounted(() => {
    fetchStations();
});
</script>

<style scoped>
/* Add these styles for consistent sizing */
.table-responsive.theme-scrollbar {
    height: 212px !important;
    overflow-y: auto;
}

.table {
    margin-bottom: 0;
}

.members-box {
    padding: 4px 8px;
    border-radius: 5px;
    font-size: 12px;
    font-weight: 500;
}

/* Keep your existing styles for progress bars and other elements */
.progress {
    height: 10px;
    margin-bottom: 0;
    position: relative;
}

.progress-striped-primary {
    background-color: #eee;
    border-radius: 4px;
}

.bg-light-primary {
    background-color: rgba(122, 112, 186, 0.1);
    color: #7A70BA;
}

.bg-light-warning {
    background-color: rgba(255, 193, 7, 0.1);
    color: #ffc107;
}

.bg-light-danger {
    background-color: rgba(220, 53, 69, 0.1);
    color: #dc3545;
}

.bg-light-secondary {
    background-color: rgba(108, 117, 125, 0.1);
    color: #6c757d;
}

.cursor-pointer {
    cursor: pointer;
}

.progress-bar {
    font-size: 0.85rem;
    line-height: 1;
    font-weight: 500;
    position: relative;
}

.progress-bar::after {
    content: attr(aria-valuenow) '%';
    position: absolute;
    right: 4px;
    top: -18px;
    font-size: 0.85rem;
    color: #495057;
}

.text-muted {
    color: #6c757d;
    font-size: 0.85rem;
}
</style>