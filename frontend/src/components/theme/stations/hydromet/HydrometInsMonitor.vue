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
                                        <i class="status-dot" :class="{ 'online': item.status === 'Successful', 'offline': item.status !== 'Successful' }"></i>
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
const latestData = ref<any[]>([])
const connectionStatus = ref<string>('Unsuccessful')
const monitorTitle = ref<string>('OTT Monitor')
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
        // Find the latest measurement by date/time
        const latestMeasurement: any = [...newMeasurements].sort((a: any, b: any) => {
            const dateA = new Date(`${a.date}T${a.time}`);
            const dateB = new Date(`${b.date}T${b.time}`);
            return dateB.getTime() - dateA.getTime();
        })[0];
        latestData.value = [{
            id: newStationInfo.serial_number,
            name: newStationInfo.name,
            status: latestMeasurement?.status || 'Unknown',
            lastUpdated: `${latestMeasurement?.date || ''}T${latestMeasurement?.time || ''}`,
        }];
        connectionStatus.value = 'Successful';
    } catch (error) {
        console.error('Error processing measurements:', error);
        latestData.value = [];
        connectionStatus.value = 'Error processing data';
    }
}, { immediate: true });
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