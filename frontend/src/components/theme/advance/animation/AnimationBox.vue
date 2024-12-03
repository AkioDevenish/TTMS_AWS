<template>
    <Card3 colClass="col-sm-12" pre="true" preClass="f-m-light mt-1" headerTitle="true" title="Modal With Animations"
        :desc="desc">
        <div class="row justify-content-center align-items-center">
            <div class="col-xl-6 col-md-8">
                <div class="animate-img" id="animation-box">
                    <div class="card">
                        <div class="animate-widget">
                            <div><img class="img-fluid" :src="getImages('slider/6.jpg')" alt="Drawing-room"></div>
                            <div class="text-center p-25">
                                <p class="text-muted mb-0"></p>
                                <h4>It&apos;s Magic!!</h4> Select the animation options given below and then click on the
                                launch button.
                                <p></p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="col-xl-6">
                <form class="form-inline theme-form row animated-modal">
                    <div class="mb-3 mb-0 animated-modal-md-mb w-100">
                        <label class="me-3">Entrances</label>
                        <select class="form-select w-75" id="entrance" v-model="enterAnimation">
                            <option v-for="(anim, index) in animationList" :value="anim" :key="index">{{ anim }}
                            </option>
                        </select>
                    </div>
                    <div class="mb-3 mb-0 animated-modal-md-mb w-100">
                        <label class="me-3">Exits</label>
                        <select class="form-select w-75" id="exit" v-model="exitAnimation">

                            <option v-for="(anim, index) in animationList" :value="anim" :key="index">{{ anim }}
                            </option>
                        </select>
                    </div>

                    <div class="mt-2 text-center w-100">
                        <button class="btn btn-primary" type="button" data-bs-toggle="modal" data-bs-target="#myModal"
                            @click.prevent="isActive(enterAnimation)">Launch demo modal</button>
                    </div>
                </form>
            </div>
        </div>
        <Teleport to="body">
            <div class="modal fade modal-popup" @click="close" id="myModal" role="dialog"
                :style="{ marginRight: animate ? '15px' : '0px' }">
                <div id="mod" class="modal-dialog" role="document">
                    <div>
                        <button class="btn-close theme-close" type="button" @click="close"></button>
                        <div class="modal-body">
                            <div class="card">
                                <div class="animate-widget">
                                    <div><img class="img-fluid" :src="getImages('slider/6.jpg')" alt=""></div>
                                    <div class="text-center p-25">
                                        <p class="text-muted mb-0"><strong class="txt-danger">Wow!!!</strong> It's so
                                            beautiful
                                            animations
                                            in Mofi theme...</p>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </Teleport>
    </Card3>
</template>
<script lang="ts" setup>
import { getImages } from "@/composables/common/getImages"
import { animationList, animation, animate, enterAnimation, exitAnimation } from "@/composables/common/animationView"
import { ref, defineAsyncComponent } from 'vue'
const Card3 = defineAsyncComponent(() => import("@/components/common/card/CardData3.vue"))
let desc = ref<string>("Use the different types of fades and animations in modals.")

function isActive(path: boolean) {
    animate.value = path
    document.getElementById("mod").className = `modal-dialog ${path} animated`
}
function close() {

    document.getElementById("mod").className = `modal-dialog ${exitAnimation.value} animated`
}
</script>