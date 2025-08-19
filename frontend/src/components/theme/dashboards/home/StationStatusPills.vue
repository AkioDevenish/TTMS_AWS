<template>
    <div class="order-2">
        <Card1
            colClass="col-xl-12 col-md-12 proorder-xl-1 proorder-md-1 mb-30"
            headerTitle="true" 
            title="Station Status Overview"
            cardHeaderClass="card-no-border pb-0"
            cardBodyClass="designer-card"
        >
            <!-- Status Summary Pills -->
            <div class="status-summary mb-4">
                <div class="row g-3">
                    <div class="col-xl-3 col-lg-6 col-md-6">
                        <div class="status-pill online">
                            <div class="status-icon">
                                <VueFeather type="wifi" size="20" />
                            </div>
                            <div class="status-content">
                                <div class="status-number">{{ summary.online }}</div>
                                <div class="status-label">Online</div>
                            </div>
                        </div>
                    </div>
                    <div class="col-xl-3 col-lg-6 col-md-6">
                        <div class="status-pill online-erroneous">
                            <div class="status-icon">
                                <VueFeather type="alert-triangle" size="20" />
                            </div>
                            <div class="status-content">
                                <div class="status-number">{{ summary.online_erroneous }}</div>
                                <div class="status-label">Online Erroneous</div>
                            </div>
                        </div>
                    </div>
                    <div class="col-xl-3 col-lg-6 col-md-6">
                        <div class="status-pill offline">
                            <div class="status-icon">
                                <VueFeather type="wifi-off" size="20" />
                            </div>
                            <div class="status-content">
                                <div class="status-number">{{ summary.offline }}</div>
                                <div class="status-label">Offline</div>
                            </div>
                        </div>
                    </div>
                    <div class="col-xl-3 col-lg-6 col-md-6">
                        <div class="status-pill total">
                            <div class="status-icon">
                                <VueFeather type="activity" size="20" />
                            </div>
                            <div class="status-content">
                                <div class="status-number">{{ summary.total_stations }}</div>
                                <div class="status-label">Total Stations</div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Loading Indicator -->
            <div v-if="isLoading" class="text-center py-4">
                <div class="spinner-border text-primary" role="status">
                    <span class="visually-hidden">Loading...</span>
                </div>
            </div>

            <!-- Station Status Table -->
            <div v-else-if="stations.length > 0" class="table-responsive">
                <table class="table table-hover">
                    <thead>
                        <tr>
                            <th>Station Name</th>
                            <th>Brand</th>
                            <th>Serial Number</th>
                            <th class="text-center">Status</th>
                            <th>Last Update</th>
                            <th>Data Quality</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="station in stations" :key="station.id" class="station-row">
                            <td>
                                <div class="station-info">
                                    <div class="station-name">{{ station.name }}</div>
                                </div>
                            </td>
                            <td>
                                <span class="brand-badge">{{ station.brand }}</span>
                            </td>
                            <td>
                                <span class="serial-number">{{ station.serial_number || 'N/A' }}</span>
                            </td>
                            <td class="text-center">
                                <span :class="getStatusClass(station.status_code)" class="status-badge">
                                    {{ station.overall_status }}
                                </span>
                            </td>
                            <td>
                                <div class="last-update">
                                    {{ formatLastUpdate(station.last_updated) }}
                                </div>
                            </td>
                            <td>
                                <div class="data-quality" v-if="station.data_quality_metrics.total_measurements > 0">
                                    <div class="quality-bar">
                                        <div 
                                            class="quality-fill" 
                                            :style="{ width: (station.data_quality_metrics.valid_measurements / station.data_quality_metrics.total_measurements * 100) + '%' }"
                                        ></div>
                                    </div>
                                    <small class="quality-text">
                                        {{ Math.round((station.data_quality_metrics.valid_measurements / station.data_quality_metrics.total_measurements) * 100) }}% valid
                                    </small>
                                </div>
                                <span v-else class="text-muted">No data</span>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>

            <!-- No Data Message -->
            <div v-else class="text-center py-5">
                <div class="empty-state">
                    <VueFeather type="alert-circle" size="48" class="text-muted mb-3" />
                    <h5>No Stations Found</h5>
                    <p class="text-muted">No station data available at the moment.</p>
                </div>
            </div>

            <!-- Error Message -->
            <div v-if="error" class="alert alert-danger mt-3" role="alert">
                {{ error }}
            </div>
        </Card1>
    </div>
</template>

<script lang="ts" setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { defineAsyncComponent } from 'vue'
import axios from '@/plugins/axios'
import VueFeather from "vue-feather"

