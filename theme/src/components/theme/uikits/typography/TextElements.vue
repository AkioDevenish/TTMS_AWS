<template>
    <Card3 colClass="col-sm-12 col-xl-6" titleClass="mb-0" pre="true" preClass="f-m-light mt-1" headerTitle="true"
        title="Inline text elements" :desc="desc">
        <div class="d-flex flex-column gap-2">
            <p class="mb-0" v-for="(item, index) in inline" :key="index" v-html="item.font">
            </p>

        </div>
    </Card3>


    <Card3 colClass="col-sm-12 col-xl-6" titleClass="mb-0" pre="true" preClass="f-m-light mt-1" headerTitle="true"
        title="Text color" :desc="desc1">
        <div class="d-flex flex-column gap-2">
            <p class=" mb-0" :class="item.color" v-for="(item, index) in textcolor" :key="index" v-html="item.title"></p>
        </div>
    </Card3>


    <Card3 colClass="col-sm-12 " titleClass="mb-0" pre="true" preClass="f-m-light mt-1" headerTitle="true"
        title="Blockquotes" :desc="desc2">
        <div class="figure d-block dark-blockquote" :class="item.class" v-for="(item, index) in blockquotes" :key="index">
            <blockquote class="blockquote light-card mb-2 " :class="item.bgclass">
                <p class="mb-0 " :class="item.textclass">{{ item.text }}</p><span class="blockquote-footer pt-3">{{
                    item.footer }}</span>
            </blockquote>
        </div>

    </Card3>
</template>
<script lang="ts" setup>
import { ref, defineAsyncComponent } from 'vue'
import { inline, textcolor, blockquotes } from "@/core/data/uikits"
const Card3 = defineAsyncComponent(() => import("@/components/common/card/CardData3.vue"))
let desc = ref<string>("Styling for common inline HTML5 elements.")
let desc1 = ref<string>("You can Give text color by using <code>txt-*</code> class")
let desc2 = ref<string>("The <code>&lt;blockquote&gt;</code> tag specifies a section that is quoted from another source.")
</script>