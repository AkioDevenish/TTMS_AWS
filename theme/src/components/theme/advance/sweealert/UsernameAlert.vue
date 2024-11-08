<template>
    <Card3 colClass="col-xxl-3 col-lg-4 col-sm-6 col-12" cardheaderClass=" height-equal" cardbodyClass=" btn-showcase"
        pre="true" preClass="f-m-light mt-1" headerTitle="true" title="Username Alert" :desc="desc">
        <button class="btn btn-secondary sweet-13" type="button" @click="usernameAlert()">Username</button>
    </Card3>
</template>
<script lang="ts" setup>
import Swal from 'sweetalert2'
import { defineAsyncComponent, ref } from 'vue'
const Card3 = defineAsyncComponent(() => import("@/components/common/card/CardData3.vue"))
let desc = ref<string>("Print the basic sweet-alert")
function usernameAlert() {
    Swal.fire({
        text: 'Please! Submit Your Username :',
        input: 'text',
        confirmButtonColor: 'var(--theme-default)',
    }).then((result) => {
        if (result.value) {
            Swal.fire({
                text: 'Your name is :' + result.value,
                confirmButtonColor: 'var(--theme-default)',
            });
        } else {
            Swal.fire({
                text: 'Your name is :' + result.value,
                confirmButtonColor: 'var(--theme-default)',
            });
        }
    });
}
</script>