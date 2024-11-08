<template>
    <Card3 colClass="col-md-12" pre="true" preClass="f-m-light mt-1" headerTitle="true" title="Basic typeahead"
        :desc="desc">
        <div class="row g-3">
            <div :class="item.colclass" v-for="(item, index) in customswitch" :key="index">
                <div class="card-wrapper " :class="item.class">
                    <div :class="item.sizeclass">
                        <div class="form-check form-switch form-check-inline" v-for="(items, index) in item.children"
                            :key="index">
                            <input class="form-check-input  check-size" :class="items.inputclass" type="checkbox"
                                role="switch" :checked="items.checked" :disabled="items.disabled">
                        </div>
                    </div>
                </div>
            </div>

        </div>
    </Card3>
</template>
<script lang="ts" setup>
import { ref, defineAsyncComponent } from 'vue'
import { customswitch } from "@/core/data/forms"
const Card3 = defineAsyncComponent(() => import("@/components/common/card/CardData3.vue"))
let desc = ref<string>("A switch has the markup of a custom checkbox but uses the .form-switch class to render a <code>toggle switch</code>.")
</script>