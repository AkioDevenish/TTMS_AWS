<template>
    <Card1 colClass="col-xl-12 col-lg-12 col-md-12 order-2" 
        headerTitle="true" 
        title="Station Status"
        cardhaderClass="card-no-border" 
        cardbodyClass="designer-card pt-0">
        <div class="mt-4">
            <div v-if="loading" class="text-center py-5">
                <div class="loading-state">
                    <VueFeather type="loader" size="48" class="text-primary mb-3 spinning" />
                    <h5>Loading Station Data...</h5>
                </div>
            </div>
            <div v-else-if="error" class="text-center py-5">
                <div class="error-state">
                    <VueFeather type="alert-triangle" size="48" class="text-danger mb-3" />
                    <h5>Error Loading Data</h5>
                    <p class="text-muted">{{ error }}</p>
                </div>
            </div>
            <div v-else>
                <div v-if="hasRecentData" class="design-button">
                    <button v-for="station in stations" 
                        :key="station.id"
                        class="btn me-1 mb-1"
                        :class="getStationClass(station)"
                    >
                        {{ station.name }}
                    </button>
                </div>
                <div v-else class="text-center py-5">
                    <div class="empty-state">
                        <VueFeather type="alert-circle" size="48" class="text-muted mb-3" />
                        <h5>No Data Available</h5>
                        <p class="text-muted">Station Health Data is currently not available</p>
                    </div>
                </div>
                <div v-if="hasRecentData">
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
                    <h5 class="f-w-500 pb-2">Station Activity: {{ status.uptime }}%</h5>
                    <div class="progress progress-striped-primary">
                        <div class="progress-bar" role="progressbar" 
                            :style="{ width: status.uptime + '%' }" 
                            :aria-valuenow="status.uptime" 
                            aria-valuemin="0"
                            aria-valuemax="100">
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </Card1>
</template>

<script lang="ts" setup>
import { defineAsyncComponent, onMounted, computed, onUnmounted } from 'vue'
import { useAWSStationsStore } from '@/store/awsStations'
import VueFeather from 'vue-feather'

const Card1 = defineAsyncComponent(() => import("@/components/common/card/CardData1.vue"))
const awsStationsStore = useAWSStationsStore()

const stations = computed(() => awsStationsStore.stations)
const loading = computed(() => awsStationsStore.loading)
const error = computed(() => awsStationsStore.error)

const hasRecentData = computed(() => {
    return stations.value.some((station: any) => {
        if (!station.latestHealth?.created_at) return false
        const lastUpdate = new Date(station.latestHealth.created_at)
        const twentyFourHoursAgo = new Date()
        twentyFourHoursAgo.setHours(twentyFourHoursAgo.getHours() - 24)
        return lastUpdate >= twentyFourHoursAgo
    })
})

const status = computed(() => {
    const total = stations.value.length
    const noData = stations.value.filter((s: any) => {
        if (!s.latestHealth || !s.latestHealth.created_at || s.latestHealth.connectivity_status !== 'Excellent') {
            return true
        }
        const lastUpdate = new Date(s.latestHealth.created_at)
        const twentyFourHoursAgo = new Date()
        twentyFourHoursAgo.setHours(twentyFourHoursAgo.getHours() - 24)
        return lastUpdate < twentyFourHoursAgo
    }).length
    const online = total - noData
    return {
        total,
        online,
        noData,
        uptime: total ? ((online / total) * 100).toFixed(1) : '0'
    }
})

const getStationClass = (station: any) => {
    if (!station.latestHealth?.created_at || !station.latestHealth?.connectivity_status) {
        return 'bg-light-danger font-danger'
    }
    const lastUpdate = new Date(station.latestHealth.created_at)
    const twentyFourHoursAgo = new Date()
    twentyFourHoursAgo.setHours(twentyFourHoursAgo.getHours() - 24)
    if (station.latestHealth.connectivity_status === 'Excellent' && lastUpdate >= twentyFourHoursAgo) {
        return 'bg-light-primary font-primary'
    }
    return 'bg-light-danger font-danger'
}

onMounted(() => {
    awsStationsStore.init()
})
</script>

<style scoped>
.empty-state {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 2rem;
}

.empty-state h5 {
    margin-bottom: 0.5rem;
    color: #495057;
}

.empty-state p {
    color: #6c757d;
}

.progress-striped-primary {
    height: 8px;
    background-color: rgba(var(--bs-primary-rgb), 0.1);
    border-radius: 4px;
}

.progress-bar {
    background-color: var(--bs-primary);
    border-radius: 4px;
    transition: width 0.6s ease;
}

.loading-state {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 2rem;
}

.loading-state h5 {
    margin-bottom: 0.5rem;
    color: #495057;
}

.spinning {
    animation: spin 1s linear infinite;
}

@keyframes spin {
    from { transform: rotate(0deg); }
    to { transform: rotate(360deg); }
}

.error-state {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 2rem;
}

.error-state h5 {
    margin-bottom: 0.5rem;
    color: #dc3545;
}

.error-state p {
    color: #6c757d;
}
</style>