<template>
    <Card1 dropdown="true" headerTitle="true" title="Automatic Weather Stations - Status"
        cardhaderClass="card-no-border pb-0" cardbodyClass="designer-card">
        <div>
            <div class="d-flex align-items-center gap-2">
                <div class="flex-shrink-0"><img src="@/assets/images/dashboard-2/user/16.png" alt="user"></div>
                <div class="flex-grow-1">
                    <h5>Trinidad and Tobago Met Services</h5>
                    <p>metfeedback@gov.tt</p>
                </div>
            </div>
            <div class="design-button">
                <button v-for="station in stations" 
                    :key="station.id"
                    class="btn me-1 mb-1"
                    :class="{
                        'bg-light-primary font-primary': station.status !== 'NoData',
                        'bg-light-danger font-danger': station.status === 'NoData'
                    }"
                >
                    {{ station.id }} {{ station.name }}
                </button>
            </div>
            <div class="ratting-button">
                <div class="d-flex align-items-center gap-2 mb-2">
                    <div class="flex-shrink-0">
                        <p class="f-w-500">{{ status.online }}</p>
                    </div>
                    <div class="flex-grow-1"><span class="f-w-500">Active Stations</span></div>
                </div>
                <div class="d-flex align-items-center gap-2 mb-2">
                    <div class="flex-shrink-0">
                        <p class="f-w-500">{{ status.noData }}</p>
                    </div>
                    <div class="flex-grow-1"><span class="f-w-500">Inactive Stations</span></div>
                </div>
            </div>
            <h5 class="f-w-500 pb-2">Network Activity: {{ status.uptime }}%</h5>
            <div class="progress progress-striped-primary">
                <div class="progress-bar" role="progressbar" 
                    :style="{ width: status.uptime + '%' }" 
                    :aria-valuenow="status.uptime" 
                    aria-valuemin="0"
                    aria-valuemax="100">
                </div>
            </div>
        </div>
    </Card1>
</template>

<script lang="ts" setup>
import { defineAsyncComponent, onMounted, computed } from 'vue'
import { useAWSStations } from '@/composables/useAWSStations'
import { getStationStatus } from '@/core/data/aws'

const Card1 = defineAsyncComponent(() => import("@/components/common/card/CardData1.vue"))
const { stations, fetchStations } = useAWSStations()

const status = computed(() => {
    const total = stations.value.length
    const noData = stations.value.filter(s => s.status === 'NoData').length
    const online = total - noData
    
    return {
        total,
        online,
        noData,
        uptime: total ? ((online / total) * 100).toFixed(1) : '0'
    }
})

onMounted(fetchStations)
</script>