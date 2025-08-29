<template>
    <Card1 colClass="col-xl-12 col-lg-12 col-md-12 order-1" 
        headerTitle="true" 
        title="Inactive Sensors"
        cardhaderClass="card-no-border pb-0" 
        cardbodyClass="designer-card">
        
        <!-- Brand Tabs -->
        <ul class="nav nav-tabs border-tab nav-primary mb-4" role="tablist">
            <li class="nav-item" v-for="brand in uniqueBrands" :key="brand">
                <a class="nav-link" :class="{ active: selectedBrand === brand }" 
                   @click="selectBrand(brand)">
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
                <p class="text-muted">No inactive sensors found for the selected criteria.</p>
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
                    <tr v-for="(sensor, index) in inactiveSensors" :key="index">
                        <td class="px-3">
                            <div class="d-flex align-items-center">
                                <h6 class="mb-0">{{ sensor.station_name }}</h6>
                            </div>
                        </td>
                        <td>{{ sensor.sensor_type }}</td>
                        <td>{{ formatDate(sensor.lastReading) }}</td>
                        <td>
                            <span class="badge rounded-pill" :class="getStatusClass(sensor.status)">
                                {{ sensor.status || 'No Status' }}
                            </span>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>

        <!-- Pagination Controls -->
        <div class="pagination-container">
            <!-- Page Size Selector -->
            <div class="page-size-selector">
                <label class="page-size-label">Show:</label>
                <select 
                    v-model="selectedPageSize" 
                    @change="changePageSize"
                    class="page-size-select"
                >
                    <option value="5">5</option>
                    <option value="10">10</option>
                    <option value="20">20</option>
                    <option value="50">50</option>
                </select>
                <span class="page-size-text">of {{ paginationInfo.totalSensors }} sensors</span>
            </div>

            <!-- Pagination Navigation -->
            <nav class="pagination-nav" aria-label="Sensor pagination">
                <ul class="pagination-list">
                    <!-- Previous Page -->
                    <li class="pagination-item">
                        <button 
                            class="pagination-button prev-button" 
                            @click="previousPage"
                            :disabled="!paginationInfo.hasPrevious"
                            :class="{ disabled: !paginationInfo.hasPrevious }"
                        >
                            ←
                        </button>
                    </li>

                    <!-- Page Numbers -->
                    <li 
                        v-for="page in pageRange" 
                        :key="page" 
                        class="pagination-item"
                    >
                        <button 
                            class="pagination-button page-button"
                            :class="{ active: page === paginationInfo.currentPage }"
                            @click="goToPage(page)"
                        >
                            {{ page }}
                        </button>
                    </li>

                    <!-- Next Page -->
                    <li class="pagination-item">
                        <button 
                            class="pagination-button next-button" 
                            @click="nextPage"
                            :disabled="!paginationInfo.hasNext"
                            :class="{ disabled: !paginationInfo.hasNext }"
                        >
                            →
                        </button>
                    </li>
                </ul>
            </nav>
        </div>
    </Card1>
</template>

<script lang="ts" setup>
import { defineAsyncComponent, onMounted, computed, ref, watch } from 'vue';
import { useInactiveSensorsStore, type InactiveSensor } from '@/store/inactiveSensors';
import VueFeather from 'vue-feather';

const Card1 = defineAsyncComponent(() => import("@/components/common/card/CardData1.vue"));

// Use the store
const store = useInactiveSensorsStore();

// Component state
const selectedPageSize = computed({
    get: () => store.pageSize,
    set: (value: number) => {
        store.pageSize = value;
    }
});

// Computed properties
const isLoading = computed(() => store.isLoading);
const inactiveSensors = computed(() => store.sensors);
const selectedBrand = computed(() => store.selectedBrand);
const uniqueBrands = computed(() => store.availableBrands);
const hasRecentData = computed(() => store.hasRecentData);
const paginationInfo = computed(() => store.getPaginationInfo);
const pageRange = computed(() => store.getPageRange);

