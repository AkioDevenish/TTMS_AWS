<template>
	<div v-if="isAdmin" class="container-fluid">
		<div class="row">
			<Card3 colClass="col-sm-12" title="Users Management Overview" headerTitle="true" cardhaderClass="title-header" text="true" :desc="desc" :btnclass="'btn-primary'">
				<template #header>
					<div class="d-flex justify-content-between align-items-center">
						<div>
							<h4>Users Management Overview</h4>
							<span v-html="desc"></span>
						</div>
				<router-link class="btn btn-primary" to="/pages/users_management/createuser">
					<i data-feather="plus-square"></i> Create New User
				</router-link>
			</div>
				</template>
				<SupportTable />
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
import { useUserStore } from '@/store/user';

const Card3 = defineAsyncComponent(() => import("@/components/common/card/CardData3.vue"))
const SupportTable = defineAsyncComponent(() => import("@/components/theme/users_management/UserMTable.vue"))
const authStore = useAuthStore()
const { isAdmin } = authStore
const userStore = useUserStore()

// const apiUrl = process.env.VUE_APP_API_URL;
// console.log('API Base URL from users page:', apiUrl);

let desc = ref<string>("List Of User Accounts");

onMounted(async () => {
	await userStore.fetchUsers()
})
</script>