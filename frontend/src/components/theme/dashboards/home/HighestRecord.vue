<template>
    <Card1 colClass="col-xl-12 col-lg-12 col-md-12 order-3" headerTitle="true" title="Highest Records"
        cardhaderClass="card-no-border" cardbodyClass="projects px-0 pt-1">
        
        <!-- Brand Tabs -->
        <ul class="nav nav-tabs border-tab nav-primary mb-3" role="tablist">
            <li class="nav-item" v-for="brand in uniqueBrands" :key="brand">
                <a class="nav-link" :class="{ active: selectedBrand === brand }" 
                   @click="selectBrand(brand)">
                    {{ brand }}
                </a>
            </li>
        </ul>

        <!-- Loading State -->
        <div v-if="isLoading" class="text-center py-5">
            <div class="spinner-border text-primary" role="status">
                <span class="visually-hidden">Loading...</span>
            </div>
        </div>

        <!-- No Data State -->
        <div v-else-if="!hasData" class="text-center py-5">
            <div class="empty-state">
                <VueFeather type="alert-circle" size="48" class="text-muted mb-3" />
                <h5>No Data Available</h5>
                <p class="text-muted">No highest records found for the selected brand.</p>
            </div>
        </div>

        <!-- Data Table -->
        <div v-else class="table-responsive theme-scrollbar">
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
        <ul class="pagination mx-2 mt-2 justify-content-end" v-if="totalPages > 1">
            <li class="page-item" :class="{ disabled: currentPage === 1 || isLoading }">
                <a class="page-link cursor-pointer" @click="prev()">Previous</a>
            </li>
            <li class="page-item" v-for="i in totalPages" :key="i" 
                :class="{ active: i === currentPage }">
                <a class="page-link cursor-pointer" @click="setPage(i)">{{ i }}</a>
            </li>
            <li class="page-item" :class="{ disabled: currentPage === totalPages || isLoading }">
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
import { defineAsyncComponent, computed, ref, onMounted } from 'vue';
import { useHighestRecordsStore, type HighestRecord } from '@/store/highestRecords';
import VueFeather from 'vue-feather';

const Card1 = defineAsyncComponent(() => import("@/components/common/card/CardData1.vue"));
const store = useHighestRecordsStore();

const isLoading = computed(() => store.isLoading);
const allData = computed(() => store.records);
const currentPage = computed(() => store.currentPage);
const totalPages = computed(() => store.totalPages);
const selectedBrand = computed(() => store.selectedBrand);
const uniqueBrands = computed(() => store.availableBrands);
const filterQuery = ref('');

const hasData = computed(() => allData.value && allData.value.length > 0);

const filteredRows = computed(() => {
    return allData.value.filter((row: HighestRecord) =>
        filterQuery.value ?
            row.station_name.toLowerCase().includes(filterQuery.value.toLowerCase()) ||
            row.sensor_type.toLowerCase().includes(filterQuery.value.toLowerCase())
            : true
    );
});

const elementsPerPage = 10;
const paginatedRows = computed(() => {
    const start = (currentPage.value - 1) * elementsPerPage;
    const end = start + elementsPerPage;
    return filteredRows.value.slice(start, end) as HighestRecord[];
});

const formatDate = (date: string) => {
    return new Date(date).toLocaleDateString('en-US', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit'
    });
};

const setPage = (page: number) => {
    store.setPage(page);
};

const next = () => {
    if (currentPage.value < totalPages.value) {
        setPage(currentPage.value + 1);
    }
};

const prev = () => {
    if (currentPage.value > 1) {
        setPage(currentPage.value - 1);
    }
};

const selectBrand = (brand: string) => {
    console.log('Component: selectBrand called with', brand);
    store.setBrand(brand);
};

onMounted(() => {
    console.log('Component: onMounted, fetching highest records');
    store.fetchHighestRecords();
});
</script>