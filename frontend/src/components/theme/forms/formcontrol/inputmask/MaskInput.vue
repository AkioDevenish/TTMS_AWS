<template>
    <Card3 colClass="col-12" pre="true" preClass="f-m-light mt-1" headerTitle="true" title="Input masks" :desc="desc">
        <div class="row g-3">
            <div :class="item.colclass" v-for="(item, index) in masks" :key="index">
                <div class="card-wrapper border rounded-3 light-card checkbox-checked">
                    <h6 class="sub-title">{{ item.title }}</h6>
                    <form class="row g-3">
                        <div :class="item.class" v-for="(items, index) in item.children" :key="index">
                            <label class="col-form-label" :for="items.id">{{ items.title }}</label>
                            <input class="form-control" :id="items.id" type="text" :placeholder="items.placeholder">
                        </div>

                    </form>
                </div>
            </div>

        </div>
    </Card3>
</template>
<script lang="ts" setup>
import { ref, defineAsyncComponent } from 'vue'
import { masks } from "@/core/data/forms"
const Card3 = defineAsyncComponent(() => import("@/components/common/card/CardData3.vue"))
let desc = ref<string>("Input mask used in form-validations,forms,card-details,and etc.")
</script>