<template>
    <Card3 headerTitle="true" title="Init AOS">
        <div><span class="comment">// The Below Function is example of how to initlize reveal</span>
            <div class="line"><span></span> &lt;script&gt; <span></span><br><code>  AOS.init();</code><br><span> &lt;</span>
                /script <span> &gt; </span></div>
        </div>
    </Card3>


    <Card3 text="true" headerTitle="true" title="How to use it?" :desc="desc">
        <div class="txt-primary"><span> &lt;</span> div data-aos="animation_name" <span> &gt; </span>
        </div>
    </Card3>

    <Card3 text="true" headerTitle="true" cardbodyClass="table-responsive" title=" Advanced settings" :desc="desc1">
        <table class="table table-bordered table-striped">
            <thead>
                <tr>
                    <th>Attribute</th>
                    <th>Description</th>
                    <th>Example value</th>
                    <th>Default value</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="(item, index) in init" :key="index">
                    <td v-html="item.attr"></td>
                    <td>{{ item.desc }}</td>
                    <td>{{ item.example }}</td>
                    <td>{{ item.default }}</td>
                </tr>

            </tbody>
        </table>
    </Card3>

    <Card3 text="true" headerTitle="true" cardbodyClass="table-responsive" title="Animation" :desc="desc2">
        <ul class="line">
            <li v-for="(item, index) in animation" :key="index">
                <h5 class="f-w-600">{{ item.title }}</h5>
                <ul class="ps-4 mb-4 list-circle">
                    <li v-for="(items, index) in item.children" :key="index">{{ items.title }}</li>

                </ul>
            </li>
        </ul>
    </Card3>

    <Card3 headerTitle="true" title=" Anchor placement">
        <ul class="ps-4 list-circle line">
            <li v-for="(item, index) in anchor" :key="index">{{ item }}</li>

        </ul>
    </Card3>


    <Card3 headerTitle="true" title="Easing functions:">
        <ul class="ps-4 list-circle line">
            <li v-for="(item, index) in easing" :key="index">{{ item }}</li>

        </ul>
    </Card3>
</template>
<script lang="ts" setup>
import { ref, defineAsyncComponent } from 'vue'
import { init, animation, anchor, easing } from "@/core/data/masonry"
const Card3 = defineAsyncComponent(() => import("@/components/common/card/CardData3.vue"))
let desc = ref<string>("All you have to do is to add <code>data-aos</code> attribute to html element, like so:")
let desc1 = ref<string>("These settings can be set both on certain elements, or as default while initializing script (in options object without <code> data- part).</code>")
let desc2 = ref<string>("There are serveral predefined animations you can use already:")
</script>