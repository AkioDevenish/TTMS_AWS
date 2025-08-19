<template>
  <div class="container-fluid dashboard-weather-stations">
    <div class="row mb-4">
      <div class="col-12">
        <div class="page-header">
          <h2 class="page-title">Weather Stations Overview</h2>
          <p class="page-description">
            Select a weather station type to view detailed information and data
          </p>
        </div>
      </div>
    </div>

    <div class="row">
      <div class="col-12">
        <div class="station-types-grid">
          <!-- OTT Hydromet -->
          <div class="station-type-card" @click="navigateToStation('AWS_OTT_Hyrdomet')">
            <div class="card-icon ott">
              <i class="fas fa-droplet"></i>
            </div>
            <div class="card-content">
              <h3>OTT Hydromet</h3>
              <p>Professional hydrological and meteorological monitoring stations</p>
              <div class="station-count" v-if="stationCounts.ott > 0">
                {{ stationCounts.ott }} active stations
              </div>
            </div>
            <div class="card-arrow">
              <i class="fas fa-chevron-right"></i>
            </div>
          </div>

          <!-- Barani -->
          <div class="station-type-card" @click="navigateToStation('AWS_Barani')">
            <div class="card-icon barani">
              <i class="fas fa-cloud"></i>
            </div>
            <div class="card-content">
              <h3>Barani</h3>
              <p>Advanced weather monitoring with comprehensive sensor arrays</p>
              <div class="station-count" v-if="stationCounts.barani > 0">
                {{ stationCounts.barani }} active stations
              </div>
            </div>
            <div class="card-arrow">
              <i class="fas fa-chevron-right"></i>
            </div>
          </div>

          <!-- Zentra -->
          <div class="station-type-card" @click="navigateToStation('AWS_Zentra')">
            <div class="card-icon zentra">
              <i class="fas fa-wind"></i>
            </div>
            <div class="card-content">
              <h3>Zentra</h3>
              <p>High-precision environmental monitoring systems</p>
              <div class="station-count" v-if="stationCounts.zentra > 0">
                {{ stationCounts.zentra }} active stations
              </div>
            </div>
            <div class="card-arrow">
              <i class="fas fa-chevron-right"></i>
            </div>
          </div>

          <!-- 3D Paws -->
          <div class="station-type-card" @click="navigateToStation('AWS_3D_Paws')">
            <div class="card-icon paws">
              <i class="fas fa-satellite-dish"></i>
            </div>
            <div class="card-content">
              <h3>3D Paws</h3>
              <p>Satellite-based weather monitoring and data collection</p>
              <div class="station-count" v-if="stationCounts.paws > 0">
                {{ stationCounts.paws }} active stations
              </div>
            </div>
            <div class="card-arrow">
              <i class="fas fa-chevron-right"></i>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Quick Actions -->
    <div class="row mt-5">
      <div class="col-12">
        <div class="quick-actions">
          <h4>Quick Actions</h4>
          <div class="action-buttons">
            <button class="btn btn-primary" @click="navigateToStation('create')">
              <i class="fas fa-plus"></i>
              Create New AWS
            </button>
            <button class="btn btn-outline-primary" @click="navigateToStation('management')">
              <i class="fas fa-cog"></i>
              Station Management
            </button>
            <button class="btn btn-outline-info" @click="navigateToStation('status')">
              <i class="fas fa-chart-line"></i>
              View All Status
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="isLoading" class="loading-overlay">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';

const router = useRouter();
const isLoading = ref(false);
const stationCounts = ref({
  ott: 0,
  barani: 0,
  zentra: 0,
  paws: 0
});

const navigateToStation = (route: string) => {
  if (route === 'create') {
    router.push('/stations/create');
  } else if (route === 'management') {
    router.push('/pages/station_management');
  } else if (route === 'status') {
    router.push('/dashboards/station_status');
  } else {
    router.push(`/stations/${route}`);
  }
};

const fetchStationCounts = async () => {
  try {
    isLoading.value = true;
    const response = await axios.get('/api/stations/?include_decommissioned=false');
    // Fix: Handle paginated response structure
    const stations = response.data.results || response.data || [];
    
    // Count stations by brand
    stationCounts.value = {
      ott: stations.filter((s: any) => s.brand_name === 'OTT').length,
      barani: stations.filter((s: any) => s.brand_name === 'Allmeteo').length,
      zentra: stations.filter((s: any) => s.brand_name === 'Zentra').length,
      paws: stations.filter((s: any) => s.brand_name === '3D_Paws').length
    };
  } catch (error) {
    console.error('Error fetching station counts:', error);
  } finally {
    isLoading.value = false;
  }
};

onMounted(() => {
  fetchStationCounts();
});
</script>

<style scoped>
.dashboard-weather-stations {
  padding: 2rem;
  background-color: #f8f9fa;
  min-height: 100vh;
}

.page-header {
  text-align: center;
  margin-bottom: 3rem;
}

.page-title {
  color: #2c3e50;
  font-weight: 600;
  margin-bottom: 0.5rem;
}

.page-description {
  color: #6c757d;
  font-size: 1.1rem;
}

.station-types-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
  margin-bottom: 2rem;
}

.station-type-card {
  background: white;
  border-radius: 12px;
  padding: 2rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  border: 2px solid transparent;
}

.station-type-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
  border-color: #7A70BA;
}

.card-icon {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 1.5rem;
  font-size: 1.5rem;
  color: white;
}

.card-icon.ott {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.card-icon.barani {
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
}

.card-icon.zentra {
  background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
}

.card-icon.paws {
  background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
}

.card-content h3 {
  color: #2c3e50;
  font-weight: 600;
  margin-bottom: 0.5rem;
  font-size: 1.3rem;
}

.card-content p {
  color: #6c757d;
  margin-bottom: 1rem;
  line-height: 1.5;
}

.station-count {
  background: #e9ecef;
  color: #495057;
  padding: 0.5rem 1rem;
  border-radius: 20px;
  font-size: 0.9rem;
  font-weight: 500;
  display: inline-block;
}

.card-arrow {
  position: absolute;
  top: 1.5rem;
  right: 1.5rem;
  color: #dee2e6;
  transition: color 0.3s ease;
}

.station-type-card:hover .card-arrow {
  color: #7A70BA;
}

.quick-actions {
  background: white;
  border-radius: 12px;
  padding: 2rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.quick-actions h4 {
  color: #2c3e50;
  margin-bottom: 1.5rem;
  font-weight: 600;
}

.action-buttons {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
}

.action-buttons .btn {
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  font-weight: 500;
  transition: all 0.3s ease;
}

.action-buttons .btn:hover {
  transform: translateY(-2px);
}

.loading-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(255, 255, 255, 0.8);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

@media (max-width: 768px) {
  .dashboard-weather-stations {
    padding: 1rem;
  }
  
  .station-types-grid {
    grid-template-columns: 1fr;
    gap: 1rem;
  }
  
  .action-buttons {
    flex-direction: column;
  }
  
  .action-buttons .btn {
    width: 100%;
  }
}
</style> 