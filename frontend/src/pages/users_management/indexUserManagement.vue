<template>
    <div class="container-fluid">
        <div class="row">
            <div class="d-flex justify-content-end mb-3">
                    <router-link class="btn btn-primary" to="users_management/createuser">
                        <i data-feather="plus-square"></i> Create New User
                    </router-link>
                </div>
            <Card3 colClass="col-sm-12" title="Users Management Overview" headerTitle="true" cardhaderClass="title-header"
                text="true" :desc="desc" :btnclass="'btn-primary'" >
                <SupportTable />
            </Card3>
        </div>
    </div>
</template>

<script lang="ts" setup>
import { ref, defineAsyncComponent } from 'vue';

const Card3 = defineAsyncComponent(() => import("@/components/common/card/CardData3.vue"))
const SupportTable = defineAsyncComponent(() => import("@/components/theme/users_management/UserMTable.vue"))

let desc = ref<string>("List Of User Accounts");
</script>
