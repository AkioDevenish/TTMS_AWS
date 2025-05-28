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
          <a class="dropdown-item" href="#" @click.prevent="selectMeasurement('wind_ave10')">Wind Speed (Average)</a>
          <a class="dropdown-item" href="#" @click.prevent="selectMeasurement('dir_ave10')">Wind Direction (Average)</a>
          <a class="dropdown-item" href="#" @click.prevent="selectMeasurement('battery')">Battery</a>
        </div>
      </div>
    </div>

    <div class="chart-container">
      <apexchart
        v-if="chartData.length > 0"
        type="area"
        height="330"
        ref="chart"
        :options="chartOptions"
        :series="chartData"
      ></apexchart>
      <div v-else>
        <p>No data available to display.</p>
      </div>
    </div>
  </Card1>
</template>

<script lang="ts" setup>
import { defineAsyncComponent, ref, watch, computed, defineProps } from 'vue';
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
const selectedSensorType = ref<string>('wind_ave10');
const chartData = ref<any[]>([]);
const isLoading = ref(false);
const sensorConfig: Record<string, { name: string; unit: string }> = {
	'wind_ave10': { name: 'Wind Speed (Average)', unit: 'm/s' },
	'dir_ave10': { name: 'Wind Direction (Average)', unit: '°' },
	'battery': { name: 'Battery', unit: 'V' }
};
const currentSensorName = computed(() => {
	return sensorConfig[selectedSensorType.value]?.name || selectedSensorType.value;
});
const currentSensorUnit = computed(() => {
	return sensorConfig[selectedSensorType.value]?.unit || '';
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
	}
}));
watch([() => props.measurements, () => selectedSensorType.value], 
	([newMeasurements, newSensorType]) => {
		if (!newMeasurements?.length) {
			chartData.value = [];
			return;
		}
		const filteredData = newMeasurements.filter(
			measurement => measurement.sensor_type === newSensorType
		);
		if (!filteredData.length) {
			chartData.value = [];
			return;
		}
		chartData.value = [{
			name: sensorConfig[newSensorType]?.name || newSensorType,
			data: filteredData.map(item => ({
				x: new Date(`${item.date}T${item.time}`).getTime(),
				y: parseFloat(item.value.toString())
			}))
		}];
	}, 
	{ immediate: true }
);
const selectMeasurement = (sensorType: string) => {
	selectedSensorType.value = sensorType;
};
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
</style>