<template>
    <Card3 colClass="col-sm-12 listing" titleClass="mb-0" pre="true" preClass="f-m-light mt-1" headerTitle="true"
        title="Listing typography" :desc="desc">
        <div class="row g-3">
            <div class="col-md-6 col-xxl-4">
                <div class="card-wrapper border rounded-3">
                    <h6 class="sub-title fw-bold">Unorder list</h6>
                    <ul>
                        <li v-for="(item, index) in unorder" :key="index">{{ item.title }}</li>

                    </ul>
                </div>
            </div>
            <div class="col-md-6 col-xxl-4">
                <div class="card-wrapper border rounded-3 h-100">
                    <h6 class="sub-title fw-bold">Order list</h6>
                    <ol>
                        <li>UI Kits</li>
                        <li>Bonus Ui</li>
                        <li>Animations</li>
                        <li>
                            <ol>
                                <li>Typography</li>
                                <li>Avatars</li>
                                <li>Grid</li>
                                <li>Tag & pills</li>
                                <li>Alert</li>
                            </ol>
                        </li>
                        <li>Dropdown</li>
                        <li>Tabs</li>
                        <li>Accordion</li>
                    </ol>
                </div>
            </div>
            <div class="col-md-12 col-xxl-4">
                <div class="card-wrapper border rounded-3">
                    <h6 class="sub-title fw-bold">Description list</h6>
                    <dl>
                        <div v-for="(item, index) in description" :key="index">
                            <dt>{{ item.title }}</dt>
                            <dd class="mx-0">{{ item.dec }}</dd>

                        </div>
                        <dt>The purpose of our lives is to be happy.</dt>
                        <dd class="mx-0 mb-0">-Dalai Lama</dd>
                    </dl>
                </div>
            </div>
        </div>
    </Card3>
</template>
<script lang="ts" setup>
import { ref, defineAsyncComponent } from 'vue'
import { unorder, description } from "@/core/data/uikits"
const Card3 = defineAsyncComponent(() => import("@/components/common/card/CardData3.vue"))
let desc = ref<string>("All typography list:- <code>&lt;ul&gt;</code>,<code>&lt;ol&gt;</code> &amp; <code>&lt;dl&gt;</code>")
</script>