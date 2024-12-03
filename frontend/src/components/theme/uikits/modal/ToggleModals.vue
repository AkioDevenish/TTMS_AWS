<template>
    <Card3 colClass="col-xl-4" titleClass="mb-0" pre="true" preClass="f-m-light mt-1" headerTitle="true"
        title="Toggle between modals" :desc="desc">
        <div class="modal fade" id="exampleModalToggle" aria-hidden="true" aria-labelledby="exampleModalToggle"
            tabindex="-1">
            <div class="modal-dialog modal-dialog-centered">
                <div class="modal-content">
                    <div class="modal-body">
                        <div class="modal-toggle-wrapper">
                            <ul class="modal-img">
                                <li><img src="@/assets/images/gif/whatapp.gif" alt="whatsapp"></li>
                                <li> <img src="@/assets/images/gif/instagram.gif" alt="instagram"></li>
                                <li> <img src="@/assets/images/gif/facebook.gif" alt="facebook"></li>
                            </ul>
                            <h6>Remove your complete account from your phone or tablet to sign out of the Gmail app.</h6>
                            <button class="btn btn-dark rounded-pill w-100 mt-4" data-bs-target="#exampleModalToggle2"
                                data-bs-toggle="modal">Connect new account</button>
                            <button class="btn rounded-pill w-100 pb-0 dark-toggle-btn" type="button"
                                data-bs-dismiss="modal">Cancel</button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div class="modal fade" id="exampleModalToggle2" aria-hidden="true" aria-labelledby="exampleModalToggle2"
            tabindex="-1">
            <div class="modal-dialog modal-dialog-centered">
                <div class="modal-content">
                    <div class="modal-body">
                        <div class="modal-toggle-wrapper">
                            <ul class="modal-img">
                                <li> <img src="@/assets/images/gif/logout.gif" alt="logout"></li>
                            </ul>
                            <h4 class="pt-3 text-center">Already leaving??</h4>
                            <p class="text-center">Are you sure want to logout this dashboard?</p><span
                                class="d-block text-center mb-4"> Not a member?<router-link
                                    to="/dashboards/dashboard_project" class="ms-1">Register</router-link></span>
                            <button class="btn btn-dark d-flex m-auto" type="button" data-bs-dismiss="modal">Yes, Log
                                out</button>
                        </div>
                    </div>
                </div>
            </div>
        </div><a class="btn btn-dark" data-bs-toggle="modal" href="#exampleModalToggle" role="button"
            data-bs-dismiss="modal">Open first modal</a>
    </Card3>
</template>
<script lang="ts" setup>
import { ref, defineAsyncComponent } from 'vue'
import { badges } from "@/core/data/uikits"
import { getImages } from "@/composables/common/getImages"
const Card3 = defineAsyncComponent(() => import("@/components/common/card/CardData3.vue"))
let desc = ref<string>(" Toggle between multiple modals with some clever placement of the <code>data-bs-target </code>and <code>data-bs-toggle</code> attributes.")
</script>