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
                    <tbody>
                        <tr v-for="(item, index) in latestData" :key="index">
                            <td>
                                <div class="d-flex align-items-center">
                                    <div class="d-flex align-items-center">  
                                            <h6>{{ item.name }}</h6>
                                    </div>
                                </div>
                            </td>
                            <td>{{ item.id }}</td>
                            <td>{{ formatDate(item.lastUpdated) }}</td>
                            <td>{{ formatTime(item.lastUpdated) }}</td>
                            <td>

                                {{ item.status }}
                     
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    </Card1>
</template>
  
<script lang="ts" setup>
import { ref, defineAsyncComponent, onMounted, watch, defineProps } from 'vue'
import axios from 'axios';

const Card1 = defineAsyncComponent(() => import("@/components/common/card/CardData1.vue"))

const props = defineProps({
    selectedStation: {
        type: Number,
        required: true
    }
});

const latestData = ref<any[]>([])
const connectionStatus = ref<string>('Unsuccessful')
const monitorTitle = ref<string>('3DPaws Monitor')

const fetchData = async () => {
    try {
        // First request - get station details
        const stationResponse = await axios.get(`http://127.0.0.1:8000/stations/${props.selectedStation}/`);
        if (!stationResponse.data || stationResponse.status !== 200) {
            throw new Error(`Station request failed with status ${stationResponse.status}`);
        }
        const stationName = stationResponse.data.name;

        // Second request - get measurements
        const measurementsResponse = await axios.get(`http://127.0.0.1:8000/measurements/by_station/?station_id=${props.selectedStation}`);
        if (!measurementsResponse.data || measurementsResponse.status !== 200) {
            throw new Error(`Measurements request failed with status ${measurementsResponse.status}`);
        }

        console.log('Station Response:', stationResponse.data);
        console.log('Measurements Response:', measurementsResponse.data);

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

            connectionStatus.value = 'Successful';
        } else {
            connectionStatus.value = 'No measurements found';
        }
    } catch (error: any) {
        console.error('Error details:', error.response?.data || error.message);
        connectionStatus.value = `Error: ${error.response?.status || 'Network error'}`;
    }
};

watch(() => props.selectedStation, fetchData);

onMounted(fetchData);

const formatDate = (timestamp: string) => {
    try {
        if (!timestamp || typeof timestamp !== 'string') return 'Invalid Date';
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
};

const formatTime = (timestamp: string) => {
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
};
</script>
