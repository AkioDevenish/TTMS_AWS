<template>
  <div class="col-12">
    <Card1 headerTitle="true" title="Barani Instance Monitor" cardClass="monitor-card">
      <div class="table-responsive">
        <table class="table">
          <thead>
            <tr>
              <th>Station Name</th>
              <th>Station ID</th>
              <th>Date</th>
              <th>Time</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="item in latestData" :key="item.id">
              <td>
                <div class="d-flex align-items-center gap-2">
                  <div class="status-dot" :class="{ 'bg-success': item.status === 'successful', 'bg-danger': item.status !== 'successful' }"></div>
                  {{ item.name }}
                </div>
              </td>
              <td>{{ item.id }}</td>
              <td>{{ formatDate(item.lastUpdated) }}</td>
              <td>{{ formatTime(item.lastUpdated) }}</td>
              <td>
                <span :class="{ 'text-success': item.status === 'successful', 'text-danger': item.status !== 'successful' }">
                  {{ item.status === 'successful' ? 'Successful' : 'Failed' }}
                </span>
              </td>
            </tr>
            <tr v-if="!latestData.length">
              <td colspan="5" class="text-center">No data available</td>
            </tr>
          </tbody>
        </table>
      </div>
    </Card1>
  </div>
</template>

<script lang="ts" setup>
import { ref, onMounted, watch } from 'vue';
import { defineAsyncComponent } from 'vue';
import axios from 'axios';

const Card1 = defineAsyncComponent(() => import("@/components/common/card/CardData1.vue"));

interface StationData {
  id: number;
  name: string;
  status: string;
  lastUpdated: string;
}

const props = defineProps({
  selectedStation: {
    type: Number,
    required: true
  }
});

const latestData = ref<StationData[]>([]);

const fetchData = async () => {
  if (!props.selectedStation) return;

  try {
    // First request - get station info
    const stationResponse = await axios.get(`http://127.0.0.1:8000/stations/${props.selectedStation}/`);
    if (!stationResponse.data) {
      throw new Error('Station not found');
    }
    const stationName = stationResponse.data.name;

    // Second request - get measurements
    const measurementsResponse = await axios.get(`http://127.0.0.1:8000/measurements/by_station/?station_id=${props.selectedStation}`);
    if (!measurementsResponse.data || measurementsResponse.status !== 200) {
      throw new Error(`Measurements request failed with status ${measurementsResponse.status}`);
    }

    if (measurementsResponse.data.length > 0) {
      const latestMeasurement = measurementsResponse.data.sort((a: any, b: any) => {
        const dateA = new Date(`${b.date}T${b.time}`);
        const dateB = new Date(`${a.date}T${a.time}`);
        return dateA.getTime() - dateB.getTime();
      })[0];

      latestData.value = [{
        id: props.selectedStation,
        name: stationName,
        status: latestMeasurement.status,
        lastUpdated: `${latestMeasurement.date}T${latestMeasurement.time}`,
      }];
    } else {
      latestData.value = [];
    }
  } catch (error) {
    console.error('Error fetching data:', error);
    latestData.value = [];
  }
};

const formatDate = (timestamp: string) => {
  if (!timestamp) return '';
  const date = new Date(timestamp);
  return date.toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  });
};

const formatTime = (timestamp: string) => {
  if (!timestamp) return '';
  const date = new Date(timestamp);
  return date.toLocaleTimeString('en-US', {
    hour: '2-digit',
    minute: '2-digit',
    hour12: true
  });
};

watch(() => props.selectedStation, () => {
  if (props.selectedStation) {
    fetchData();
  }
}, { immediate: true });
</script>

<style scoped>
.status-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  display: inline-block;
}

.monitor-card {
  margin-bottom: 1.5rem;
}

.table th {
  font-weight: 600;
  background-color: #f8f9fa;
}

.table td {
  vertical-align: middle;
}
</style>