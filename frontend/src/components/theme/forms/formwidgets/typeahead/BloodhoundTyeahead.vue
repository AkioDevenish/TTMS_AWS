<template>
    <Card3 colClass="col-sm-12 col-md-6" pre="true" preClass="f-m-light mt-1" headerTitle="true"
        title="Bloodhound (Suggestion Engine)" :desc="desc">
        <div id="bloodhound">
            <form class="theme-form">
                <div>
                    <vue3-simple-typeahead :items="list" class="form-control typeahead form-control"
                        :placeholder="options.placeholder" @onInput="onInput" @onBlur="onBlur"
                        :minInputLength="options.minInputLength" />
                </div>
            </form>
        </div>
    </Card3>
</template>
<script lang="ts" setup>
import { ref, defineAsyncComponent } from 'vue'
import { options, list, onInput, onBlur } from "@/composables/common/typeaheadview"
const Card3 = defineAsyncComponent(() => import("@/components/common/card/CardData3.vue"))
let desc = ref<string>("Bloodhound offers advanced functionalities such as prefetching and backfilling with remote data.")
</script>