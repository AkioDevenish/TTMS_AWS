<template>
    <Card3 colClass="col-xxl-3 col-lg-4 col-sm-6 col-12" cardheaderClass=" height-equal" cardbodyClass=" btn-showcase"
        pre="true" preClass="f-m-light mt-1" headerTitle="true" title="Info Alert" :desc="desc">
        <button class="btn btn-info sweet-4" type="button" @click="infoAlert()">Informational</button>
    </Card3>
</template>
<script lang="ts" setup>
import Swal from 'sweetalert2'
import { defineAsyncComponent, ref } from 'vue'
const Card3 = defineAsyncComponent(() => import("@/components/common/card/CardData3.vue"))
let desc = ref<string>("Print the informational message.")
function infoAlert() {
    Swal.fire({
        text: ' Click on either the button or outside the modal.',
        confirmButtonColor: 'var(--theme-default)',
    }).then((result) => {
        if (result.value) {
            Swal.fire({
                text: 'Thank you for visit Mofi theme: ' + result.value,
                confirmButtonColor: 'var(--theme-default)',
            });
        } else {
            Swal.fire({
                confirmButtonColor: 'var(--theme-default)',
                text: 'Thank you for visit Mofi theme: ' + result.value
            });
        }
    });
}
</script>