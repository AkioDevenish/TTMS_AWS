<template>
    <Card1 colClass="col-xl-12 col-lg-12 col-md-12 order-1" 
        headerTitle="true" 
        title="Station Health Status"
        cardhaderClass="card-no-border pb-0" 
        cardbodyClass="designer-card">
        
        <!-- Brand Tabs -->
        <ul class="nav nav-tabs border-tab nav-primary mb-4" role="tablist">
            <li class="nav-item" v-for="brand in availableBrands" :key="brand">
                <a class="nav-link" :class="{ active: selectedBrand === brand }" 
                   @click="selectBrand(brand)">
                    {{ brand }}
                </a>
            </li>
        </ul>

        <!-- Loading State -->
        <div v-if="isLoading" class="loading-state">
            <div class="spinner-border text-primary spinning" role="status">
                <span class="visually-hidden">Loading...</span>
            </div>
            <h5 class="mt-3">Loading Station Health Data...</h5>
        </div>

        <!-- Error State -->
        <div v-else-if="error" class="error-state">
            <VueFeather type="alert-triangle" size="48" class="text-danger mb-3" />
            <h5>Error Loading Data</h5>
            <p>{{ error }}</p>
            <button class="btn btn-primary" @click="refreshData">Retry</button>
        </div>

        <!-- No Data State -->
        <div v-else-if="!hasRecentData" class="empty-state">
            <VueFeather type="alert-circle" size="48" class="text-muted mb-3" />
            <h5>No Data Available</h5>
            <p class="text-muted">No station health data found for the selected criteria.</p>
        </div>

        <!-- Data Display State -->
        <div v-else class="card-body">
            <!-- Stations Table -->
            <div class="table-responsive theme-scrollbar">
                <table class="table table-hover">
                    <thead>
                        <tr>
                            <th>Station Name</th>
                            <th>Status</th>
                            <th>Battery</th>
                            <th>Last Update</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="station in filteredStations" :key="station.id">
                            <td>{{ station.name }}</td>
                            <td>
                                <span class="status-badge badge rounded-pill" :class="getStatusClass(station.status)">
                                    {{ station.status }}
                                </span>
                            </td>
                            <td>
                                <span class="status-badge badge rounded-pill" :class="getBatteryClass(station.battery_status)">
                                    {{ station.battery_status || 'Unknown' }}
                                </span>
                            </td>
                            <td>{{ formatDate(station.created_at) }}</td>
                        </tr>
                    </tbody>
                </table>
            </div>

            <!-- Debug Panel (Development Only) -->
            <div v-if="showDebug" class="mt-4 p-3 bg-light rounded">
                <h6>Debug Information</h6>
                <div class="row">
                    <div class="col-md-3">
                        <strong>Total Stations:</strong> {{ store.stationHealth.length }}
                    </div>
                    <div class="col-md-3">
                        <strong>Health Records:</strong> {{ store.stationHealth.length }}
                    </div>
                    <div class="col-md-3">
                        <strong>Loading:</strong> {{ store.isLoading }}
                    </div>
                    <div class="col-md-3">
                        <strong>Error:</strong> {{ store.error || 'None' }}
                    </div>
                </div>
                <div class="mt-2">
                    <button class="btn btn-sm btn-secondary me-2" @click="refreshData">Refresh Data</button>
                    <button class="btn btn-sm btn-info" @click="testAPI">Test API</button>
                </div>
            </div>
        </div>
    </Card1>
</template>

<script lang="ts" setup>
import { defineAsyncComponent, onMounted, onUnmounted, computed, ref } from 'vue';
import { useAWSStationsStore, type StationHealth } from '@/store/awsStations';
import VueFeather from 'vue-feather';

const Card1 = defineAsyncComponent(() => import("@/components/common/card/CardData1.vue"));

// Use the store
const store = useAWSStationsStore();

// Component state
const showDebug = ref(false); // Set to true for development

// Computed properties
const isLoading = computed(() => store.isLoading);
const error = computed(() => store.error);
const hasRecentData = computed(() => store.hasRecentData);
const status = computed(() => store.getStationStatus);
const availableBrands = computed(() => store.availableBrands);
const selectedBrand = computed(() => store.selectedBrand);

const filteredStations = computed(() => {
    if (selectedBrand.value) {
        return store.getStationsByBrand(selectedBrand.value);
    }
    // Default to first brand if none selected
    return store.getStationsByBrand(store.availableBrands[0]);
});

// Helper functions
const getStatusClass = (status: string) => {
    switch (status?.toLowerCase()) {
        case 'online':
            return 'badge bg-light-success';
        case 'critical battery':
            return 'badge bg-light-danger';
        case 'low battery':
            return 'badge bg-light-warning';
        case 'battery warning':
            return 'badge bg-light-warning';
        case 'warning':
            return 'badge bg-light-warning';
        case 'offline':
            return 'badge bg-light-danger';
        case 'online erroneous data':
            // For battery sensors, this might be incorrect - check if it's a battery sensor
            return 'badge bg-light-warning';
        default:
            return 'badge bg-light-warning';
    }
};

const getBatteryClass = (batteryStatus: string) => {
    switch (batteryStatus?.toLowerCase()) {
        case 'excellent':
        case 'good':
            return 'status-active badge-success';
        case 'fair':
            return 'status-unknown badge-warning';
        case 'poor':
        case 'critical':
            return 'status-inactive badge-danger';
        default:
            return 'status-unknown badge-secondary';
    }
};

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

// Actions
const refreshData = async () => {
    const brandToUse = selectedBrand.value || store.availableBrands[0];
    await store.fetchStationHealth(brandToUse);
};

const selectBrand = (brand: string | null) => {
    store.setBrand(brand);
};

const testAPI = async () => {
    await store.testAPI();
};

// Lifecycle
onMounted(async () => {
    console.log('Station Health component mounted');
    
    try {
        await store.init();
        console.log('Store initialized');
        
        // Set default brand to first available brand
        if (store.availableBrands.length > 0 && !selectedBrand.value) {
            store.setBrand(store.availableBrands[0]);
        }
    } catch (err) {
        console.error('Error initializing:', err);
    }
});

onUnmounted(() => {
    store.cleanup();
});
</script>

<style scoped>
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

.progress-striped-primary {
    height: 8px;
    background-color: rgba(var(--bs-primary-rgb), 0.1);
    border-radius: 4px;
}

.progress-bar {
    background-color: var(--bs-primary);
    border-radius: 4px;
    transition: width 0.6s ease;
}

.loading-state {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 2rem;
}

.loading-state h5 {
    margin-bottom: 0.5rem;
    color: #495057;
}

.spinning {
    animation: spin 1s linear infinite;
}

@keyframes spin {
    from { transform: rotate(0deg); }
    to { transform: rotate(360deg); }
}

.error-state {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 2rem;
}

.error-state h5 {
    margin-bottom: 0.5rem;
    color: #dc3545;
}

.error-state p {
    color: #6c757d;
}
</style>