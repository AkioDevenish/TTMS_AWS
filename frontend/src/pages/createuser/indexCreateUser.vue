<template>
    .
    <div class="container-fluid">
        <div class="row">
            <Card3 colClass="col-sm-12">
                <NewUser />
            </Card3>
        </div>
    </div>
</template>
<script lang="ts" setup>
import { ref, defineAsyncComponent } from 'vue'
const NewUser = defineAsyncComponent(() => import("@/components/theme/users_management/createuser/NewUser.vue"))
const Card3 = defineAsyncComponent(() => import("@/components/common/card/CardData3.vue"))
</script>