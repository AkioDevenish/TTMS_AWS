<template>
    <Card3 colClass="col-xxl-3 col-lg-4 col-sm-6 col-12" cardbodyClass=" btn-showcase" pre="true" preClass="f-m-light mt-1"
        headerTitle="true" title="Basic Example" :desc="desc">
        <button class="btn btn-primary sweet-1" type="button" @click="basicAlert()">Click it!</button>
    </Card3>
</template>
<script lang="ts" setup>
import Swal from 'sweetalert2'
import { defineAsyncComponent, ref } from 'vue'
const Card3 = defineAsyncComponent(() => import("@/components/common/card/CardData3.vue"))
let desc = ref<string>("Print the basic message.")
function basicAlert() {
    Swal.fire({
        confirmButtonColor: 'var(--theme-default)',
        title: "Welcome! to the Mofi theme",
    });
}
</script>