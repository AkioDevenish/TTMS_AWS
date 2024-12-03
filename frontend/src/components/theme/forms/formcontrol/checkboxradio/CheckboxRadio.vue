<template>
    <Card3 colClass="col-xl-6" pre="true" cardClass="height-equal" preClass="f-m-light mt-1" headerTitle="true"
        title="Basic radio and checkbox" :desc="desc">
        <div class="row g-3">
            <div class="col-md-12">
                <div class="card-wrapper border rounded-3 checkbox-checked">
                    <h6 class="sub-title">Simple Checkbox</h6>
                    <div class="form-check-size">
                        <div class="form-check form-check-inline checkbox checkbox-dark mb-0"
                            v-for="(item, index) in checkbox" :key="index">
                            <input class="form-check-input" :id="item.id" type="checkbox" :checked="item.checked">
                            <label class="form-check-label" :for="item.id">{{ item.label }}</label>
                        </div>

                    </div>
                </div>
            </div>
            <div class="col-md-12">
                <div class="card-wrapper border rounded-3 checkbox-checked">
                    <h6 class="sub-title">Simple Radios</h6>
                    <div class="form-check-size">
                        <div class="form-check form-check-inline radio radio-primary" v-for="(item, index) in radio"
                            :key="index">
                            <input class="form-check-input" :id="item.id" type="radio" name="radio5" value="option5"
                                :checked="item.checked">
                            <label class="form-check-label mb-0" :for="item.id">{{ item.label }}</label>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </Card3>
</template>
<script lang="ts" setup>
import { ref, defineAsyncComponent } from 'vue'
import { checkbox, radio } from "@/core/data/forms"
const Card3 = defineAsyncComponent(() => import("@/components/common/card/CardData3.vue"))
let desc = ref<string>(" Use the <code>.form-check-inline </code>through display inline.")
</script>