// Import Card component
const Card1 = defineAsyncComponent(() => import('@/components/common/card/CardData1.vue'))

interface DataQualityMetrics {
    total_measurements: number
    invalid_measurements: number
    valid_measurements: number
    invalid_percentage: number
}

interface HealthInfo {
    battery_status: string
    connectivity_status: string
    last_health_check: string | null
}

interface Station {
    id: number
    name: string
    brand: string
    serial_number: string
    overall_status: string
    status_code: string
    status_description: string
    status_color: string
    transmission_status: string
    data_quality_status: string
    data_quality_metrics: DataQualityMetrics
    last_updated: string | null
    time_since_last_update: number
    time_until_next_update: number
    progress: number
    health_info: HealthInfo
}

interface StatusSummary {
    total_stations: number
    online: number
    offline: number
    online_erroneous: number
}

const stations = ref<Station[]>([])
const summary = ref<StatusSummary>({
    total_stations: 0,
    online: 0,
    offline: 0,
    online_erroneous: 0
})
const isLoading = ref(false)
const error = ref('')
let refreshIntervalId: number | null = null

const fetchStationStatus = async () => {
    try {
        isLoading.value = true
        error.value = ''
        
        const response = await axios.get('/api/stations/comprehensive-status/')
        stations.value = response.data.stations
        summary.value = response.data.summary
    } catch (err: any) {
        console.error('Error fetching station status:', err)
        error.value = err.response?.data?.error || 'Failed to fetch station status'
    } finally {
        isLoading.value = false
    }
}

const getStatusClass = (statusCode: string): string => {
    const statusMap: { [key: string]: string } = {
        'online': 'status-online',
        'offline': 'status-offline',
        'online_erroneous': 'status-online-erroneous',
        'default': 'status-default'
    }
    return statusMap[statusCode] || statusMap['default']
}

const formatLastUpdate = (timestamp: string | null): string => {
    if (!timestamp) return 'No Recent Updates'
    
    try {
        const date = new Date(timestamp)
        const now = new Date()
        const diffMs = now.getTime() - date.getTime()
        const diffMins = Math.floor(diffMs / (1000 * 60))
        const diffHours = Math.floor(diffMs / (1000 * 60 * 60))
        const diffDays = Math.floor(diffMs / (1000 * 60 * 60 * 24))
        
        if (diffMins < 60) {
            return `${diffMins} min ago`
        } else if (diffHours < 24) {
            return `${diffHours} hours ago`
        } else if (diffDays < 7) {
            return `${diffDays} days ago`
        } else {
            return date.toLocaleDateString()
        }
    } catch {
        return 'Date Unavailable'
    }
}

onMounted(() => {
    fetchStationStatus()
    
    // Set up refresh interval (every 5 minutes)
    refreshIntervalId = window.setInterval(() => {
        fetchStationStatus()
    }, 5 * 60 * 1000)
})

onUnmounted(() => {
    if (refreshIntervalId) {
        clearInterval(refreshIntervalId)
        refreshIntervalId = null
    }
})
</script>

<style scoped>
.status-summary {
    margin-bottom: 2rem;
}

.status-pill {
    display: flex;
    align-items: center;
    padding: 1.5rem;
    border-radius: 12px;
    background: white;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    transition: all 0.3s ease;
    height: 100%;
}

.status-pill:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
}

.status-icon {
    margin-right: 1rem;
    padding: 0.75rem;
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
}

.status-content {
    flex: 1;
}

.status-number {
    font-size: 2rem;
    font-weight: 700;
    line-height: 1;
    margin-bottom: 0.25rem;
}

.status-label {
    font-size: 0.875rem;
    font-weight: 500;
    opacity: 0.8;
}

/* Status Pill Colors */
.status-pill.online {
    border-left: 4px solid #28a745;
}

.status-pill.online .status-icon {
    background-color: rgba(40, 167, 69, 0.1);
    color: #28a745;
}

.status-pill.online .status-number {
    color: #28a745;
}

.status-pill.online-erroneous {
    border-left: 4px solid #ffc107;
}

.status-pill.online-erroneous .status-icon {
    background-color: rgba(255, 193, 7, 0.1);
    color: #ffc107;
}

.status-pill.online-erroneous .status-number {
    color: #ffc107;
}

.status-pill.offline {
    border-left: 4px solid #dc3545;
}

.status-pill.offline .status-icon {
    background-color: rgba(220, 53, 69, 0.1);
    color: #dc3545;
}

.status-pill.offline .status-number {
    color: #dc3545;
}

.status-pill.total {
    border-left: 4px solid #6c757d;
}

