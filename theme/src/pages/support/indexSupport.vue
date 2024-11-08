<template>
    <div class="container-fluid">
        <div class="row">
            <Card3 colClass="col-sm-12 " title="Support Ticket List" headerTitle="true" cardhaderClass="title-header"
                text="true" :desc="desc">
                <SupportTicket />
                <SupportTable />
            </Card3>
        </div>
    </div>
</template>
<script lang="ts" setup>
import { ref, defineAsyncComponent } from 'vue';
const Card3 = defineAsyncComponent(() => import("@/components/common/card/CardData3.vue"))
const SupportTicket = defineAsyncComponent(() => import("@/components/theme/support/SupportTicket.vue"))
const SupportTable = defineAsyncComponent(() => import("@/components/theme/support/SupportTable.vue"))
let desc = ref<string>("List of ticket opend by customers")
</script>