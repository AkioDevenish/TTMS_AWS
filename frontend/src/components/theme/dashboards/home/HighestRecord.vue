<template>
    <Card1 colClass="col-xl-12 col-lg-12 col-md-12 order-3" headerTitle="true" title="Highest Records"
        cardhaderClass="card-no-border" cardbodyClass="projects px-0 pt-1">
        
        <!-- Brand Tabs -->
        <ul class="nav nav-tabs border-tab nav-primary mb-3" role="tablist">
            <li class="nav-item" v-for="brand in uniqueBrands" :key="brand">
                <a class="nav-link" :class="{ active: selectedBrand === brand }" 
                   @click="selectedBrand = brand">
                    {{ brand }}
                </a>
            </li>
        </ul>

        <div class="table-responsive theme-scrollbar">
            <div id="recent-order_wrapper" class="dataTables_wrapper no-footer">
                <div id="recent-order_filter" class="dataTables_filter">
                    <label>Search:<input type="search" placeholder="" v-model="filterQuery"></label>
                </div>
                <table class="table display dataTable no-footer" id="information" style="width:100%">
                    <thead>
                        <tr>
                            <th>Station Name</th>
                            <th>Date</th>
                            <th>Value</th>
                            <th>Sensor Type</th>
                            <th>Unit</th>
                        </tr>
                    </thead>
                    <tbody v-if="!filteredRows.length">
                        <tr class="odd">
                            <td valign="top" colspan="5" class="dataTables_empty">No matching records found</td>
                        </tr>
                    </tbody>
                    <tbody v-if="filteredRows.length">
                        <tr v-for="(row, index) in paginatedRows" :key="index">
                            <td>
                                <div class="d-flex align-items-center">
                                    <h6>{{ row.station_name }}</h6>
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
            <li class="page-item" :class="{ disabled: currentPage === 1 }">
                <a class="page-link cursor-pointer" @click="prev()">Previous</a>
            </li>
            <li class="page-item" v-for="i in totalPages" :key="i" 
                :class="{ active: i === currentPage }">
                <a class="page-link cursor-pointer" @click="currentPage = i">{{ i }}</a>
            </li>
            <li class="page-item" :class="{ disabled: currentPage === totalPages }">
                <a class="page-link cursor-pointer" @click="next()">Next</a>
            </li>
        </ul>
    </Card1>
</template>

<style scoped>
.cursor-pointer {
    cursor: pointer;
}

.nav-tabs .nav-link {
    cursor: pointer;
}

.nav-tabs .nav-link.active {
    color: #7A70BA;
    border-bottom: 2px solid #7A70BA;
}
</style>

<script lang="ts" setup>
import { ref, defineAsyncComponent, onMounted, watch, computed } from 'vue'
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
const selectedBrand = ref<string>("")

// Computed properties for filtering and pagination
const uniqueBrands = computed(() => {
    const brands = [...new Set(allData.value.map(record => record.brand_name))]
    if (!selectedBrand.value && brands.length > 0) {
        selectedBrand.value = brands[0]
    }
    return brands
})

const filteredRows = computed(() => {
    return allData.value
        .filter(row => row.brand_name === selectedBrand.value)
        .filter(row => 
            filterQuery.value ? 
                row.station_name.toLowerCase().includes(filterQuery.value.toLowerCase()) ||
                row.sensor_type.toLowerCase().includes(filterQuery.value.toLowerCase())
            : true
        )
})

const totalPages = computed(() => 
    Math.ceil(filteredRows.value.length / elementsPerPage.value)
)

const paginatedRows = computed(() => {
    const start = (currentPage.value - 1) * elementsPerPage.value
    const end = start + elementsPerPage.value
    return filteredRows.value.slice(start, end)
})

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

        // Group measurements by brand and sensor type
        const highestMeasurements = new Map<string, HighestRecord>();

        measurementsResponse.data.forEach((measurement: Measurement) => {
            const station = stationsMap.get(measurement.station);
            const sensor = sensorsMap.get(measurement.sensor);
            const key = `${station?.brand_name}-${sensor?.type}`;

            if (!highestMeasurements.has(key) || 
                measurement.value > highestMeasurements.get(key)!.value) {
                highestMeasurements.set(key, {
                    station_name: station?.name || 'Unknown Station',
                    brand_name: station?.brand_name || 'Unknown Brand',
                    date: measurement.date,
                    time: measurement.time,
                    value: measurement.value,
                    sensor_type: sensor?.type || 'Unknown Sensor',
                    sensor_unit: sensor?.unit || 'N/A'
                });
            }
        });

        allData.value = Array.from(highestMeasurements.values())
            .sort((a, b) => b.value - a.value);

    } catch (error) {
        console.error('Error fetching data:', error);
        allData.value = [];
    }
};

watch([filterQuery, selectedBrand], () => {
    currentPage.value = 1;
});

const next = () => {
    if (currentPage.value < totalPages.value) currentPage.value++;
};

const prev = () => {
    if (currentPage.value > 1) currentPage.value--;
};

onMounted(() => {
    fetchHighestRecords();
});
</script>