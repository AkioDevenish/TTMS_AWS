<template>
    <Card3 colClass="col-sm-12 col-xl-6" pre="true" preClass="f-m-light mt-1" headerTitle="true" title="Simple accordion"
        :desc="desc">
        <div class="accordion dark-accordion" id="simpleaccordion">
            <div class="accordion-item" v-for="(item, index) in simple" :key="index">
                <h2 class="accordion-header" :id="item.hederid">
                    <button class="accordion-button  bg-light-primary font-primary " @click="toggleAccordion(index)"
                        type="button" :data-bs-target="item.id" aria-expanded="true" :aria-controls="item.ids">{{ item.title
                        }}<vue-feather class="svg-color" type="chevron-down"></vue-feather> </button>
                </h2>
                <div class="accordion-collapse " v-if="item.isActive" :id="item.ids" :aria-labelledby="item.hederid"
                    data-bs-parent="#simpleaccordion">
                    <div class="accordion-body">
                        <div v-for="(items, index) in item.childern" :key="index">
                            <p v-html="items.desc" v-if="item.one">
                            </p>
                        </div>
                        <div v-for="(items, index) in item.childern" :key="index">
                            <p class="mb-3" v-html="items.desc" v-if="item.two">
                            </p>
                        </div>
                        <p v-if="item.three">
                            The web design process allows designers to adjust to any preferences and provide effective
                            solutions. There are many standard components of every web design, including:</p>
                        <div v-for="(items, index) in item.childern" :key="index">

                            <ul class="d-flex flex-column gap-2 accordions-content" v-if="item.three">
                                <li>--> {{ items.title }}</li>
                            </ul>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </Card3>
</template>
<script lang="ts" setup>
import { ref, defineAsyncComponent } from 'vue'
import { useCommonStore } from "@/store/common"
const Card3 = defineAsyncComponent(() => import("@/components/common/card/CardData3.vue"))
let desc = ref<string>(" Click the accordions below to expand/collapse the accordion content.  Use the <code>.accordion </code>.")
let store = useCommonStore()
let simple = store.data
const toggleAccordion = (index: number) => {
    simple[index].isActive = !simple[index].isActive;
    closeOtherAccordions(index);
};

const closeOtherAccordions = (currentIndex: number) => {
    simple.forEach((item, index) => {
        if (index !== currentIndex) {
            item.isActive = false;
        }
    });
};
</script>