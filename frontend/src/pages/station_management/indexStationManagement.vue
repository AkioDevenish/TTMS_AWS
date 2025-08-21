<template>
	<div v-if="isAdmin" class="container-fluid">
		<div class="row">
			<Card3 colClass="col-sm-12" title="Stations Management Overview" headerTitle="true" cardhaderClass="title-header" text="true" :desc="desc" :btnclass="'btn-primary'">
				<template #header>
					<div class="d-flex justify-content-between align-items-center">
						<h5 class="mb-0">Stations Management Overview</h5>
						<button @click="refreshStations" class="btn btn-outline-primary btn-sm" :disabled="stationStore.loading">
							<i class="fa fa-refresh" :class="{ 'fa-spin': stationStore.loading }"></i>
							Refresh
						</button>
					</div>
				</template>
				<StationTable />
			</Card3>
		</div>
	</div>
	<div v-else>
		<h3>Access Denied</h3>
		<p>You don't have permission to access this page.</p>
	</div>
</template>

<script lang="ts" setup>
import { ref, defineAsyncComponent, onMounted } from 'vue';
import { useAuthStore } from '@/store/auth';
import { useStationStore } from '@/store/station';

const Card3 = defineAsyncComponent(() => import("@/components/common/card/CardData3.vue"))
const StationTable = defineAsyncComponent(() => import("@/components/theme/station_management/StationTable.vue"))
const authStore = useAuthStore()
const { isAdmin } = authStore
const stationStore = useStationStore()

let desc = ref<string>("List Of Weather Station Accounts");

const refreshStations = async () => {
	console.log('Manual refresh requested...')
	await stationStore.fetchStations()
}

onMounted(async () => {
	// Force fresh data fetch to avoid stale cache issues
	console.log('Station Management: Fetching fresh station data...')
	await stationStore.fetchStations()
})
</script> 