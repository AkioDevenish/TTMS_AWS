<template>
    <Card3 colClass="col-xl-4" titleClass="mb-0" pre="true" preClass="f-m-light mt-1" headerTitle="true"
        title="Static Backdrop Modal" :desc="desc">
        <button class="btn btn-primary" type="button" data-bs-toggle="modal" data-bs-target="#staticBackdrop">Static
            backdrop modal</button>

        <div class="modal fade" id="staticBackdrop" data-bs-backdrop="static" data-bs-keyboard="false" tabindex="-1"
            aria-labelledby="staticBackdrop" aria-hidden="true">
            <div class="modal-dialog">
                <div class="modal-content dark-sign-up">
                    <div class="modal-body social-profile text-start">
                        <div class="modal-toggle-wrapper">
                            <h4 class="text-dark">Mofi Login</h4>
                            <p>
                                Fill in your information below to continue.</p>
                            <form class="row g-3">
                                <div class="col-md-12">
                                    <label class="form-label" for="inputEmail4">Email</label>
                                    <input class="form-control" id="inputEmail4" type="email"
                                        placeholder="Enter Your Email">
                                </div>
                                <div class="col-md-12">
                                    <label class="form-label" for="inputPassword4">Password</label>
                                    <input class="form-control" id="inputPassword4" type="password"
                                        placeholder="Enter Your Password">
                                </div>
                                <div class="col-12">
                                    <div class="form-check">
                                        <input class="form-check-input" id="gridCheck" type="checkbox">
                                        <label class="form-check-label d-block mb-0" for="gridCheck">Check me out</label>
                                    </div>
                                </div>
                                <div class="col-12">
                                    <button class="btn btn-primary" type="submit" data-bs-dismiss="modal">Sign in </button>
                                </div>
                            </form>
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
let desc = ref<string>(" When backdrop is set to static, the modal will not close when clicking outside of it. Click the button below to try it.")
</script>