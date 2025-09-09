<template>
    <div class="container-fluid">
        <div class="row">

            <Card3 colClass="col-sm-12" titleClass="m-b-0" headerTitle="true" title="Whether Icons With Animations">
                <WhetherIcons />
            </Card3>
        </div>

    </div>
</template>
<script lang="ts" setup>
import { ref, defineAsyncComponent } from 'vue'
const Card3 = defineAsyncComponent(() => import("@/components/common/card/CardData3.vue"))
const WhetherIcons = defineAsyncComponent(() => import("@/components/theme/icons/whether/WhetherIcons.vue"))
</script>