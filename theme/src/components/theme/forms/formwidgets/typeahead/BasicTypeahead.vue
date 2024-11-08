<template>
    <Card3 colClass="col-sm-12 col-md-6" pre="true" preClass="f-m-light mt-1" headerTitle="true" title="Basic typeahead"
        :desc="desc">
        <div id="the-basics">
            <form class="theme-form">
                <div>
                    <vue3-simple-typeahead :items="list" class=" typeahead form-control" :placeholder="options.placeholder"
                        @onInput="onInput" @onBlur="onBlur" :minInputLength="options.minInputLength" />
                </div>
            </form>
        </div>
    </Card3>
</template>
<script lang="ts" setup>
import { ref, defineAsyncComponent } from 'vue'
import { options, list, onInput, onBlur } from "@/composables/common/typeaheadview"
const Card3 = defineAsyncComponent(() => import("@/components/common/card/CardData3.vue"))
let desc = ref<string>("This is the simple demo for Typeahead.")
</script>