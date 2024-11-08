<template>
    <Card3 colClass="col-xxl-4 col-md-6" cardhaderClass="rating-header" pre="true" preClass="f-m-light mt-1"
        headerTitle="true" title="Star Rating" :desc="desc">
        <star-rating :star-size="20" :max-rating="10" :increment="0.01"></star-rating>
    </Card3>
</template>
<script lang="ts" setup>
import StarRating from 'vue-star-rating';
import { ref, defineAsyncComponent } from "vue"
const Card3 = defineAsyncComponent(() => import("@/components/common/card/CardData3.vue"))
let desc = ref<string>("Star Rating is displayed using <code>#u-rating-star </code> id using javascript.")
const rating = ref<string>("0")
</script>