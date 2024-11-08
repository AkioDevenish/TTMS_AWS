<template>
    <div class="col-sm-12">
        <div class="card">
            <div class="profile-img-style">
                <div class="row">
                    <div class="col-sm-8">
                        <div class="d-flex"><img class="img-thumbnail rounded-circle me-3" src="@/assets/images/user/7.jpg"
                                alt="Generic placeholder image">
                            <div class="flex-grow-1 align-self-center">
                                <h5 class="mt-0 user-name">JOHAN DIO</h5>
                            </div>
                        </div>
                    </div>
                    <div class="col-sm-4 align-self-center">
                        <div class="float-sm-end"><small>10 Hours ago</small></div>
                    </div>
                </div>
                <hr>
                <p>Spend time outdoors: Find a nearby park, forest, beach, or any natural setting where you can immerse
                    yourself in nature. Take a walk, go hiking, or simply sit and observe the natural surroundings. Practice
                    mindfulness: Engage in mindful activities that help you connect with nature on a deeper level.</p>
                <div class="img-container">
                    <div class="my-gallery" id="aniimated-thumbnials" itemscope>
                        <figure itemprop="associatedMedia" itemscope v-for="(src, index) in img" :key="index"
                            @click="() => showImg(index)"><img class="img-fluid rounded" :src="getImgUrl(src.image)"
                                itemprop="thumbnail" alt="Image description">
                        </figure>
                    </div>
                    <vue-easy-lightbox :index="indexRef" :visible="visible" :imgs="imgs"
                        @hide="handleHide"></vue-easy-lightbox>
                </div>
                <div class="like-comment">
                    <ul class="list-inline">
                        <li class="list-inline-item border-right pe-3">
                            <label class="m-0"><a href="#"><i class="fa fa-heart"></i></a>  Like</label><span
                                class="ms-2 counter">
                                <number class="counter follow-num" ref="number" :from="0" :to="2659" :duration="5"
                                    :delay="0" easing="Power1.easeOut" />
                            </span>
                        </li>
                        <li class="list-inline-item ms-2">
                            <label class="m-0"><a href="#"><i class="fa fa-comment"></i></a>  Comment</label><span
                                class="ms-2 counter">
                                <number class="counter follow-num" ref="number" :from="0" :to="569" :duration="5" :delay="0"
                                    easing="Power1.easeOut" />
                            </span>
                        </li>
                    </ul>
                </div>
            </div>
        </div>
    </div>
</template>
<script lang="ts" setup>
import { defineAsyncComponent } from 'vue';
import { ref, onMounted } from "vue"
const Card3 = defineAsyncComponent(() => import("@/components/common/card/CardData3.vue"))
const lightBoxImages = ref([])
let visible = ref<boolean>(false)
let indexRef = ref<number>(0)
const imgs = ref([{ src: require('@/assets/images/other-images/profile-style-img3.png'), title: 'Image caption  1' },])
const img = ref([{ image: 'other-images/profile-style-img3.png' },])

function showImg(index: number) {
    indexRef.value = index
    visible.value = true
}
function handleHide() {
    visible.value = false
}

function getImgUrl(path: string) {
    return require('@/assets/images/' + path);
}
</script>