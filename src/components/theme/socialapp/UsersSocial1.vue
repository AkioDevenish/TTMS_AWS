<template>
    <Card3 colClass="col-sm-12">
        <div class="new-users-social">
            <div class="d-flex"><img class="rounded-circle image-radius m-r-15" :src="getImages('user/1.jpg')" alt="">
                <div class="flex-grow-1">
                    <h4 class="mb-0 f-w-700">ELANA</h4>
                    <p>January, 12,2019</p>
                </div><span class="pull-right mt-0"><vue-feather type='more-vertical'></vue-feather></span>
            </div>
        </div><img class="img-fluid" alt="" src="@/assets/images/social-app/timeline-2.png">
        <div class="timeline-content">
            <p>
                Lorem ipsum dolor sit amet, consectetur adipiscing elit. Suspendisse sed urna in justo euismod condimentum.
                Fusce
                placerat enim et odio molestie sagittis.
            </p>
            <div class="like-content"><span><i class="fa fa-heart font-danger"></i></span><span
                    class="pull-right comment-number"><span>20 </span><span><i
                            class="fa fa-share-alt me-0"></i></span></span><span class="pull-right comment-number"><span>10
                    </span><span><i class="fa fa-comments-o"></i></span></span></div>
            <div class="social-chat">
                <div class="your-msg" v-for="(item, index) in post1" :key="index">
                    <div class="d-flex"><img class="img-50 img-fluid m-r-20 rounded-circle" alt=""
                            :src="getImages(item.image)">
                        <div class="flex-grow-1"><span class="f-w-600">{{ item.name }} <span>{{
                            item.date
                        }}<i class="fa fa-reply font-primary"></i></span></span>
                            <p>{{ item.msg }}</p>
                        </div>
                    </div>
                </div>

                <div class="text-center"><a href="#">More Commnets</a></div>
            </div>
            <div class="comments-box">
                <div class="d-flex"><img class="img-50 img-fluid m-r-20 rounded-circle" alt=""
                        :src="getImages('user/1.jpg')">
                    <div class="flex-grow-1">
                        <div class="input-group text-box">
                            <input class="form-control input-txt-bx" type="text" name="message-to-send"
                                placeholder="Post Your commnets">
                            <div class="input-group-append">
                                <button class="btn btn-transparent" type="button"><i class="fa fa-smile-o"> </i></button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </Card3>
</template>
<script lang="ts" setup>
import { ref, defineAsyncComponent, onMounted } from 'vue'
import { post1 } from "@/core/data/sociall-app"
import { getImages } from "@/composables/common/getImages"
const Card3 = defineAsyncComponent(() => import("@/components/common/card/CardData3.vue"))
</script>