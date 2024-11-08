<template>
    <Card3 colClass="col-sm-12 col-md-6" pre="true" preClass="f-m-light mt-1" headerTitle="true" title="Remote typeahead"
        :desc="desc">
        <div id="remote">
            <form class="theme-form">
                <div>
                    <vue3-simple-typeahead :items="remote" class="form-control typeahead form-control" @onInput="onInput"
                        @onBlur="onBlur" placeholder="Choose Option" :minInputLength="options.minInputLength" />
                </div>
            </form>
        </div>
    </Card3>
</template>
<script lang="ts" setup>
import { ref, defineAsyncComponent } from 'vue'
import { options, remote, onInput, onBlur } from "@/composables/common/typeaheadview"
const Card3 = defineAsyncComponent(() => import("@/components/common/card/CardData3.vue"))
let desc = ref<string>("Remote data is only used when the data provided by local and prefetch is insufficient")
</script>