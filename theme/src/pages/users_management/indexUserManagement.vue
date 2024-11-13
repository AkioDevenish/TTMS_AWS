<template>
    <div class="container-fluid">
        <div class="row">
            <Card3 colClass="col-sm-12 " title="Users Management Overview" headerTitle="true" cardhaderClass="title-header"
                text="true" :desc="desc">
                <SupportTable />
            </Card3>
        </div>
    </div>
</template>
<script lang="ts" setup>
import { ref, defineAsyncComponent } from 'vue';
const Card3 = defineAsyncComponent(() => import("@/components/common/card/CardData3.vue"))
const SupportTable = defineAsyncComponent(() => import("@/components/theme/users_management/UserMTable.vue"))
let desc = ref<string>("List Of User Accounts ")
</script>