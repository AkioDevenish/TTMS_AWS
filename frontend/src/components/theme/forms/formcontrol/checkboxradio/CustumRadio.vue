<template>
    <Card3 colClass="col-12" pre="true" preClass="f-m-light mt-1" headerTitle="true" title="Custom radio" :desc="desc">
        <div class="row g-3">
            <div class="col-xl-4 col-sm-6">
                <div class="card-wrapper border rounded-3 h-100 checkbox-checked">
                    <h6 class="sub-title">Bordered Radio</h6>
                    <div class="form-check radio " :class="item.class" v-for="(item, index) in borderedradio" :key="index">
                        <input class="form-check-input" :id="item.ids" type="radio" name="radio1" value="option1">
                        <label class="form-check-label" :for="item.ids">{{ item.title }} </label>
                    </div>
                </div>
            </div>
            <div class="col-xl-4 col-sm-12 order-xl-0 order-sm-1">
                <div class="card-wrapper border rounded-3 h-100 checkbox-checked">
                    <h6 class="sub-title">Icons Radio</h6>
                    <div class="form-check radio radio-primary ps-0">
                        <ul class="radio-wrapper">
                            <li v-for="(item, index) in iconsradio" :key="index">
                                <input class="form-check-input" :id="item.ids" type="radio" name="radio2" value="option2">
                                <label class="form-check-label" :for="item.ids"><i class="fa "
                                        :class="item.icon"></i><span>{{ item.title }}</span></label>
                            </li>

                        </ul>
                    </div>
                </div>
            </div>
            <div class="col-xl-4 col-sm-6">
                <div class="card-wrapper border rounded-3 fill-radios h-100 checkbox-checked">
                    <h6 class="sub-title">Filled Radio</h6>
                    <div class="form-check radio " :class="item.class" v-for="(item, index) in filledradio" :key="index">
                        <input class="form-check-input" :id="item.ids" type="radio" name="radio3" value="option1">
                        <label class="form-check-label" :for="item.ids">{{ item.title }}</label>
                    </div>

                </div>

            </div>
        </div>
    </Card3>
</template>
<script lang="ts" setup>
import { ref, defineAsyncComponent } from 'vue'
import { borderedradio, iconsradio, filledradio } from "@/core/data/forms"
const Card3 = defineAsyncComponent(() => import("@/components/common/card/CardData3.vue"))
let desc = ref<string>(" Use the <code>.form-check-input </code>and <code>.form-check-label </code>for radios.")
</script>