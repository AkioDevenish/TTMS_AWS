<template>
    <Card3 colClass="col-sm-12 col-md-6" pre="true" preClass="f-m-light mt-1" headerTitle="true"
        title="Multiple sections with headers" :desc="desc">
        <div id="multiple-datasets">
            <form class="theme-form">
                <div>
                    <vue3-simple-typeahead :items="multiple" class="form-control typeahead form-control" @onInput="onInput"
                        @onBlur="onBlur" placeholder="NBA and NHL teams" :minInputLength="options.minInputLength" />
                </div>
            </form>
        </div>
    </Card3>
</template>
<script lang="ts" setup>
import { ref, defineAsyncComponent } from 'vue'
import { options, multiple, onInput, onBlur } from "@/composables/common/typeaheadview"
const Card3 = defineAsyncComponent(() => import("@/components/common/card/CardData3.vue"))
let desc = ref<string>("Two datasets that are prefetched, stored, and searched on the client. Highlighting is enabled.")
</script>