<template>
    <Card3 colClass="col-xl-4" titleClass="mb-0" pre="true" preClass="f-m-light mt-1" headerTitle="true"
        title="Centered modal" :desc="desc">
        <button class="btn btn-success" type="button" data-bs-toggle="modal"
            data-bs-target="#exampleModalCenter1">Vertically centered</button>
        <div class="modal fade" id="exampleModalCenter1" tabindex="-1" role="dialog" aria-labelledby="exampleModalCenter1"
            aria-hidden="true">
            <div class="modal-dialog modal-dialog-centered" role="document">
                <div class="modal-content">
                    <div class="modal-body">
                        <div class="modal-toggle-wrapper">
                            <ul class="modal-img">
                                <li> <img src="@/assets/images/gif/danger.gif" alt="error"></li>
                            </ul>
                            <h4 class="text-center pb-2">Ohh! Something went wrong!</h4>
                            <p class="text-center">Attackers on malicious activity may trick you into doing something
                                dangrous like installing software or revealing your personal informations.</p>
                            <button class="btn btn-secondary d-flex m-auto" type="button"
                                data-bs-dismiss="modal">Close</button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </Card3>
</template>
<script lang="ts" setup>
import { ref, defineAsyncComponent } from 'vue'
import { badges } from "@/core/data/uikits"
import { getImages } from "@/composables/common/getImages"
const Card3 = defineAsyncComponent(() => import("@/components/common/card/CardData3.vue"))
let desc = ref<string>("Use the <code>.modal-dialog-centered </code>through centered modal. and set <code>data-bs-target </code>.")
</script>