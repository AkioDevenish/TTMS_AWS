<template>
    <Card3 colClass="col-sm-12 col-md-6" pre="true" preClass="f-m-light mt-1" headerTitle="true" title="RTL Support"
        :desc="desc">
        <div id="rtl-support">
            <form class="theme-form">
                <div>
                    <vue3-simple-typeahead :items="list" class="form-control typeahead form-control" dir="rtl"
                        @onInput="onInput" @onBlur="onBlur" placeholder="Countries" :minInputLength="options.minInputLength"
                        :hint="options.hint" />
                </div>
            </form>
        </div>
    </Card3>
</template>
<script lang="ts" setup>
import { ref, defineAsyncComponent } from 'vue'
import { options, onInput, onBlur } from "@/composables/common/typeaheadview"
const Card3 = defineAsyncComponent(() => import("@/components/common/card/CardData3.vue"))
let desc = ref<string>("Dataset shows in Right Side.")
let list = ref<string[]>(["India",
    "USA",
    "Australia",
    "UEA",
    "China"])
</script>