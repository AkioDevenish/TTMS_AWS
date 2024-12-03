<template>
    <Card3 colClass="col-sm-12 col-md-6" pre="true" preClass="f-m-light mt-1" headerTitle="true"
        title="Scrollable Dropdown Menu" :desc="desc">
        <div id="scrollable-dropdown-menu">
            <form class="theme-form">
                <div>
                    <vue3-simple-typeahead :items="scroll" class="form-control typeahead form-control" @onInput="onInput"
                        @onBlur="onBlur" placeholder="Countries" :minInputLength="options.minInputLength" />
                </div>
            </form>
        </div>
    </Card3>
</template>
<script lang="ts" setup>
import { ref, defineAsyncComponent } from 'vue'
import { options, scroll, onInput, onBlur } from "@/composables/common/typeaheadview"
const Card3 = defineAsyncComponent(() => import("@/components/common/card/CardData3.vue"))
let desc = ref<string>("Dataset shows in scrollable dropdown menu.")
</script>