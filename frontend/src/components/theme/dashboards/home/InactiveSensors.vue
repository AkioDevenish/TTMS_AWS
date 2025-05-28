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
                            <button class="btn btn-sm" :class="getStationClass(sensor)">
                                {{ sensor.status }}
                            </button>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>

        <!-- Pagination -->
        <div class="pagination-scroll-x">
            <ul class="pagination mx-3 mt-3 justify-content-end" v-if="totalPages > 1">
                <li class="page-item" :class="{ disabled: currentPage === 1 || isLoading }">
                    <a class="page-link cursor-pointer" @click="prev()">Previous</a>
                </li>
                <li
                    v-for="page in visiblePages"
                    :key="page"
                    class="page-item"
                    :class="{ active: page === currentPage, disabled: page === '...' }"
                >
                    <a
                        v-if="page !== '...'"
                        class="page-link cursor-pointer"
                        @click="setPage(page as number)"
                    >{{ page }}</a>
                    <span v-else class="page-link">...</span>
                </li>
                <li class="page-item" :class="{ disabled: currentPage === totalPages || isLoading }">
                    <a class="page-link cursor-pointer" @click="next()">Next</a>
                </li>
            </ul>
        </div>
    </Card1>
</template>

<script lang="ts" setup>
import { defineAsyncComponent, onMounted, computed } from 'vue';
import { useInactiveSensorsStore, type InactiveSensor } from '@/store/inactiveSensors';
import VueFeather from 'vue-feather';

const Card1 = defineAsyncComponent(() => import("@/components/common/card/CardData1.vue"));

// Use the store
const store = useInactiveSensorsStore();

// Get state and actions from the store
const isLoading = computed(() => store.isLoading);
const inactiveSensors = computed(() => store.sensors); // This now gets the paginated/filtered sensors from the store
const currentPage = computed(() => store.currentPage);
const totalPages = computed(() => store.totalPages);
const selectedBrand = computed(() => {
    console.log('Component: selectedBrand computed property:', store.selectedBrand);
    return store.selectedBrand;
});
const uniqueBrands = computed(() => {
    console.log('Component: uniqueBrands computed property:', store.availableBrands);
    return store.availableBrands;
});

// Check if we have any data to display (considering the current page)
const hasRecentData = computed(() => {
    console.log('Component: hasRecentData computed property:', inactiveSensors.value && inactiveSensors.value.length > 0);
    return inactiveSensors.value && inactiveSensors.value.length > 0;
});

// Helper functions (keep these as they work with the data structure)
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

// Pagination methods dispatching to store actions
const setPage = (page: number) => {
    store.setPage(page);
};

const next = () => {
    if (currentPage.value < totalPages.value) {
        setPage(currentPage.value + 1); // Use local setPage which calls store action
    }
};

const prev = () => {
    if (currentPage.value > 1) {
        setPage(currentPage.value - 1); // Use local setPage which calls store action
    }
};

// Brand selection method dispatching to store action
const selectBrand = (brand: string) => {
    store.setBrand(brand);
};

// Fetch data on component mount
onMounted(() => {
    // Initial fetch when the component is mounted
    store.fetchInactiveSensors();
    // Note: The store should handle the refresh interval internally if needed.
});

// Note: The component no longer needs the watch on selectedBrand or its own refresh interval.
// These concerns are now managed within the Pinia store.

const visiblePages = computed(() => {
    const pages = [];
    const windowSize = 2; // how many pages before/after current to show
    let start = Math.max(1, currentPage.value - windowSize);
    let end = Math.min(totalPages.value, currentPage.value + windowSize);

    // Always show first page
    if (start > 1) {
        pages.push(1);
        if (start > 2) pages.push('...');
    }

    for (let i = start; i <= end; i++) {
        pages.push(i);
    }

    // Always show last page
    if (end < totalPages.value) {
        if (end < totalPages.value - 1) pages.push('...');
        pages.push(totalPages.value);
    }

    return pages;
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

.pagination-scroll-x {
    overflow-x: auto;
    -webkit-overflow-scrolling: touch;
    width: 100%;
    margin-bottom: 1rem;
}
.pagination {
    min-width: 400px;
    white-space: nowrap;
}
</style>