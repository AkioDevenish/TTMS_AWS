<template>
    <Card3 colClass="col-xxl-3 col-lg-4 col-sm-6 col-12" cardheaderClass=" height-equal" cardbodyClass=" btn-showcase"
        pre="true" preClass="f-m-light mt-1" headerTitle="true" title="Questions Alert" :desc="desc">
        <button class="btn btn-primary sweet-11" type="button" @click="questionsAlert()">Questions state</button>
    </Card3>
</template>
<script lang="ts" setup>
import Swal from 'sweetalert2'
import { defineAsyncComponent, ref } from 'vue'
const Card3 = defineAsyncComponent(() => import("@/components/common/card/CardData3.vue"))
let desc = ref<string>("Print the questionary and give answers.")
function questionsAlert() {
    Swal.fire({
        text: 'Are you sure you want to do this?',
        showCancelButton: true,
        confirmButtonText: 'Aww yiss!',
        confirmButtonColor: 'var(--theme-default)',
        cancelButtonText: 'Oh noez!',
        cancelButtonColor: '#efefef',
        reverseButtons: true
    });
}
</script>