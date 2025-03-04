<template>
    <Card1 colClass="col-xl-6 col-lg-6 col-md-6 order-last" 
        headerTitle="true"
        title="Task Execution Status" 
        cardhaderClass="card-no-border pb-0" 
        cardbodyClass="active-members px-0">
        <!-- Brand tabs section -->
        <ul class="nav nav-tabs border-tab nav-primary" role="tablist">
            <li class="nav-item" v-for="brand in stationBrands" :key="brand">
                <a class="nav-link" 
                   :class="{ active: currentBrand === brand }" 
                   @click="currentBrand = brand"
                   role="tab">
                    {{ brand }}
                </a>
            </li>
        </ul>

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
                    <tr v-for="station in filteredStations" :key="station.id">
                        <td>{{ station.name }}</td>
                        <td>
                            <p class="members-box text-center" 
                               :class="getStatusClass(station)">
                                {{ station.status }}
                            </p>
                        </td>
                        <td>{{ new Date(station.last_updated).toLocaleString() }}</td>
                        <td>{{ formatTimeUntilNext(station.time_until_next) }}</td>
                        <td>
                            <div class="progress progress-striped-primary">
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

interface Station {
    id: number;
    name: string;
    brand: string;
    status: string;
    last_updated: string;
    time_until_next: number;
    progress: number;
}

// State
const stations = ref<Station[]>([]);
const currentBrand = ref('All');

// Computed properties
const stationBrands = computed(() => ['All', ...new Set(stations.value.map(s => s.brand))]);

const filteredStations = computed(() => {
    return currentBrand.value === 'All' 
        ? stations.value 
        : stations.value.filter(s => s.brand === currentBrand.value);
});

// Methods
const formatTimeUntilNext = (timeInSeconds: number): string => {
    if (timeInSeconds <= 0) return 'Due now';
    const minutes = Math.floor(timeInSeconds / 60);
    const seconds = Math.floor(timeInSeconds % 60);
    return `${minutes}:${seconds.toString().padStart(2, '0')}`;
};

const getStatusClass = (station: Station) => {
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
    const interval = setInterval(fetchStations, 1000);
    onUnmounted(() => clearInterval(interval));
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

.nav-tabs .nav-link {
    color: #495057;
    cursor: pointer;
}

.nav-tabs .nav-link.active {
    color: #7A70BA;
    border-bottom: 2px solid #7A70BA;
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
</style>