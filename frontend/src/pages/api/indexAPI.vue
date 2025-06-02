<template>
    <div class="container-fluid">
        <div class="row">
            <Card3 colClass="col-sm-12 " title="API Accounts Overview" headerTitle="true" cardhaderClass="title-header"
                text="true" :desc="desc">
                <template v-if="isAdmin">
                  <SupportTable />
                </template>
                <template v-else>
                  <div class="alert alert-warning mt-4">You do not have permission to view API key management.</div>
                </template>
            </Card3>
        </div>
    </div>
</template>
<script lang="ts" setup>
import { ref, defineAsyncComponent } from 'vue';
import { useAuthStore } from '@/store/auth';
const Card3 = defineAsyncComponent(() => import("@/components/common/card/CardData3.vue"))
// const SupportTicket = defineAsyncComponent(() => import("@/components/theme/api/SupportTicket.vue"))
const SupportTable = defineAsyncComponent(() => import("@/components/theme/api/SupportTable.vue"))
const authStore = useAuthStore()
const { isAdmin } = authStore
let desc = ref<string>("List of Accounts and API Status Of Customers")
</script>