<template>
    <Card3 colClass="col-xxl-3 col-lg-4 col-sm-6 col-12" cardheaderClass=" height-equal" cardbodyClass=" btn-showcase"
        pre="true" preClass="f-m-light mt-1" headerTitle="true" title="Danger Alert" :desc="desc">
        <button class="btn btn-danger sweet-7" type="button" @click="dangerAlert()">Danger mode</button>
    </Card3>
</template>
<script lang="ts" setup>
import Swal from 'sweetalert2'
import { defineAsyncComponent, ref } from 'vue'
const Card3 = defineAsyncComponent(() => import("@/components/common/card/CardData3.vue"))
let desc = ref<string>("Print the danger message.")
function dangerAlert() {
    Swal.fire({
        icon: "error",
        title: "It's danger",
        text: "Something went wrong!",
        confirmButtonColor: 'var(--theme-default)',
    });
}
</script>