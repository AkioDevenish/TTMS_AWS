<template>
    <Card3 colClass="col-12" pre="true" preClass="f-m-light mt-1" headerTitle="true" title="Custom checkbox " :desc="desc">
        <div class="row g-3">
            <div class="col-xl-4 col-sm-6">
                <div class="card-wrapper border rounded-3 h-100 checkbox-checked">
                    <h6 class="sub-title">Bordered Checkbox </h6>
                    <div class="form-check checkbox  mb-0" :class="item.class" v-for="(item, index) in borderedcheckbox"
                        :key="index">
                        <input class="form-check-input" :id="item.ids" type="checkbox">
                        <label class="form-check-label" :for="item.ids">{{ item.title }}</label>
                    </div>
                </div>
            </div>
            <div class="col-xl-4 col-sm-12 order-xl-0 order-sm-1">
                <div class="card-wrapper border rounded-3 h-100 checkbox-checked">
                    <h6 class="sub-title">Icon Checkbox </h6>
                    <div class="form-check checkbox checkbox-primary ps-0 main-icon-checkbox">
                        <ul class="checkbox-wrapper">
                            <li v-for="(item, index) in iconcheckbox" :key="index">
                                <input class="form-check-input checkbox-shadow" :id="item.ids" type="checkbox">
                                <label class="form-check-label" :for="item.ids"><i class="fa "
                                        :class="item.icon"></i><span>{{ item.title }}</span></label>
                            </li>
                        </ul>
                    </div>
                </div>
            </div>
            <div class="col-xl-4 col-sm-6">
                <div class="card-wrapper border rounded-3 h-100 checkbox-checked">
                    <h6 class="sub-title">Filled Checkbox </h6>
                    <div class="form-check checkbox " :class="item.class" v-for="(item, index) in filledCheckbox"
                        :key="index">
                        <input class="form-check-input" :id="item.ids" type="checkbox">
                        <label class="form-check-label" :for="item.ids">{{ item.title }} </label>
                    </div>
                </div>
            </div>
        </div>
    </Card3>
</template>
<script lang="ts" setup>
import { ref, defineAsyncComponent } from 'vue'
import { borderedcheckbox, iconcheckbox, filledCheckbox } from "@/core/data/forms"
const Card3 = defineAsyncComponent(() => import("@/components/common/card/CardData3.vue"))
let desc = ref<string>("Use the <code>.form-check-input </code>and <code>.form-check-label </code>for checkbox. And filled checkbox used <code>.checkbox-dashed-*</code> and bordered checkbox used <code>.checkbox-*</code>.")
</script>