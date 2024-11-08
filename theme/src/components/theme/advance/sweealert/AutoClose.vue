<template>
    <Card3 colClass="col-xxl-3 col-lg-4 col-sm-6 col-12" cardheaderClass=" height-equal" cardbodyClass=" btn-showcase"
        pre="true" preClass="f-m-light mt-1" headerTitle="true" title="Auto Close Timer" :desc="desc">
        <button class="btn btn-primary sweet-14" type="button" @click="autoAlert()">Timer</button>
    </Card3>
</template>
<script lang="ts" setup>
import Swal from 'sweetalert2'
import { defineAsyncComponent, ref } from 'vue'
const Card3 = defineAsyncComponent(() => import("@/components/common/card/CardData3.vue"))
let desc = ref<string>("A text message with an automatic timer")
function autoAlert() {
    Swal.fire({
        position: 'center',
        title: 'Auto close alert!',
        text: "just a wait!  I will close in 30 second!",
        showConfirmButton: false,
        timer: 4000,
    });
}
</script>