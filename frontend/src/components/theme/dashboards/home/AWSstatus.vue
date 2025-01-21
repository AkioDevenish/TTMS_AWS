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
                        'bg-light-primary font-primary': station.status === 'Online',
                        'bg-light-danger font-danger': station.status === 'Offline',
                        'bg-light-warning font-warning': station.status === 'Maintenance'
                    }"
                >
                    {{ station.id }} {{ station.name }}
                </button>
            </div>
            <div class="ratting-button">
                <div class="d-flex align-items-center gap-2 mb-2">
                    <div class="flex-shrink-0">
                        <p class="f-w-500">{{ stationStatus.online }}</p>
                    </div>
                    <div class="flex-grow-1"><span class="f-w-500">Online Stations</span></div>
                </div>
                <div class="d-flex align-items-center gap-2 mb-2">
                    <div class="flex-shrink-0">
                        <p class="f-w-500">{{ stationStatus.offline }}</p>
                    </div>
                    <div class="flex-grow-1"><span class="f-w-500">Offline Stations</span></div>
                </div>
                <div class="d-flex align-items-center gap-2 mb-2">
                    <div class="flex-shrink-0">
                        <p class="f-w-500">{{ stationStatus.maintenance }}</p>
                    </div>
                    <div class="flex-grow-1"><span class="f-w-500">Under Maintenance</span></div>
                </div>
            </div>
            <h5 class="f-w-500 pb-2">Network Uptime: {{ stationStatus.uptime }}%</h5>
            <div class="progress progress-striped-primary">
                <div class="progress-bar" role="progressbar" 
                    :style="{ width: stationStatus.uptime + '%' }" 
                    :aria-valuenow="stationStatus.uptime" 
                    aria-valuemin="0"
                    aria-valuemax="100">
                </div>
            </div>
        </div>
    </Card1>
</template>

<script lang="ts" setup>
import { defineAsyncComponent, onMounted } from 'vue'
import { useAWSStations } from '@/composables/useAWSStations'

const Card1 = defineAsyncComponent(() => import("@/components/common/card/CardData1.vue"))
const { stations, stationStatus, fetchStations } = useAWSStations()

onMounted(fetchStations)
</script>