<template>
  <div class="container-fluid dashboard-station-status">
    <div class="row mb-4">
      <div class="col-12">
        <div class="page-header">
          <h2 class="page-title">MDPS - AWS Station Status Dashboard</h2>
          <p class="page-description">
            Real-time monitoring of all weather stations with comprehensive status information
          </p>
        </div>
      </div>
    </div>

    <!-- Station Status Overview Component -->
    <div class="row">
      <div class="col-12">
        <StationStatusOverview />
      </div>
    </div>

    <!-- Additional Status Information -->
    <div class="row mt-4">
      <div class="col-12">
        <div class="status-legend">
          <h5>Status Legend</h5>
          <div class="legend-items">
            <div class="legend-item">
              <div class="legend-indicator online"></div>
              <div class="legend-text">
                <strong>Online</strong>
                <p>Stations reporting valid data within expected parameters</p>
              </div>
            </div>
            <div class="legend-item">
              <div class="legend-indicator online-erroneous"></div>
              <div class="legend-text">
                <strong>Online Erroneous Data</strong>
                <p>Stations transmitting but data fails validation</p>
              </div>
            </div>
            <div class="legend-item">
              <div class="legend-indicator offline"></div>
              <div class="legend-text">
                <strong>Offline</strong>
                <p>Stations not reporting data (no recent transmissions)</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { defineAsyncComponent } from 'vue'

const StationStatusOverview = defineAsyncComponent(() => 
  import('@/components/theme/stations/StationStatusOverview.vue')
)
</script>

<style scoped>
.dashboard-station-status {
  padding: 1rem;
}

.page-header {
  background: white;
  padding: 2rem;
  border-radius: 0.5rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
  text-align: center;
  margin-bottom: 2rem;
}

.page-title {
  color: #2c3e50;
  margin-bottom: 0.5rem;
  font-weight: 600;
}

.page-description {
  color: #6c757d;
  margin: 0;
  font-size: 1.1rem;
}

.status-legend {
  background: white;
  padding: 1.5rem;
  border-radius: 0.5rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.status-legend h5 {
  color: #2c3e50;
  margin-bottom: 1rem;
  font-weight: 600;
}

.legend-items {
  display: flex;
  gap: 2rem;
  flex-wrap: wrap;
}

.legend-item {
  display: flex;
  align-items: flex-start;
  gap: 0.75rem;
  min-width: 250px;
}

.legend-indicator {
  width: 16px;
  height: 16px;
  border-radius: 50%;
  margin-top: 0.25rem;
  flex-shrink: 0;
}

.legend-indicator.online {
  background-color: #28a745;
}

.legend-indicator.online-erroneous {
  background-color: #ffc107;
}

.legend-indicator.offline {
  background-color: #dc3545;
}

.legend-text strong {
  color: #2c3e50;
  font-size: 0.95rem;
}

.legend-text p {
  color: #6c757d;
  font-size: 0.85rem;
  margin: 0.25rem 0 0 0;
  line-height: 1.4;
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .page-header {
    padding: 1.5rem;
  }
  
  .legend-items {
    flex-direction: column;
    gap: 1rem;
  }
  
  .legend-item {
    min-width: auto;
  }
}
</style> 