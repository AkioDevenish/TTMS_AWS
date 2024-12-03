<template>
    <Card3 colClass="col-12" pre="true" preClass="f-m-light mt-1" headerTitle="true" title="Inline input-types"
        :desc="desc">
        <div class="row g-3">
            <div class="col-md-6 col-xl-4" v-for="(item, index) in Inline" :key="index">
                <div class="card-wrapper border rounded-3 checkbox-checked">
                    <h6 class="sub-title">{{ item.title }}</h6>
                    <div class="form-check-size rtl-input">
                        <div class="form-check form-check-inline" v-for="(items, index) in item.children" :key="index">
                            <input class="form-check-input me-2" :id="items.id" :type="items.type" :value="items.value"
                                :checked="items.checked" :disabled="items.disabled" :name="items.name">
                            <label class="form-check-label" :for="items.id">{{ items.label }}</label>
                        </div>

                    </div>
                </div>
            </div>
        </div>
    </Card3>
</template>
<script lang="ts" setup>
import { ref, defineAsyncComponent } from 'vue'
import { Inline } from "@/core/data/forms"
const Card3 = defineAsyncComponent(() => import("@/components/common/card/CardData3.vue"))
let desc = ref<string>(" Group checkboxes or radios on the same horizontal row by adding <code>.form-check-inline </code>to any<code>.form-check</code>.")
</script>