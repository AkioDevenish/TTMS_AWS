<template>
    <Card3 colClass="col-xxl-3 col-lg-4 col-sm-6 col-12" cardheaderClass=" height-equal" cardbodyClass=" btn-showcase"
        pre="true" preClass="f-m-light mt-1" headerTitle="true" title="Title With A Text Under" :desc="desc">
        <button class="btn btn-secondary sweet-2" type="button" @click="textAlert()">Surprise!</button>
    </Card3>
</template>
<script lang="ts" setup>
import Swal from 'sweetalert2'
import { defineAsyncComponent, ref } from 'vue'
const Card3 = defineAsyncComponent(() => import("@/components/common/card/CardData3.vue"))
let desc = ref<string>("Print the title with text.")
function textAlert() {
    Swal.fire({
        confirmButtonColor: 'var(--theme-default)',
        title: "It's Magic!",
        text: 'Thank you for visiting Mofi theme',
    });
}
</script>