// Helper functions (keep these as they work with the data structure)
const formatDate = (dateString: string | null) => {
    if (!dateString) return 'No Reading';
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

const getStatusClass = (status: string) => {
    switch (status) {
        case 'No Reading':
            return 'bg-light-warning font-warning';
        case 'No Data':
            return 'bg-light-secondary font-secondary';
        default:
            return 'bg-light text-dark';
    }
};

// Actions
const selectBrand = (brand: string) => {
    store.setBrand(brand);
};

// Pagination methods
const goToPage = async (page: number) => {
    await store.goToPage(page);
};

const nextPage = async () => {
    await store.nextPage();
};

const previousPage = async () => {
    await store.previousPage();
};

const changePageSize = async () => {
    await store.changePageSize(selectedPageSize.value);
};

// Lifecycle
onMounted(() => {
    store.fetchInactiveSensors();
});

// Watch for changes in selected brand and refresh data
watch(() => selectedBrand.value, (newBrand) => {
    if (newBrand) {
        console.log('Brand changed to:', newBrand, 'refreshing data...');
        store.fetchInactiveSensors(true);
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

/* Status Badge Styles */
.badge.rounded-pill {
    font-size: 0.75rem;
    font-weight: 500;
    padding: 0.5rem 0.75rem;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    border-radius: 50px;
}

/* Pagination Styles */
.pagination-container {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: 2rem;
    padding: 1.5rem;
    background: #f8f9fa;
    border-radius: 12px;
    border: 1px solid #e9ecef;
    width: 100%;
    box-sizing: border-box;
}



.page-size-selector {
    display: flex;
    align-items: center;
    gap: 0.75rem;
}

.page-size-label {
    color: #6c757d;
    font-size: 0.875rem;
    font-weight: 500;
    margin: 0;
}

.page-size-select {
    padding: 0.5rem 0.75rem;
    border: 1px solid #dee2e6;
    border-radius: 8px;
    background: white;
    color: #495057;
    font-size: 0.875rem;
    min-width: 80px;
    cursor: pointer;
    transition: all 0.2s ease;
}

.page-size-select:focus {
    outline: none;
    border-color: #7A70BA;
    box-shadow: 0 0 0 3px rgba(122, 112, 186, 0.1);
}

.page-size-text {
    color: #6c757d;
    font-size: 0.875rem;
    font-weight: 500;
}

.pagination-nav {
    display: flex;
    align-items: center;
}

.pagination-list {
    display: flex;
    list-style: none;
    margin: 0;
    padding: 0;
    gap: 0.5rem;
    align-items: center;
}

.pagination-item {
    margin: 0;
}

.pagination-button {
    display: flex;
    align-items: center;
    justify-content: center;
    min-width: 40px;
    height: 40px;
    padding: 0.5rem;
    border: 1px solid #dee2e6;
    border-radius: 8px;
    background: white;
    color: #6c757d;
    font-size: 0.875rem;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s ease;
    text-decoration: none;
    line-height: 1;
}

.pagination-button:hover:not(.disabled) {
    background: #f8f9fa;
    border-color: #7A70BA;
    color: #7A70BA;
    transform: translateY(-1px);
    box-shadow: 0 2px 8px rgba(122, 112, 186, 0.15);
}

.pagination-button:active:not(.disabled) {
    transform: translateY(0);
    box-shadow: 0 1px 4px rgba(122, 112, 186, 0.15);
}

.pagination-button.active {
    background: #7A70BA;
    border-color: #7A70BA;
    color: white;
    box-shadow: 0 2px 8px rgba(122, 112, 186, 0.25);
}

.pagination-button.active:hover {
    background: #6a5faa;
    border-color: #6a5faa;
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(122, 112, 186, 0.3);
}

.pagination-button.disabled,
.pagination-button:disabled {
    background: #f8f9fa;
    border-color: #e9ecef;
    color: #adb5bd;
    cursor: not-allowed;
    transform: none;
    box-shadow: none;
}

.pagination-button.disabled:hover,
.pagination-button:disabled:hover {
    background: #f8f9fa;
    border-color: #e9ecef;
    color: #adb5bd;
    transform: none;
    box-shadow: none;
}

.prev-button,
.next-button {
    min-width: 40px;
}

.page-button {
    min-width: 40px;
}

/* Dark Mode Styles */
body.dark-only .pagination-container {
    background: #2a2b36 !important;
    border-color: #3a3b46 !important;
}

body.dark-only .page-size-label {
    color: rgba(255, 255, 255, 0.7) !important;
}

body.dark-only .page-size-text {
    color: rgba(255, 255, 255, 0.7) !important;
}

body.dark-only .page-size-select {
    background: #1d1e26 !important;
    border-color: #3a3b46 !important;
    color: rgba(255, 255, 255, 0.8) !important;
}

body.dark-only .page-size-select:focus {
    border-color: #7A70BA !important;
    box-shadow: 0 0 0 3px rgba(122, 112, 186, 0.2) !important;
}

body.dark-only .pagination-button {
    background: #1d1e26 !important;
    border-color: #3a3b46 !important;
    color: rgba(255, 255, 255, 0.8) !important;
}

body.dark-only .pagination-button:hover:not(.disabled) {
    background: #374462 !important;
    border-color: #7A70BA !important;
    color: #7A70BA !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 2px 8px rgba(122, 112, 186, 0.25) !important;
}

body.dark-only .pagination-button.active {
    background: #7A70BA !important;
    border-color: #7A70BA !important;
    color: white !important;
    box-shadow: 0 2px 8px rgba(122, 112, 186, 0.25) !important;
}

body.dark-only .pagination-button.active:hover {
    background: #6a5faa !important;
    border-color: #6a5faa !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 12px rgba(122, 112, 186, 0.3) !important;
}

body.dark-only .pagination-button.disabled,
body.dark-only .pagination-button:disabled {
    background: #1d1e26 !important;
    border-color: #3a3b46 !important;
    color: rgba(255, 255, 255, 0.4) !important;
    transform: none !important;
    box-shadow: none !important;
}

body.dark-only .pagination-button.disabled:hover,
body.dark-only .pagination-button:disabled:hover {
    background: #1d1e26 !important;
    border-color: #3a3b46 !important;
    color: rgba(255, 255, 255, 0.4) !important;
    transform: none !important;
    box-shadow: none !important;
}
</style>