.status-pill.total .status-icon {
    background-color: rgba(108, 117, 125, 0.1);
    color: #6c757d;
}

.status-pill.total .status-number {
    color: #6c757d;
}

/* Table Styles */
.station-row {
    transition: background-color 0.2s ease;
}

.station-row:hover {
    background-color: #f8f9fa;
}

.station-name {
    font-weight: 600;
    color: #333;
}

.brand-badge {
    display: inline-block;
    padding: 0.25rem 0.5rem;
    background-color: #e9ecef;
    color: #495057;
    border-radius: 4px;
    font-size: 0.75rem;
    font-weight: 500;
}

.serial-number {
    font-family: monospace;
    font-size: 0.875rem;
    color: #6c757d;
}

.status-badge {
    display: inline-block;
    padding: 0.375rem 0.75rem;
    border-radius: 20px;
    font-size: 0.75rem;
    font-weight: 500;
    text-align: center;
    min-width: 100px;
    border: 1px solid transparent;
    transition: all 0.2s ease;
}

.status-online {
    background-color: #d4edda;
    color: #155724;
    border-color: #c3e6cb;
}

.status-offline {
    background-color: #f8d7da;
    color: #721c24;
    border-color: #f5c6cb;
}

.status-online-erroneous {
    background-color: #fff3cd;
    color: #856404;
    border-color: #ffeaa7;
}

.status-default {
    background-color: #e2e3e5;
    color: #383d41;
    border-color: #d6d8db;
}

.last-update {
    font-size: 0.875rem;
    color: #6c757d;
}

.data-quality {
    width: 100%;
}

.quality-bar {
    width: 100%;
    height: 6px;
    background-color: #e9ecef;
    border-radius: 3px;
    overflow: hidden;
    margin-bottom: 0.25rem;
}

.quality-fill {
    height: 100%;
    background: linear-gradient(90deg, #28a745 0%, #20c997 100%);
    transition: width 0.3s ease;
}

.quality-text {
    font-size: 0.75rem;
    color: #6c757d;
}

.empty-state {
    padding: 2rem;
    text-align: center;
}

.empty-state h5 {
    margin-bottom: 0.5rem;
}

/* Dark Mode Styles for Status Badges */
body.dark-only .status-badge {
    border-color: #3a3b46 !important;
}

body.dark-only .status-online {
    background-color: #1e4d2b !important;
    color: #d4edda !important;
    border-color: #2d5a3a !important;
}

body.dark-only .status-offline {
    background-color: #4d1e1e !important;
    color: #f8d7da !important;
    border-color: #5a2d2d !important;
}

body.dark-only .status-online-erroneous {
    background-color: #4d3e1e !important;
    color: #fff3cd !important;
    border-color: #5a4d2d !important;
}

body.dark-only .status-default {
    background-color: #3a3b46 !important;
    color: #e2e3e5 !important;
    border-color: #4a4b56 !important;
}

body.dark-only .serial-number {
    color: rgba(255, 255, 255, 0.7) !important;
}

body.dark-only .last-update {
    color: rgba(255, 255, 255, 0.7) !important;
}

body.dark-only .quality-text {
    color: rgba(255, 255, 255, 0.7) !important;
}

/* Additional dark mode class support */
:deep(.dark-mode) .status-badge {
    border-color: #3a3b46 !important;
}

:deep(.dark-mode) .status-online {
    background-color: #1e4d2b !important;
    color: #d4edda !important;
    border-color: #2d5a3a !important;
}

:deep(.dark-mode) .status-offline {
    background-color: #4d1e1e !important;
    color: #f8d7da !important;
    border-color: #5a2d2d !important;
}

:deep(.dark-mode) .status-online-erroneous {
    background-color: #4d3e1e !important;
    color: #fff3cd !important;
    border-color: #5a4d2d !important;
}

:deep(.dark-mode) .status-default {
    background-color: #3a3b46 !important;
    color: #e2e3e5 !important;
    border-color: #4a4b56 !important;
}

:deep(.dark-mode) .serial-number {
    color: rgba(255, 255, 255, 0.7) !important;
}

:deep(.dark-mode) .last-update {
    color: rgba(255, 255, 255, 0.7) !important;
}

:deep(.dark-mode) .quality-text {
    color: rgba(255, 255, 255, 0.7) !important;
}

/* Responsive adjustments */
@media (max-width: 768px) {
    .status-pill {
        padding: 1rem;
    }
    
    .status-number {
        font-size: 1.5rem;
    }
    
    .table-responsive {
        font-size: 0.875rem;
    }
}
</style> 