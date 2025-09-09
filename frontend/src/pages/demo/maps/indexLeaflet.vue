<template>
    <div class="container-fluid">
        <div class="row">
            <Card3 colClass="col-xl-6" cardbodyClass="map-z-index" title="Simple Map" headerTitle="true">
                <SimpleMap />
            </Card3>
            <Card3 colClass="col-xl-6" cardbodyClass="map-z-index" title="Multi-language support" headerTitle="true"
                text="true" :desc="desc">
                <MultiLanguage />
            </Card3>
            <Card3 colClass="col-xl-12" cardbodyClass="map-z-index" title="Multi-language support" headerTitle="true"
                text="true" :desc="desc">
                <MultiLanguage2 />
            </Card3>
        </div>
    </div>
</template>
<script lang="ts" setup>
import { ref, defineAsyncComponent } from 'vue';
let Card3 = defineAsyncComponent(() => import("@/components/common/card/CardData3.vue"))
const SimpleMap = defineAsyncComponent(() => import("@/components/theme/maps/SimpleMap.vue"))
const MultiLanguage = defineAsyncComponent(() => import("@/components/theme/maps/MultiLanguage.vue"))
const MultiLanguage2 = defineAsyncComponent(() => import("@/components/theme/maps/MultiLanguage2.vue"))
let desc = ref<string>("Display a map with labels in a foreign language")
</script>