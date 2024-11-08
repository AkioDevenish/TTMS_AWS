<template>
    <Card3 colClass="col-xxl-3 col-lg-4 col-sm-6 col-12" cardheaderClass=" height-equal" cardbodyClass=" btn-showcase"
        pre="true" preClass="f-m-light mt-1" headerTitle="true" title="Pikachu Alert" :desc="desc">
        <button class="btn btn-warning sweet-12" type="button" @click="infoAlert()">Pikachu</button>
    </Card3>
</template>
<script lang="ts" setup>
import Swal from 'sweetalert2'
import { defineAsyncComponent, ref } from 'vue'
const Card3 = defineAsyncComponent(() => import("@/components/common/card/CardData3.vue"))
let desc = ref<string>("atch the pokeball.")
function infoAlert() {
    Swal.fire({
        text: 'A wild Pikachu appeared! What do you want to do?',
        showCancelButton: true,
        showDenyButton: true,
        confirmButtonText: 'Defect',
        confirmButtonColor: 'var(--theme-default)',
        cancelButtonText: 'Run away!',
        denyButtonColor: 'var(--theme-default',
        denyButtonText: `Throw Pokeball!`,
    }).then((result) => {

        if (result.value) {


            Swal.fire({
                icon: 'success',
                title: 'Yeah!',
                text: 'Pikachu was caught!',
                confirmButtonColor: 'var(--theme-default)',
            });
        } else if (result.isDenied) {
            Swal.fire({
                text: 'Got away safely!',
                confirmButtonColor: 'var(--theme-default)',
            })

        } else {
            Swal.fire({
                text: 'Pikachu fainted! You gained 500 XP!',
                confirmButtonColor: 'var(--theme-default)',
            });
        }
    });
}
</script>