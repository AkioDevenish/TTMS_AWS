<template>
    <Card3 colClass="col-12" cardbodyClass="btn-group-showcase" headerTitle="true" title="Basic button group">
        <div class="row">
            <div class="col-xxl-4 col-md-6 col-sm-12" v-for="(item, index) in basic" :key="index">
                <div class="btn-group" role="group" aria-label="Basic example">
                    <button class="btn " :class="item.classes" type="button">Left</button>
                    <button class="btn " :class="item.classes" type="button">Middle</button>
                    <button class="btn " :class="item.classes" type="button">Right</button>
                </div>
            </div>
        </div>
    </Card3>

    <Card3 colClass="col-12" cardbodyClass="btn-group-showcase" headerTitle="true" title="Edges button group">
        <div class="row">
            <div class="col-xxl-4 col-md-6 col-sm-12" v-for="(item, index) in basic" :key="index">
                <div class="btn-group btn-group-pill" role="group" aria-label="Basic example">
                    <button class="btn " :class="item.classes" type="button">Left</button>
                    <button class="btn " :class="item.classes" type="button">Middle</button>
                    <button class="btn " :class="item.classes" type="button">Right</button>
                </div>
            </div>
        </div>
    </Card3>

    <Card3 colClass="col-12" cardbodyClass="btn-group-showcase" headerTitle="true" title="Flat button group">
        <div class="row">
            <div class="col-xxl-4 col-md-6 col-sm-12" v-for="(item, index) in flat" :key="index">
                <div class="btn-group btn-group-square" role="group" aria-label="Basic example">
                    <button class="btn " :class="item.classes" type="button">Left</button>
                    <button class="btn " :class="item.classes" type="button">Middle</button>
                    <button class="btn " :class="item.classes" type="button">Right</button>
                </div>
            </div>
        </div>
    </Card3>
    <Card3 colClass="col-12" cardbodyClass="btn-group-showcase" headerTitle="true" title="large Button group">
        <div class="row">
            <div class="col-md-6 col-sm-12 col-xxl-4" v-for="(item, index) in basic" :key="index">
                <div class="btn-group" role="group" aria-label="Basic example">
                    <button class="btn btn-lg" :class="item.classes" type="button">Left</button>
                    <button class="btn btn-lg" :class="item.classes" type="button">Middle</button>
                    <button class="btn btn-lg" :class="item.classes" type="button">Right</button>
                </div>
            </div>
        </div>
    </Card3>

    <Card3 colClass="col-12" cardbodyClass="btn-group-showcase" headerTitle="true" title="large Edges Button group">
        <div class="row">
            <div class="col-md-6 col-sm-12 col-xxl-4" v-for="(item, index) in basic" :key="index">
                <div class="btn-group btn-group-pill" role="group" aria-label="Basic example">
                    <button class="btn btn-lg" :class="item.classes" type="button">Left</button>
                    <button class="btn btn-lg" :class="item.classes" type="button">Middle</button>
                    <button class="btn btn-lg" :class="item.classes" type="button">Right</button>
                </div>
            </div>
        </div>
    </Card3>

    <Card3 colClass="col-12" cardbodyClass="btn-group-showcase" headerTitle="true" title="Outline Custom button group">
        <div class="row">
            <div class="col-xxl-4 col-md-6 col-sm-12" v-for="(item, index) in common" :key="index">
                <div class="btn-group btn-group-pill" role="group" aria-label="Basic example">
                    <button :class="'btn btn-outline-' + item.classes" type="button">Left</button>
                    <button :class="'btn btn-' + item.classes" type="button">Middle</button>
                    <button :class="'btn btn-outline-' + item.classes" type="button">Right</button>
                </div>
            </div>
        </div>
    </Card3>

    <Card3 colClass="col-12" cardbodyClass="btn-group-showcase" headerTitle="true" title="Outline button group">
        <div class="row">
            <div class="col-xxl-4 col-md-6 col-sm-12" v-for="(item, index) in common" :key="index">
                <div class="btn-group" role="group" aria-label="Basic example">
                    <button :class="'btn btn-outline-' + item.classes" type="button">Left</button>
                    <button :class="'btn btn-outline-' + item.classes" type="button">Middle</button>
                    <button :class="'btn btn-outline-' + item.classes" type="button">Right</button>
                </div>
            </div>
        </div>
    </Card3>
</template>
<script lang="ts" setup>
import { ref, defineAsyncComponent } from 'vue'
import { basic, flat, common } from "@/core/data/buttons"
import { getImages } from "@/composables/common/getImages"
const Card3 = defineAsyncComponent(() => import("@/components/common/card/CardData3.vue"))
let desc = ref<string>("Use the <code>.alert </code> utility class to quickly provide additional content within any alerts.")
</script>