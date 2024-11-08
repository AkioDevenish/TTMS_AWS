<template>
    <Card3 colClass="col-xxl-6" pre="true" preClass="f-m-light mt-1" headerTitle="true" title="Material style tabs"
        :desc="desc">
        <ul class="nav nav-tabs border-tab border-0 mb-0 nav-danger" id="topline-tab" role="tablist">
            <li class="nav-item"><a class="nav-link active nav-border pt-0 txt-danger nav-danger" id="topline-top-user-tab"
                    data-bs-toggle="tab" href="#topline-top-user" role="tab" aria-controls="topline-top-user"
                    aria-selected="true"><i class="icofont icofont-man-in-glasses"></i>User</a></li>
            <li class="nav-item"><a class="nav-link nav-border txt-danger nav-danger" id="topline-top-description-tab"
                    data-bs-toggle="tab" href="#topline-top-description" role="tab" aria-controls="topline-top-description"
                    aria-selected="false"><i class="icofont icofont-file-document"></i>Description</a></li>
            <li class="nav-item"><a class="nav-link nav-border txt-danger nav-danger" id="topline-top-review-tab"
                    data-bs-toggle="tab" href="#topline-top-review" role="tab" aria-controls="topline-top-review"
                    aria-selected="false"><i class="icofont icofont-star"></i>Review</a></li>
        </ul>
        <div class="tab-content" id="topline-tabContent">
            <div class="tab-pane fade " :class="items.active == true ? 'show active' : ''" :id="items.ids" role="tabpanel"
                aria-labelledby="topline-top-user-tab" v-for="(items, index) in material" :key="index">
                <div class="card-body px-0 pb-0">
                    <div class="user-header pb-2">
                        <h6 class="fw-bold">{{ items.title }}</h6>
                    </div>
                    <div class="user-content">
                        <div class="table-responsive theme-scrollbar">
                            <table class="table mb-0">
                                <thead>
                                    <tr>
                                        <th scope="col">{{ items.no }}</th>
                                        <th scope="col">{{ items.name }}</th>
                                        <th scope="col">{{ items.country }}</th>
                                        <th scope="col">{{ items.contact }}</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr v-for="(item, index) in items.children" :key="index">
                                        <th scope="row" v-if="item.row">{{ item.row }}</th>
                                        <td>{{ item.name }}</td>
                                        <td>{{ item.coutry }}</td>
                                        <td v-if="item.cont">{{ item.cont }}</td>
                                        <td v-html="stars(item.star)"></td>
                                    </tr>

                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
            </div>

        </div>
    </Card3>
</template>
<script lang="ts" setup>
import { ref, defineAsyncComponent } from 'vue'
import { getImages } from "@/composables/common/getImages"
import { material } from "@/core/data/uikits"
const Card3 = defineAsyncComponent(() => import("@/components/common/card/CardData3.vue"))
let desc = ref<string>("Use the <code>.nav-link </code>with <code>.active </code>class through access new tabs. And icons of design for attractive webpage.")
function stars(count: number) {
    var stars = '';

    for (var i = 0; i < 5; i++) {
        if (count > i) {
            stars = stars + '<i class="ico-color icofont icofont-star"></i>';
        }
    }

    return stars;
}
</script>