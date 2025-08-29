<template>
  <div class="station-status-overview">
    <!-- Header with summary -->
    <div class="status-header mb-4">
      <h4 class="mb-3">Station Status Overview</h4>
      <div class="status-summary d-flex gap-3">
        <div class="status-summary-item">
          <div class="status-indicator online"></div>
          <span class="status-label">Online: {{ summary.online }}</span>
        </div>
        <div class="status-summary-item">
          <div class="status-indicator online-erroneous"></div>
          <span class="status-label">Online Erroneous: {{ summary.online_erroneous }}</span>
        </div>
        <div class="status-summary-item">
          <div class="status-indicator offline"></div>
          <span class="status-label">Offline: {{ summary.offline }}</span>
        </div>
        <div class="status-summary-item">
          <span class="status-label">Total: {{ summary.total_stations }}</span>
        </div>
      </div>
    </div>

    <!-- Station cards -->
    <div class="row">
      <div 
        v-for="station in stations" 
        :key="station.id" 
        class="col-xl-4 col-lg-6 col-md-6 mb-4"
      >
        <div class="station-status-card">
          <!-- Status indicator circle -->
          <div class="status-circle-container">
            <div 
              class="status-circle" 
              :style="{ backgroundColor: station.status_color }"
              :title="station.status_description"
            ></div>
          </div>

          <!-- Station information -->
          <div class="station-info">
            <h6 class="station-name">{{ station.name }}</h6>
            <p class="station-brand">{{ station.brand }}</p>
            <p class="station-serial">SN: {{ station.serial_number || 'Not Available' }}</p>
          </div>

          <!-- Status details -->
          <div class="status-details">
            <div class="status-main">
              <strong>{{ station.overall_status }}</strong>
            </div>
            <div class="status-description">
              {{ station.status_description }}
            </div>
          </div>

          <!-- Data quality metrics -->
          <div class="data-quality" v-if="station.data_quality_metrics.total_measurements > 0">
            <div class="quality-bar">
              <div class="quality-fill" :style="{ width: (station.data_quality_metrics.valid_measurements / station.data_quality_metrics.total_measurements * 100) + '%' }"></div>
            </div>
            <div class="quality-stats">
              <small>
                {{ station.data_quality_metrics.valid_measurements }}/{{ station.data_quality_metrics.total_measurements }} valid
                ({{ Math.round((station.data_quality_metrics.valid_measurements / station.data_quality_metrics.total_measurements) * 100) }}%)
              </small>
            </div>
          </div>

          <!-- Last update info -->
          <div class="last-update">
            <small class="text-muted">
              Last update: {{ formatLastUpdate(station.last_updated) }}
            </small>
          </div>

          <!-- Health info -->
          <div class="health-info" v-if="station.health_info.battery_status !== 'Unknown'">
            <div class="health-item">
              <span class="health-label">Battery:</span>
              <span class="health-value">{{ station.health_info.battery_status }}</span>
            </div>
            <div class="health-item">
              <span class="health-label">Connectivity:</span>
              <span class="health-value">{{ station.health_info.connectivity_status }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Loading state -->
    <div v-if="isLoading" class="text-center py-4">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
    </div>

    <!-- Error state -->
    <div v-if="error" class="alert alert-danger" role="alert">
      {{ error }}
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

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

// Auto-refresh every 30 seconds
let refreshInterval: number

onMounted(() => {
  fetchStationStatus()
  refreshInterval = setInterval(fetchStationStatus, 30000) // 30 seconds
})

// Cleanup interval on component unmount
import { onUnmounted } from 'vue'
onUnmounted(() => {
  if (refreshInterval) {
    clearInterval(refreshInterval)
  }
})
</script>

<style scoped>
.station-status-overview {
  padding: 1rem;
}

.status-header {
  background: white;
  padding: 1.5rem;
  border-radius: 0.5rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.status-summary {
  flex-wrap: wrap;
}

.status-summary-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.status-indicator {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  display: inline-block;
}

.status-indicator.online {
  background-color: #28a745;
}

.status-indicator.online-erroneous {
  background-color: #ffc107;
}

.status-indicator.offline {
  background-color: #dc3545;
}

.status-label {
  font-size: 0.9rem;
  color: #6c757d;
}

.station-status-card {
  background: white;
  border-radius: 0.5rem;
  padding: 1.5rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
  border: 1px solid #e9ecef;
  position: relative;
  transition: transform 0.2s, box-shadow 0.2s;
}

.station-status-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.status-circle-container {
  position: absolute;
  top: 1rem;
  right: 1rem;
}

.status-circle {
  width: 16px;
  height: 16px;
  border-radius: 50%;
  border: 2px solid white;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.station-info {
  margin-bottom: 1rem;
}

.station-name {
  margin: 0 0 0.25rem 0;
  font-weight: 600;
  color: #212529;
}

.station-brand {
  margin: 0 0 0.25rem 0;
  font-size: 0.875rem;
  color: #6c757d;
  text-transform: capitalize;
}

.station-serial {
  margin: 0;
  font-size: 0.75rem;
  color: #adb5bd;
  font-family: monospace;
}

.status-details {
  margin-bottom: 1rem;
}

.status-main {
  font-size: 0.9rem;
  margin-bottom: 0.25rem;
}

.status-description {
  font-size: 0.8rem;
  color: #6c757d;
  line-height: 1.3;
}

.data-quality {
  margin-bottom: 1rem;
}

.quality-bar {
  width: 100%;
  height: 6px;
  background-color: #e9ecef;
  border-radius: 3px;
  overflow: hidden;
  margin-bottom: 0.5rem;
}

.quality-fill {
  height: 100%;
  background-color: #28a745;
  transition: width 0.3s ease;
}

.quality-stats {
  text-align: center;
}

.health-info {
  margin-bottom: 1rem;
  padding-top: 1rem;
  border-top: 1px solid #e9ecef;
}

.health-item {
  display: flex;
  justify-content: space-between;
  margin-bottom: 0.25rem;
  font-size: 0.8rem;
}

.health-label {
  color: #6c757d;
}

.health-value {
  font-weight: 500;
  color: #495057;
}

.last-update {
  text-align: center;
  padding-top: 0.5rem;
  border-top: 1px solid #e9ecef;
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .status-summary {
    flex-direction: column;
    gap: 0.5rem;
  }
  
  .station-status-card {
    padding: 1rem;
  }
}
</style> 