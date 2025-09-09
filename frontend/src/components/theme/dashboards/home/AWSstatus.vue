<template>
  <Card1
      colClass="col-xl-12 col-lg-12 col-md-12 order-1"
      headerTitle="true"
      title="Station Health"
      cardClass="slim-complex"
      cardhaderClass="card-no-border pb-0"
      cardbodyClass="designer-card">

    <!-- Brand Tabs -->
    <ul class="nav nav-tabs border-tab nav-primary mb-0" role="tablist">
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
    <div v-else>
      <!-- Stations Table -->
      <div class="table-responsive theme-scrollbar">
        <table class="table table-hover">
          <thead>
            <tr>
              <th>Station Name</th>
              <th>Last Update</th>
              <th>Battery</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="station in filteredStations" :key="station.id">
              <td>{{ station.name }}</td>
              <td>{{ formatDate(station.created_at) }}</td>
              <td>
                <span class="status-badge" :class="getBatteryClass(station.battery_status)">
                  {{ station.battery_status || 'Unknown' }}
                </span>
              </td>
              <td>
                <span class="status-badge" :class="getStatusClass(station.status)">
                  {{ station.status }}
                </span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Pagination Controls -->
      <div v-if="paginationInfo.totalPages > 1" class="pagination-wrapper">
        <div class="pagination-container">
          <!-- Page Size Selector -->
          <div class="page-size-selector">
            <label class="page-size-label">Show:</label>
            <select
                v-model="selectedPageSize"
                @change="changePageSize"
                class="page-size-select">
              <option value="10">10</option>
              <option value="20">20</option>
              <option value="50">50</option>
              <option value="100">100</option>
            </select>
            <span class="page-size-text">of {{ paginationInfo.totalStations }} stations</span>
          </div>

          <!-- Pagination Navigation -->
          <nav class="pagination-nav" aria-label="Station pagination">
            <ul class="pagination-list">
              <!-- Previous Page -->
              <li class="pagination-item">
                <button
                    class="pagination-button prev-button"
                    @click="previousPage"
                    :disabled="!paginationInfo.hasPrevious"
                    :class="{ disabled: !paginationInfo.hasPrevious }">←
                </button>
              </li>

              <!-- Page Numbers -->
              <li
                  v-for="page in pageRange"
                  :key="page"
                  class="pagination-item">
                <button
                    class="pagination-button page-button"
                    :class="{ active: page === paginationInfo.currentPage }"
                    @click="goToPage(page)">
                  {{ page }}
                </button>
              </li>

              <!-- Next Page -->
              <li class="pagination-item">
                <button
                    class="pagination-button next-button"
                    @click="nextPage"
                    :disabled="!paginationInfo.hasNext"
                    :class="{ disabled: !paginationInfo.hasNext }">
                  →
                </button>
              </li>
            </ul>
          </nav>
        </div>
      </div>

      <!-- Debug Panel (Development Only) -->
      <div v-if="showDebug" class="mt-4 p-3 bg-light rounded">
        <h6>Debug Information</h6>
        <div class="row">
          <div class="col-md-3">
            <strong>Total Stations:</strong> {{ paginationInfo.totalStations }}
          </div>
          <div class="col-md-3">
            <strong>Current Page:</strong> {{ paginationInfo.currentPage }} of {{ paginationInfo.totalPages }}
          </div>
          <div class="col-md-3">
            <strong>Page Size:</strong> {{ paginationInfo.pageSize }}
          </div>
          <div class="col-md-3">
            <strong>Loading:</strong> {{ store.isLoading }}
          </div>
        </div>
        <div class="row mt-2">
          <div class="col-md-3">
            <strong>Has Next:</strong> {{ paginationInfo.hasNext }}
          </div>
          <div class="col-md-3">
            <strong>Has Previous:</strong> {{ paginationInfo.hasPrevious }}
          </div>
          <div class="col-md-3">
            <strong>Error:</strong> {{ store.error || 'None' }}
          </div>
          <div class="col-md-3">
            <strong>Health Records:</strong> {{ store.stationHealth.length }}
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
import { defineAsyncComponent, onMounted, onUnmounted, computed, ref, watch } from 'vue';
import { useAWSStationsStore, type StationHealth } from '@/store/awsStations';
import VueFeather from 'vue-feather';

