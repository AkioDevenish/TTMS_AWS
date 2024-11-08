<template>
    <Card3 colClass="col-lg-6" pre="true" preClass="f-m-light mt-1" headerTitle="true"  title="Negative Value" :desc="desc">
        <div class="form-group row py-1 my-3">
            <div class="col-md-10">
                <VueSlider v-model="four.value" :data="four.data2" :marks="true" :tooltip="'always'"
                    :tooltip-placement="'top'"></VueSlider>
            </div>
        </div>
    </Card3>
</template>
<script lang="ts" setup>
import VueSlider from 'vue-slider-component'
import 'vue-slider-component/theme/antd.css'
import { ref, defineAsyncComponent } from "vue"
const Card3 = defineAsyncComponent(() => import("@/components/common/card/CardData3.vue"))
let desc = ref<string>(" Use the <code>.range-slider </code> class. and Mofi used Ion range slider.<code>[http://ionden.com/a/plugins/ion.rangeSlider]</code>")
const four = ref({
    value: [-500, 500],
    data2: [-1000, -500, 0, 500, 1000],
})
</script>