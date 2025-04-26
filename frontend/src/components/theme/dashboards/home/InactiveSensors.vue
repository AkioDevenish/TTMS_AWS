<template>
    <Card1 colClass="col-xl-12 col-lg-12 col-md-12 order-3" 
        headerTitle="true" 
        title="Inactive Sensors"
        cardhaderClass="card-no-border pb-0" 
        cardbodyClass="designer-card">
        
        <!-- Brand Tabs -->
        <ul class="nav nav-tabs border-tab nav-primary mb-4" role="tablist">
            <li class="nav-item" v-for="brand in uniqueBrands" :key="brand">
                <a class="nav-link" :class="{ active: selectedBrand === brand }" 
                   @click="selectedBrand = brand">
                    {{ brand }}
                </a>
            </li>
        </ul>

        <!-- Loading State -->
        <div v-if="isLoading" class="text-center py-5">
            <div class="spinner-border text-primary" role="status">
                <span class="visually-hidden">Loading...</span>
            </div>
        </div>

        <!-- No Data State -->
        <div v-else-if="!hasRecentData" class="text-center py-5">
            <div class="empty-state">
                <VueFeather type="alert-circle" size="48" class="text-muted mb-3" />
                <h5>No Data Available</h5>
                <p class="text-muted">No inactive sensors found in the last 24 hours.</p>
            </div>
        </div>

        <!-- Data Table -->
        <div v-else class="table-responsive theme-scrollbar px-0">
            <table class="table" id="information">
                <thead>
                    <tr>
                        <th class="px-3">Station Name</th>
                        <th>Sensor Type</th>
                        <th>Last Reading</th>
                        <th>Status</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="(sensor, index) in paginatedSensors" :key="index">
                        <td class="px-3">
                            <div class="d-flex align-items-center">
                                <h6 class="mb-0">{{ sensor.station_name }}</h6>
                            </div>
                        </td>
                        <td>{{ sensor.sensor_type }}</td>
                        <td>{{ formatDate(sensor.lastReading) }}</td>
                        <td>
                            <button class="btn btn-sm" :class="getStationClass(sensor)">
                                {{ sensor.status }}
                            </button>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
        
        <!-- Pagination -->
        <ul class="pagination mx-3 mt-3 justify-content-end" v-if="hasRecentData">
            <li class="page-item" :class="{ disabled: currentPage === 1 }">
                <a class="page-link cursor-pointer" @click="prev()">Previous</a>
            </li>
            <li class="page-item" v-for="i in totalPages" :key="i" 
                :class="{ active: i === currentPage }">
                <a class="page-link cursor-pointer" @click="currentPage = i">{{ i }}</a>
            </li>
            <li class="page-item" :class="{ disabled: currentPage === totalPages }">
                <a class="page-link cursor-pointer" @click="next()">Next</a>
            </li>
        </ul>
    </Card1>
</template>

<script lang="ts" setup>
import { ref, defineAsyncComponent, onMounted, watch, computed, onUnmounted } from 'vue'
import axios from 'axios'
import VueFeather from 'vue-feather'

const Card1 = defineAsyncComponent(() => import("@/components/common/card/CardData1.vue"))

interface InactiveSensor {
    station_name: string;
    brand_name: string;
    sensor_type: string;
    lastReading: string | null;
    status: string;
}

const elementsPerPage = ref<number>(5)
const currentPage = ref<number>(1)
const selectedBrand = ref<string>("")
const inactiveSensors = ref<InactiveSensor[]>([])
const isLoading = ref<boolean>(true)

// Fetch inactive sensors data
const fetchInactiveSensors = async () => {
    try {
        isLoading.value = true;
        const response = await axios.get('/measurements/inactive_sensors/');
        
        if (response.data) {
            inactiveSensors.value = response.data.map((sensor: any) => ({
                station_name: sensor.station_name,
                brand_name: sensor.brand_name,
                sensor_type: sensor.sensor_type,
                lastReading: sensor.last_reading,
                status: sensor.status
            }));
        }
    } catch (error) {
        console.error('Error fetching inactive sensor data:', error);
        inactiveSensors.value = [];
    } finally {
        isLoading.value = false;
    }
};

// Check if we have any recent data (within last 24 hours)
const hasRecentData = computed(() => {
    return inactiveSensors.value.some(sensor => {
        if (!sensor.lastReading) return false;
        const lastUpdate = new Date(sensor.lastReading);
        const twentyFourHoursAgo = new Date();
        twentyFourHoursAgo.setHours(twentyFourHoursAgo.getHours() - 24);
        return lastUpdate >= twentyFourHoursAgo;
    });
});

const uniqueBrands = computed(() => {
    const brands = [...new Set(inactiveSensors.value.map(sensor => sensor.brand_name))];
    if (!selectedBrand.value && brands.length > 0) {
        selectedBrand.value = brands[0];
    }
    return brands;
});

const filteredSensors = computed(() => {
    return inactiveSensors.value.filter(sensor => {
        if (!sensor.lastReading) return false;
        const lastUpdate = new Date(sensor.lastReading);
        const twentyFourHoursAgo = new Date();
        twentyFourHoursAgo.setHours(twentyFourHoursAgo.getHours() - 24);
        return lastUpdate >= twentyFourHoursAgo && sensor.brand_name === selectedBrand.value;
    });
});

const totalPages = computed(() => 
    Math.ceil(filteredSensors.value.length / elementsPerPage.value)
);

const paginatedSensors = computed(() => {
    const start = (currentPage.value - 1) * elementsPerPage.value;
    const end = start + elementsPerPage.value;
    return filteredSensors.value.slice(start, end);
});

// Helper functions
const formatDate = (dateString: string | null) => {
    if (!dateString) return 'Never';
    try {
        return new Date(dateString).toLocaleString('en-US', {
            year: 'numeric',
            month: '2-digit',
            day: '2-digit',
            hour: '2-digit',
            minute: '2-digit',
            hour12: true
        });
    } catch {
        return 'Invalid Date';
    }
};

const getStationClass = (sensor: InactiveSensor) => {
    return {
        'bg-light-danger font-danger': sensor.status === 'No Data',
        'bg-light-warning font-warning': sensor.status === 'No Reading',
        'bg-light-error font-error': sensor.status === 'Inactive'
    };
};

// Pagination methods
const next = () => {
    if (currentPage.value < totalPages.value) currentPage.value++;
};

const prev = () => {
    if (currentPage.value > 1) currentPage.value--;
};

// Watch for brand changes
watch(selectedBrand, () => {
    currentPage.value = 1;
});

// Add after onMounted
let refreshInterval: number;

onMounted(() => {
    fetchInactiveSensors();
    // Refresh every 5 minutes
    refreshInterval = window.setInterval(fetchInactiveSensors, 300000);
});

onUnmounted(() => {
    if (refreshInterval) {
        clearInterval(refreshInterval);
    }
});
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

.btn-sm {
    padding: 0.25rem 0.8rem;
    font-size: 0.875rem;
    border-radius: 4px;
}

.table td {
    padding: 1rem 0.5rem;
    vertical-align: middle;
}

.table th {
    padding: 1rem 0.5rem;
    font-weight: 500;
}

.designer-card {
    padding: 1.25rem 0;
}

.empty-state {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 2rem;
}

.empty-state h5 {
    margin-bottom: 0.5rem;
    color: #495057;
}

.empty-state p {
    color: #6c757d;
}
</style>