const Card1 = defineAsyncComponent(() => import('@/components/common/card/CardData1.vue'));

// Use the store
const store = useAWSStationsStore();

// Component state
const showDebug = ref(false); // Set to true for development
const selectedPageSize = ref(50); // Default page size (increased to show all stations)

// Computed properties
const isLoading = computed(() => store.isLoading);
const error = computed(() => store.error);
const hasRecentData = computed(() => store.hasRecentData);
const status = computed(() => store.getStationStatus);
const availableBrands = computed(() => store.availableBrands);
const selectedBrand = computed(() => store.selectedBrand);
const paginationInfo = computed(() => store.getPaginationInfo);
const pageRange = computed(() => store.getPageRange);

const filteredStations = computed(() => {
  // The store already fetches data for the selected brand, so just return the store data
  console.log('filteredStations computed - store data:', store.stationHealth);
  console.log('filteredStations computed - selected brand:', selectedBrand.value);
  console.log('filteredStations computed - available brands:', store.availableBrands);
  return store.stationHealth;
});

// Helper functions
const getStatusClass = (status: string) => {
  switch (status?.toLowerCase()) {
    case 'online':
    case 'connected':
      return 'status-active';
    case 'critical battery':
      return 'status-inactive';
    case 'low battery':
      return 'status-pending';
    case 'battery warning':
      return 'status-pending';
    case 'warning':
      return 'status-pending';
    case 'offline':
      return 'status-inactive';
    case 'online erroneous data':
      return 'status-pending';
    default:
      return 'status-default';
  }
};

