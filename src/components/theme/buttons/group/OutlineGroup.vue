<template>
    <Card3 colClass="col-12" cardbodyClass="btn-group-showcase" headerTitle="true" title="Outline Edges button">
        <div class="row">
            <div class="col-xxl-4 col-md-6 col-sm-12" v-for="(item, index) in common" :key="index">
                <div class="btn-group btn-group-pill" role="group" aria-label="Basic example">
                    <button :class="'btn btn-outline-' + item.classes" type="button">Left</button>
                    <button :class="'btn btn-outline-' + item.classes" type="button">Middle</button>
                    <button :class="'btn btn-outline-' + item.classes" type="button">Right</button>
                </div>
            </div>

        </div>
    </Card3>

    <Card3 colClass="col-12" cardbodyClass="btn-group-showcase" headerTitle="true" title="Outline flat button">
        <div class="row">
            <div class="col-xxl-4 col-md-6 col-sm-12" v-for="(item, index) in common" :key="index">
                <div class="btn-group btn-group-square" role="group" aria-label="Basic example">
                    <button :class="'btn btn-outline-' + item.classes" type="button">Left</button>
                    <button :class="'btn btn-outline-' + item.classes" type="button">Middle</button>
                    <button :class="'btn btn-outline-' + item.classes" type="button">Right</button>
                </div>
            </div>

        </div>
    </Card3>

    <Card3 colClass="col-12" cardbodyClass="btn-group-showcase" headerTitle="true" title="Radio button group" :desc="desc"
        text="true">
        <div class="row">
            <div class="col-xxl-4 col-md-6 col-sm-12" v-for="(item, index) in radioButtonData" :key="index">
                <div class="btn-radio">
                    <div class="btn-group" data-bs-toggle="buttons">
                        <div class="btn " :class="'btn-' + items.classes" v-for="(items, index) in item.options"
                            :key="index">
                            <div class="radio " :class="'radio-' + items.classes">
                                <input :id="items.id" type="radio" name="radio1" :value="items.value"
                                    :checked="items.checked">
                                <label :for="items.id">{{ items.label }}</label>
                            </div>
                        </div>

                    </div>
                </div>
            </div>
        </div>
    </Card3>

    <Card3 colClass="col-12" cardbodyClass="btn-group-showcase" headerTitle="true" title="Check Box button group"
        :desc="desc1" text="true">
        <div class="row">
            <div class="col-xl-6 col-sm-12" v-for="(item, index) in checkButtonData" :key="index">
                <div class="btn-group btn-option" data-bs-toggle="buttons">
                    <div class="btn " :class="'btn-' + items.classes" v-for="(items, index) in item.options" :key="index">
                        <div class="checkbox " :class="'checkbox-' + items.classes">
                            <input :id="items.id" type="checkbox">
                            <label :for="items.id">{{ items.label }}</label>
                        </div>
                    </div>

                </div>
            </div>
        </div>
    </Card3>
</template>
<script lang="ts" setup>
import { ref, defineAsyncComponent } from 'vue'
import { basic, flat, common, radioButtonData, checkButtonData} from "@/core/data/buttons"
import { getImages } from "@/composables/common/getImages"
const Card3 = defineAsyncComponent(() => import("@/components/common/card/CardData3.vue"))
let desc = ref<string>("Add <code>.active</code> for active state and<code>.disabled</code> class or <code>disabled='disabled'</code> attribute")
let desc1 = ref<string>("Add <code>.active</code> for active state and <code>.disabled</code> class or <code>disabled='disabled'</code> attribute")
</script>