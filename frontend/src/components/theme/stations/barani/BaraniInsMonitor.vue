<template>
  <Card1 colClass="col-xl-12 col-md-12 proorder-md-1" headerTitle="true" :title="monitorTitle"
      cardhaderClass="card-no-border pb-0" cardbodyClass="pt-0 assignments-table px-0">
      <div class="table-responsive theme-scrollbar">
          <div id="recent-order_wrapper" class="dataTables_wrapper no-footer">
              <table class="table display dataTable" id="assignments-table" style="width:100%">
                  <thead>
                      <tr>
                          <th>Name</th>
                          <th>ID</th>
                          <th>Date</th>
                          <th>Time</th>
                          <th>Status</th>
                      </tr>
                  </thead>
                  <tbody v-if="!latestData.length">
                      <tr class="odd">
                          <td valign="top" colspan="6" class="dataTables_empty">{{ connectionStatus }}</td>
                      </tr>
                  </tbody>
                  <tbody v-else>
                      <tr v-for="(item, index) in latestData" :key="index">
                          <td>
                              <div class="d-flex align-items-center">
                                  <div class="d-flex align-items-center">
                                      <h6>{{ item.name }}</h6>
                                      <i class="status-dot" :class="{ 'online': item.status === 'Online', 'offline': item.status !== 'Online' }"></i>
                                  </div>
                              </div>
                          </td>
                          <td>{{ item.id }}</td>
                          <td>{{ formatDateTime.date(item.lastUpdated) }}</td>
                          <td>{{ formatDateTime.time(item.lastUpdated) }}</td>
                          <td>{{ item.status }}</td>
                      </tr>
                  </tbody>
              </table>
          </div>
      </div>
  </Card1>
</template>

<script lang="ts" setup>
import { ref, defineAsyncComponent, watch, defineProps } from 'vue'
const Card1 = defineAsyncComponent(() => import("@/components/common/card/CardData1.vue"))

// Add Measurement interface
interface Measurement {
  sensor_type: string;
  date: string;
  time: string;
  value: number;
  status?: string;
}

// Add MonitorRow interface for table rows
interface MonitorRow {
  id: string;
  name: string;
  status: string;
  lastUpdated: string;
  lastUpdatedAgo: string;
}

const props = defineProps({
    selectedStation: {
        type: Number,
        required: true
    },
    measurements: {
        type: Array as () => Measurement[],
        default: () => []
    },
    stationInfo: {
        type: Object,
        default: () => ({})
    }
});
const latestData = ref<MonitorRow[]>([])
const connectionStatus = ref<string>('Unsuccessful')
const monitorTitle = ref<string>('Barani Monitor')
// Local date/time formatter
const formatDateTime = {
    date: (timestamp: string) => {
        try {
            if (!timestamp) return 'Invalid Date';
            const date = new Date(timestamp);
            if (isNaN(date.getTime())) return 'Invalid Date';
            return date.toLocaleDateString('en-US', {
                year: 'numeric',
                month: '2-digit',
                day: '2-digit'
            });
        } catch {
            return 'Invalid Date';
        }
    },
    time: (timestamp: string) => {
        try {
            const date = new Date(timestamp);
            if (isNaN(date.getTime())) return 'Invalid Time';
            return date.toLocaleTimeString('en-US', {
                hour: '2-digit',
                minute: '2-digit',
                second: '2-digit',
                hour12: true
            });
        } catch {
            return 'Invalid Time';
        }
    }
};

// Barani/Allmeteo sensor config
const sensorConfig: Record<string, { name: string }> = {
    'wind_ave10': { name: 'Wind Speed (Average)' },
    'wind_max10': { name: 'Wind Speed (Max)' },
    'wind_min10': { name: 'Wind Speed (Min)' },
    'dir_ave10': { name: 'Wind Direction (Average)' },
    'dir_max10': { name: 'Wind Direction (Max)' },
    'dir_hi10': { name: 'Wind Direction (High)' },
    'dir_lo10': { name: 'Wind Direction (Low)' },
    'battery': { name: 'Battery' },
    'humidity': { name: 'Humidity' },
    'irradiation': { name: 'Irradiation' },
    'irr_max': { name: 'Irradiation (Max)' },
    'pressure': { name: 'Pressure' },
    'temperature': { name: 'Temperature' },
    'temperature_max': { name: 'Temperature (Max)' },
    'temperature_min': { name: 'Temperature (Min)' },
    'rain_counter': { name: 'Rain Counter' },
    'rain_intensity_max': { name: 'Rain Intensity (Max)' }
};

watch([
    () => props.measurements,
    () => props.stationInfo
], ([newMeasurements, newStationInfo]) => {
    if (!newMeasurements?.length || !newStationInfo) {
        latestData.value = [];
        connectionStatus.value = 'Unsuccessful';
        return;
    }
    try {
        // Sort all measurements by date/time descending
        const sorted = [...newMeasurements].sort((a: any, b: any) => {
            const dateA = new Date(`${a.date}T${a.time}`);
            const dateB = new Date(`${b.date}T${b.time}`);
            return dateB.getTime() - dateA.getTime();
        });
        const now = Date.now();
        // Find any measurement in the last 60 minutes
        const onlineThresholdMinutes = 60;
        const recentMeasurement = sorted.find((m: any) => {
            const measurementTime = new Date(`${m.date}T${m.time}`).getTime();
            const diffMinutes = (now - measurementTime) / (1000 * 60);
            return diffMinutes <= onlineThresholdMinutes;
        });
        let status = 'Offline';
        let lastUpdated = 'N/A';
        let lastUpdatedAgo = '';
        let latest = sorted[0];
        if (recentMeasurement) {
            status = 'Online';
            latest = recentMeasurement;
        }
        if (latest) {
            lastUpdated = `${latest.date}T${latest.time}`;
            const measurementTime = new Date(`${latest.date}T${latest.time}`).getTime();
            const diffMinutes = Math.round((now - measurementTime) / (1000 * 60));
            lastUpdatedAgo = diffMinutes === 0 ? 'just now' : `${diffMinutes} min ago`;
        } else {
            lastUpdated = 'N/A';
            lastUpdatedAgo = '';
        }
        latestData.value = [{
            id: newStationInfo.serial_number ?? newStationInfo.serialNumber ?? newStationInfo.id ?? 'N/A',
            name: newStationInfo.name ?? newStationInfo.station_name ?? 'N/A',
            status,
            lastUpdated,
            lastUpdatedAgo
        }];
        connectionStatus.value = 'Successful';
    } catch (error) {
        console.error('Error processing measurements:', error);
        latestData.value = [];
        connectionStatus.value = 'Error processing data';
    }
}, { immediate: true });

watch(
  () => props.stationInfo,
  (val) => {
    console.log('BaraniInsMonitor stationInfo:', val);
  },
  { immediate: true }
);
</script>


<style scoped>
.status-dot {
    display: inline-block;
    width: 8px;
    height: 8px;
    min-width: 8px;
    min-height: 8px;
    border-radius: 50%;
    margin-left: 8px;
    flex: none;
}

.online {
    background-color: #51bb25;
}

.offline {
    background-color: #dc3545;
}
</style>