const getBatteryClass = (batteryStatus: string) => {
  switch (batteryStatus?.toLowerCase()) {
    case 'excellent':
    case 'good':
      return 'status-active';
    case 'fair':
      return 'status-pending';
    case 'poor':
    case 'critical':
      return 'status-inactive';
    default:
      return 'status-default';
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
  await store.fetchStationHealth(brandToUse, paginationInfo.value.currentPage, paginationInfo.value.pageSize);
};

const selectBrand = (brand: string | null) => {
  console.log('selectBrand called with:', brand);
  store.setBrand(brand);
};

const testAPI = async () => {
  await store.testAPI();
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
onMounted(async () => {
  console.log('Station Health component mounted');

  try {
    await store.init();
    console.log('Store initialized');

    // The store.init() already sets the default brand, no need to set it again

    // Sync selected page size with store
    selectedPageSize.value = store.pageSize;
  } catch (err) {
    console.error('Error initializing:', err);
  }
});

onUnmounted(() => {
  store.cleanup();
});

// Watch for changes in store page size and sync with local state
watch(() => store.pageSize, (newPageSize) => {
  selectedPageSize.value = newPageSize;
});

// Watch for changes in selected brand and refresh data
watch(() => selectedBrand.value, (newBrand, oldBrand) => {
  console.log('Brand watch triggered:', { oldBrand, newBrand });
  if (newBrand && newBrand !== oldBrand) {
    console.log('Brand changed to:', newBrand, 'refreshing data...');
    refreshData();
  }
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
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
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

/* Status Badge Styles - matching Recent Users component */
.status-badge {
  display: inline-block;
  padding: 0.375rem 0.75rem;
  border-radius: 20px;
  font-size: 0.75rem;
  font-weight: 500;
  text-align: center;
  min-width: 80px;
  border: 1px solid transparent;
  transition: all 0.2s ease;
}

.status-active {
  background-color: #d4edda;
  color: #155724;
  border-color: #c3e6cb;
}

.status-inactive {
  background-color: #f8d7da;
  color: #721c24;
  border-color: #f5c6cb;
}

.status-pending {
  background-color: #fff3cd;
  color: #856404;
  border-color: #ffeaa7;
}

.status-default {
  background-color: #e2e3e5;
  color: #383d41;
  border-color: #d6d8db;
}

/* Dark Mode Styles for Status Badges */
body.dark-only .status-badge {
  border-color: #3a3b46 !important;
}

body.dark-only .status-active {
  background-color: #1e4d2b !important;
  color: #d4edda !important;
  border-color: #2d5a3a !important;
}

body.dark-only .status-inactive {
  background-color: #4d1e1e !important;
  color: #f8d7da !important;
  border-color: #5a2d2d !important;
}

body.dark-only .status-pending {
  background-color: #4d3e1e !important;
  color: #fff3cd !important;
  border-color: #5a4d2d !important;
}

body.dark-only .status-default {
  background-color: #3a3b46 !important;
  color: #e2e3e5 !important;
  border-color: #4a4b56 !important;
}

/* Additional dark mode class support for status badges */
:deep(.dark-mode) .status-badge {
  border-color: #3a3b46 !important;
}

:deep(.dark-mode) .status-active {
  background-color: #1e4d2b !important;
  color: #d4edda !important;
  border-color: #2d5a3a !important;
}

:deep(.dark-mode) .status-inactive {
  background-color: #4d1e1e !important;
  color: #f8d7da !important;
  border-color: #5a2d2d !important;
}

:deep(.dark-mode) .status-pending {
  background-color: #4d3e1e !important;
  color: #fff3cd !important;
  border-color: #5a4d2d !important;
}

:deep(.dark-mode) .status-default {
  background-color: #3a3b46 !important;
  color: #e2e3e5 !important;
  border-color: #4a4b56 !important;
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

/* Additional dark mode class support */
:deep(.dark-mode) .pagination-container {
  background: #2a2b36 !important;
  border-color: #3a3b46 !important;
}

:deep(.dark-mode) .page-size-label {
  color: rgba(255, 255, 255, 0.7) !important;
}

:deep(.dark-mode) .page-size-text {
  color: rgba(255, 255, 255, 0.7) !important;
}

:deep(.dark-mode) .page-size-select {
  background: #1d1e26 !important;
  border-color: #3a3b46 !important;
  color: rgba(255, 255, 255, 0.8) !important;
}

:deep(.dark-mode) .pagination-button {
  background: #1d1e26 !important;
  border-color: #3a3b46 !important;
  color: rgba(255, 255, 255, 0.8) !important;
}

:deep(.dark-mode) .pagination-button:hover:not(.disabled) {
  background: #374462 !important;
  border-color: #7A70BA !important;
  color: #7A70BA !important;
  transform: translateY(-1px) !important;
  box-shadow: 0 2px 8px rgba(122, 112, 186, 0.25) !important;
}

:deep(.dark-mode) .pagination-button.active {
  background: #7A70BA !important;
  border-color: #7A70BA !important;
  color: white !important;
  box-shadow: 0 2px 8px rgba(122, 112, 186, 0.25) !important;
}

:deep(.dark-mode) .pagination-button.active:hover {
  background: #6a5faa !important;
  border-color: #6a5faa !important;
  transform: translateY(-1px) !important;
  box-shadow: 0 4px 12px rgba(122, 112, 186, 0.3) !important;
}

:deep(.dark-mode) .pagination-button.disabled,
:deep(.dark-mode) .pagination-button:disabled {
  background: #1d1e26 !important;
  border-color: #3a3b46 !important;
  color: rgba(255, 255, 255, 0.4) !important;
  transform: none !important;
  box-shadow: none !important;
}

:deep(.dark-mode) .pagination-button.disabled:hover,
:deep(.dark-mode) .pagination-button:disabled:hover {
  background: #1d1e26 !important;
  border-color: #3a3b46 !important;
  color: rgba(255, 255, 255, 0.4) !important;
  transform: none !important;
  box-shadow: none !important;
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .pagination-container {
    flex-direction: column;
    gap: 1rem;
    align-items: stretch;
  }

  .page-size-selector {
    justify-content: center;
  }

  .pagination-nav {
    justify-content: center;
  }

  .pagination-list {
    gap: 0.25rem;
  }

  .pagination-button {
    min-width: 36px;
    height: 36px;
    font-size: 0.8rem;
  }
}
</style>
