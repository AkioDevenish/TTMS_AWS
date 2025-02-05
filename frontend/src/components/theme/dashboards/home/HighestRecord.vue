<template>
    <Card1 colClass="col-xl-6 proorder-xl-5 box-col-7 proorder-md-5" headerTitle="true" title="Highest Records"
        cardhaderClass="card-no-border" cardbodyClass="projects px-0 pt-1">
        <div class="table-responsive theme-scrollbar">
            <div id="recent-order_wrapper" class="dataTables_wrapper no-footer">
                <div id="recent-order_filter" class="dataTables_filter">
                    <label>Search:<input type="search" placeholder="" v-model="filterQuery"></label>
                </div>
                <table class="table display dataTable no-footer" id="information" style="width:100%">
                    <thead>
                        <tr>
                            <th>Station Name</th>
                            <th>Brand</th>
                            <th>Date</th>
                            <th>Value</th>
                            <th>Sensor Type</th>
                            <th>Unit</th>
                        </tr>
                    </thead>
                    <tbody v-if="!get_rows().length">
                        <tr class="odd">
                            <td valign="top" colspan="6" class="dataTables_empty">No matching records found</td>
                        </tr>
                    </tbody>
                    <tbody v-if="get_rows().length">
                        <tr v-for="(row, index) in get_rows()" :key="index">
                            <td>
                                <div class="d-flex align-items-center">
                                    <h6>{{ row.station_name }}</h6>
                                </div>
                            </td>
                            <td class="project-dot">
                                <div class="d-flex">
                                    <div class="flex-grow-1">
                                        <h6>{{ row.brand_name }}</h6>
                                    </div>
                                </div>
                            </td>
                            <td>{{ formatDate(row.date) }}</td>
                            <td>{{ row.value }}</td>
                            <td>{{ row.sensor_type }}</td>
                            <td>{{ row.sensor_unit }}</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
        <ul class="pagination mx-2 mt-2 justify-content-end">
            <li class="page-item">
                <a class="page-link cursor-pointer" @click="prev()">Previous</a>
            </li>
            <li class="page-item" v-for="i in num_pages()" :key="i" 
                :class="{ active: i === currentPage }">
                <a class="page-link cursor-pointer" @click="change_page(i)">{{ i }}</a>
            </li>
            <li class="page-item">
                <a class="page-link cursor-pointer" @click="next()">Next</a>
            </li>
        </ul>
    </Card1>
</template>

<style scoped>
.cursor-pointer {
    cursor: pointer;
}
</style>

<script lang="ts" setup>
import { ref, defineAsyncComponent, onMounted, watch } from 'vue'
import axios from 'axios'

// Define interfaces for type safety
interface Station {
    id: number;
    name: string;
    brand_name: string;
}

interface Sensor {
    id: number;
    type: string;
    unit: string;
}

interface Measurement {
    station: number;
    sensor: number;
    date: string;
    time: string;
    value: number;
}

interface HighestRecord {
    station_name: string;
    brand_name: string;
    date: string;
    time: string;
    value: number;
    sensor_type: string;
    sensor_unit: string;
}

const Card1 = defineAsyncComponent(() => import("@/components/common/card/CardData1.vue"))

const elementsPerPage = ref<number>(4)
const currentPage = ref<number>(1)
const filterQuery = ref<string>("")
const allData = ref<HighestRecord[]>([])

const formatDate = (date: string) => {
    return new Date(date).toLocaleDateString('en-US', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit'
    });
};

const formatTime = (time: string) => {
    return new Date(`2000-01-01T${time}`).toLocaleTimeString('en-US', {
        hour: '2-digit',
        minute: '2-digit',
        hour12: true
    });
};

const fetchHighestRecords = async () => {
    try {
        const [stationsResponse, measurementsResponse, sensorsResponse] = await Promise.all([
            axios.get<Station[]>('/stations/'),
            axios.get<Measurement[]>('/measurements/'),
            axios.get<Sensor[]>('/sensors/')
        ]);

        // Create maps for quick lookup
        const stationsMap = new Map(stationsResponse.data.map((station: Station) => [station.id, station]));
        const sensorsMap = new Map(sensorsResponse.data.map((sensor: Sensor) => [sensor.id, sensor]));

        // Group measurements by sensor type and find highest value for each
        const highestMeasurements = new Map<string, HighestRecord>();

        measurementsResponse.data.forEach((measurement: Measurement) => {
            const sensor = sensorsMap.get(measurement.sensor);
            const sensorType = sensor?.type || 'Unknown Sensor';
            const station = stationsMap.get(measurement.station);

            if (!highestMeasurements.has(sensorType) || 
                measurement.value > highestMeasurements.get(sensorType)!.value) {
                highestMeasurements.set(sensorType, {
                    station_name: station?.name || 'Unknown Station',
                    brand_name: station?.brand_name || 'Unknown Brand',
                    date: measurement.date,
                    time: measurement.time,
                    value: measurement.value,
                    sensor_type: sensorType,
                    sensor_unit: sensor?.unit || 'N/A'
                });
            }
        });

        // Convert Map to array and sort by value
        allData.value = Array.from(highestMeasurements.values())
            .sort((a, b) => b.value - a.value);

    } catch (error) {
        console.error('Error fetching data:', error);
        allData.value = [];
    }
};

watch(filterQuery, (search: string) => {
    if (!search) {
        fetchHighestRecords();
        return;
    }

    const filteredData = allData.value.filter((row: any) => {
        return (
            row.station_name.toLowerCase().includes(search.toLowerCase()) ||
            row.brand_name.toLowerCase().includes(search.toLowerCase()) ||
            row.sensor_type.toLowerCase().includes(search.toLowerCase())
        );
    });
    allData.value = filteredData;
});

const get_rows = () => {
    const start = (currentPage.value - 1) * elementsPerPage.value;
    const end = start + elementsPerPage.value;
    return allData.value.slice(start, end);
};

const num_pages = () => {
    return Math.ceil(allData.value.length / elementsPerPage.value);
};

const change_page = (page: number) => {
    currentPage.value = page;
};

const next = () => {
    if (currentPage.value < num_pages()) {
        currentPage.value++;
    }
};

const prev = () => {
    if (currentPage.value > 1) {
        currentPage.value--;
    }
};

onMounted(() => {
    fetchHighestRecords();
});
</script>