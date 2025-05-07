<template>
    <Card1 colClass="col-xl-6 col-lg-6 col-md-6 order-5" 
        dropdown="true" headerTitle="true" title="Total Stations"
        cardhaderClass="card-no-border pb-0" cardbodyClass="total-project">

        <h5 class="f-w-500">Currently Active
            <span class="px-2 f-w-500 font-primary">{{ stationStats.online }} Stations</span>
        </h5>
        <div id="total-project">
            <apexchart type="bar" height="220" :options="chartOptions" :series="series">
            </apexchart>
        </div>
        <ul>
            <li class="d-flex align-items-center gap-2" v-for="(item, index) in statusItems" :key="index">
                <span :class="item.bgclass"></span>
                <p>{{ item.title }} ({{ item.count }})</p>
            </li>
        </ul>
    </Card1>
</template>

<script lang="ts" setup>
import { ref, defineAsyncComponent, onMounted, computed } from 'vue'
import Card1 from '@/components/common/card/CardData1.vue'
import { useAWSStationsStore } from '@/store/awsStations'

const awsStationsStore = useAWSStationsStore()

const stationStats = computed(() => {
    const total = awsStationsStore.stations.length
    const offline = awsStationsStore.stations.filter(s => s.status === 'Offline').length
    const maintenance = awsStationsStore.stations.filter(s => s.status === 'Maintenance').length
    const online = total - offline - maintenance
    
    return {
        total,
        online,
        offline,
        maintenance
    }
})

const statusItems = computed(() => [
    { title: 'Online Stations', count: stationStats.value.online, bgclass: 'bg-primary' },
    { title: 'Offline Stations', count: stationStats.value.offline, bgclass: 'bg-danger' },
    { title: 'Maintenance', count: stationStats.value.maintenance, bgclass: 'bg-warning' }
])

const chartOptions = {
    chart: {
        type: 'bar',
        toolbar: { show: false }
    },
    plotOptions: {
        bar: {
            horizontal: true,
            distributed: true,
            dataLabels: {
                position: 'top'
            }
        }
    },
    colors: ['#7A70BA', '#dc3545', '#ffc107'],
    dataLabels: {
        enabled: true,
        formatter: function(val: number) {
            return val.toString()
        },
        offsetX: 20
    },
    xaxis: {
        categories: ['Online', 'Offline', 'Maintenance'],
        labels: { show: false }
    },
    yaxis: { show: true },
    grid: { show: false }
}

const series = computed(() => [{
    name: 'Stations',
    data: [
        stationStats.value.online,
        stationStats.value.offline,
        stationStats.value.maintenance
    ]
}])
</script>

<style scoped>
.bg-primary { background-color: #7A70BA; }
.bg-danger { background-color: #dc3545; }
.bg-warning { background-color: #ffc107; }

li span {
    width: 10px;
    height: 10px;
    border-radius: 50%;
    display: inline-block;
}

.font-primary {
    color: #7A70BA;
}
</style>