<template>
    <Card3 colClass="col-xxl-4 col-md-6" cardhaderClass="rating-header" pre="true" preClass="f-m-light mt-1"
        headerTitle="true" title="Movie Rating Bar" :desc="desc">
        <div class="rating-container">
            <rate :length="5" :value="2" :ratedesc="['Very bad', 'bad', 'Normal', 'Good', 'Very good']" />
        </div>
    </Card3>
</template>
<script lang="ts" setup>
import { defineAsyncComponent, ref } from 'vue'
const Card3 = defineAsyncComponent(() => import("@/components/common/card/CardData3.vue"))
let desc = ref<string>("Movie rating is displayed using <code>#u-rating-movie</code> id using javascript.")
</script>