<template>
  <div class="station-status-summary">
    <div class="status-header">
      <h6 class="status-title">Station Status Overview</h6>
      <div class="status-legend">
        <div class="legend-item">
          <div class="legend-indicator online"></div>
          <span>Online</span>
        </div>
        <div class="legend-item">
          <div class="legend-indicator online-erroneous-data"></div>
          <span>Online Erroneous Data</span>
        </div>
        <div class="legend-item">
          <div class="legend-indicator offline"></div>
          <span>Offline</span>
        </div>
      </div>
    </div>
    
    <div class="status-counts">
      <div class="status-count online">
        <span class="count">{{ onlineCount }}</span>
        <span class="label">Online</span>
      </div>
      <div class="status-count online-erroneous-data">
        <span class="count">{{ onlineNoDataCount }}</span>
        <span class="label">Erroneous Data</span>
      </div>
      <div class="status-count offline">
        <span class="count">{{ offlineCount }}</span>
        <span class="label">Offline</span>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { computed } from 'vue'

interface Props {
  stations: Array<{
    status: string
    dataQuality?: {
      validCount: number
      totalCount: number
      validPercentage: number
    }
  }>
}

const props = defineProps<Props>()

const onlineCount = computed(() => 
  props.stations.filter(s => s.status === 'Online').length
)

const onlineNoDataCount = computed(() => 
  props.stations.filter(s => s.status === 'Online Erroneous Data').length
)

const offlineCount = computed(() => 
  props.stations.filter(s => s.status === 'Offline').length
)
</script>

<style scoped>
.station-status-summary {
  background: white;
  border-radius: 0.5rem;
  padding: 1rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
  border: 1px solid #e9ecef;
}

.status-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.status-title {
  margin: 0;
  font-weight: 600;
  color: #2c3e50;
  font-size: 0.9rem;
}

.status-legend {
  display: flex;
  gap: 1rem;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.75rem;
  color: #6c757d;
}

.legend-indicator {
  width: 8px;
  height: 8px;
  border-radius: 50%;
}

.legend-indicator.online {
  background-color: #28a745;
}

.legend-indicator.online-erroneous-data {
  background-color: #ffc107;
}

.legend-indicator.offline {
  background-color: #dc2626;
}

.status-counts {
  display: flex;
  gap: 1rem;
  justify-content: space-around;
}

.status-count {
  text-align: center;
  flex: 1;
}

.status-count .count {
  display: block;
  font-size: 1.5rem;
  font-weight: 700;
  line-height: 1;
}

.status-count .label {
  display: block;
  font-size: 0.75rem;
  color: #6c757d;
  margin-top: 0.25rem;
}

.status-count.online .count {
  color: #28a745;
}

.status-count.online-erroneous-data .count {
  color: #ffc107;
}

.status-count.offline .count {
  color: #dc2626;
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .status-header {
    flex-direction: column;
    gap: 0.5rem;
    align-items: flex-start;
  }
  
  .status-legend {
    gap: 0.75rem;
  }
  
  .status-counts {
    gap: 0.5rem;
  }
}
</style> 