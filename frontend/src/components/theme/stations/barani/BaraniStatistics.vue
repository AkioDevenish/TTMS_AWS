<template>
  <Card1
    colClass="col-xl-12 col-md-12 proorder-xl-2 proorder-md-2"
    dropdown="true"
    cardhaderClass="card-no-border pb-0"
  >
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h4 class="mb-0">{{ stationInfo?.name || 'Station Statistics' }}</h4>
      <div class="dropdown position-relative">
        <button
          class="btn dropdown-toggle w-100 d-flex align-items-center justify-content-between"
          id="measurementDropdown"
          type="button"
          data-bs-toggle="dropdown"
          aria-expanded="false"
        >
          <span class="mx-auto">{{ currentSensorName }}</span>
          <span class="dropdown-toggle-icon ms-3"></span>
        </button>

        <div
          class="dropdown-menu dropdown-menu-end position-absolute"
          aria-labelledby="measurementDropdown"
        >
          <a v-for="sensor in availableSensors" :key="sensor.type" class="dropdown-item" href="#" @click.prevent="selectMeasurement(sensor.type)">
            {{ sensor.name }}
          </a>
        </div>
      </div>
    </div>

    <div class="chart-container">
      <div v-if="isLoading" class="d-flex justify-content-center align-items-center" style="height: 330px;">
				<div class="spinner-border text-primary" role="status">
					<span class="visually-hidden">Loading...</span>
				</div>
			</div>
      <apexchart
        v-else-if="chartData.length > 0"
        type="area"
        height="330"
        ref="chart"
        :options="chartOptions"
        :series="chartData"
      ></apexchart>
      <div v-else class="d-flex justify-content-center align-items-center" style="height: 330px;">
        <p class="text-muted">No data available to display.</p>
      </div>
    </div>
  </Card1>
</template>

<script lang="ts" setup>
import { defineAsyncComponent, ref, watch, computed, defineProps, onMounted, onUnmounted } from 'vue';
import axios from 'axios';
import { useStationData, type Measurement } from '@/composables/useStationData';
const Card1 = defineAsyncComponent(() => import('@/components/common/card/CardData1.vue'));

const props = defineProps({
	selectedStation: {
		type: Number,
		required: true
	},
	measurements: {
		type: Array,
		default: () => []
	},
	stationInfo: {
		type: Object,
		default: () => ({})
	}
});

const selectedSensorType = ref<string>('');
const chartData = ref<any[]>([]);
const availableSensors = ref<Array<{type: string, name: string, unit: string}>>([]);

const baraniData = useStationData();

const fetchAvailableSensors = async () => {
    if (!props.selectedStation) return;
    
    try {
        const response = await axios.get(`/station-sensors/`, {
            params: {
                station_id: props.selectedStation,
                brand: 'AllMeteo',
            }
        });
        
        if (response.data && Array.isArray(response.data)) {
            const uniqueSensors = new Map();
            
            // Filter and deduplicate sensors
            response.data.forEach(sensor => {
                if (!uniqueSensors.has(sensor.sensor_type)) {
                    uniqueSensors.set(sensor.sensor_type, {
                        type: sensor.sensor_type,
                        name: sensor.name || sensor.sensor_type,
                        unit: sensor.unit || ''
                    });
                }
            });

            availableSensors.value = Array.from(uniqueSensors.values());
            
            if (availableSensors.value.length > 0 && !selectedSensorType.value) {
                selectedSensorType.value = availableSensors.value[0].type;
                if (props.selectedStation && selectedSensorType.value) {
                    baraniData.fetchStationData(props.selectedStation, selectedSensorType.value, 12);
                }
            }
        }
    } catch (error) {
        console.error('Error fetching available sensors:', error);
        availableSensors.value = [];
        selectedSensorType.value = '';
    }
};

const currentSensorName = computed(() => {
    const sensor = availableSensors.value.find(s => s.type === selectedSensorType.value);
    return sensor?.name || selectedSensorType.value;
});

const currentSensorUnit = computed(() => {
    const sensor = availableSensors.value.find(s => s.type === selectedSensorType.value);
    return sensor?.unit || '';
});

const chartOptions = computed(() => ({
	yaxis: {
		title: {
			text: `${currentSensorName.value} (${currentSensorUnit.value})`,
			style: {
				fontSize: '14px',
				fontWeight: 500
			}
		},
		labels: {
			formatter: (val: number) => `${val.toFixed(1)} ${currentSensorUnit.value}`
		}
	},
	xaxis: {
		type: 'datetime',
		labels: {
			formatter: (val: number) => {
				const date = new Date(val);
				return date.toLocaleString('en-US', {
					month: 'numeric',
					day: 'numeric',
					hour: '2-digit',
					minute: '2-digit',
					hour12: true
				});
			}
		}
	},
	tooltip: {
		x: {
			formatter: (val: number) => {
				const date = new Date(val);
				return date.toLocaleString('en-US', {
					month: 'numeric',
					day: 'numeric',
					hour: '2-digit',
					minute: '2-digit',
					hour12: true
				});
			}
		},
		y: {
			formatter: (val: number) => `${val.toFixed(1)} ${currentSensorUnit.value}`
		}
	},
	colors: ['#7A70BA']
}));

watch([() => baraniData.measurements.value, () => selectedSensorType.value], 
	([newMeasurements, newSensorType]) => {
		if (!newMeasurements?.length) {
			chartData.value = [];
			return;
		}
		const filteredData = newMeasurements.filter(
			(measurement: Measurement) => measurement.sensor_type === newSensorType
		);
		if (!filteredData.length) {
			chartData.value = [];
			return;
		}
		chartData.value = [{
			name: availableSensors.value.find(s => s.type === newSensorType)?.name || newSensorType,
			data: filteredData.map(item => ({
				x: new Date(`${item.date}T${item.time}`).getTime(),
				y: parseFloat(item.value.toString())
			}))
		}];
	}, 
	{ immediate: true }
);

let fetchTimeout: number | null = null;

watch([() => props.selectedStation, () => availableSensors.value, () => selectedSensorType.value], ([newStationId, newAvailableSensors, newSensorType]) => {
    if (newStationId && newAvailableSensors.length > 0 && newSensorType && newSensorType !== '') {
        if (fetchTimeout) {
            clearTimeout(fetchTimeout);
        }
        fetchTimeout = setTimeout(() => {
            baraniData.fetchStationData(newStationId, newSensorType, 12);
        }, 300);
    } else {
        baraniData.measurements.value = [];
    }
}, { immediate: true });

onMounted(() => {
    fetchAvailableSensors();
});

onUnmounted(() => {
    if (fetchTimeout) {
        clearTimeout(fetchTimeout);
    }
});

const selectMeasurement = (sensorType: string) => {
	selectedSensorType.value = sensorType;
};

const isLoading = computed(() => baraniData.isLoading.value);
</script>

<style scoped>
.chart-container {
  min-height: 350px;
}

.dropdown-menu {
  max-height: 300px;
  overflow-y: auto;
}

.btn.dropdown-toggle {
  background-color: #f8f9fa;
  border: 1px solid #dee2e6;
  color: #495057;
  padding: 0.5rem 1rem;
}

.dropdown-toggle-icon {
	border-left: 4px solid transparent;
	border-right: 4px solid transparent;
	border-top: 4px solid currentColor;
	display: inline-block;
	margin-left: 0.255em;
	vertical-align: middle;
}
</style>