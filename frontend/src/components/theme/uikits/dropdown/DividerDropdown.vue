<template>
    <Card3 colClass="col-md-6" cardbodyClass="rtl-dropdown" pre="true" preClass="f-m-light mt-1" headerTitle="true"
        title="Divider dropdown" :desc="desc">
        <div class="common-flex">
            <div class="btn-group">
                <button class="btn btn-success rounded-pill dropdown-toggle" type="button" data-bs-toggle="dropdown"
                    aria-expanded="false">Wishlist</button>
                <ul class="dropdown-menu dropdown-block">
                    <li><a class="dropdown-item" href="#">Shoes </a></li>
                    <li><a class="dropdown-item" href="#">Bag</a></li>
                    <li><a class="dropdown-item" href="#">Clothes </a></li>
                    <li>
                        <hr class="dropdown-divider">
                    </li>
                    <li><a class="dropdown-item" href="#">Separated link</a></li>
                </ul>
            </div>
            <div class="btn-group">
                <button class="btn btn-primary rounded-pill dropdown-toggle" type="button" data-bs-toggle="dropdown"
                    aria-expanded="false">Sports </button>
                <ul class="dropdown-menu dropdown-block">
                    <li><a class="dropdown-item" href="#">Badminton</a></li>
                    <li><a class="dropdown-item" href="#">Tenis </a></li>
                    <li><a class="dropdown-item" href="#">Kho-Kho</a></li>
                    <li>
                        <hr class="dropdown-divider">
                    </li>
                    <li><a class="dropdown-item" href="#">Separated link</a></li>
                </ul>
            </div>
            <div class="btn-group">
                <button class="btn btn-secondary rounded-pill dropdown-toggle" type="button" data-bs-toggle="dropdown"
                    aria-expanded="false">Colors </button>
                <ul class="dropdown-menu dropdown-block">
                    <li><a class="dropdown-item" href="#">Orange </a></li>
                    <li><a class="dropdown-item" href="#">Yellow </a></li>
                    <li><a class="dropdown-item" href="#">Red </a></li>
                    <li>
                        <hr class="dropdown-divider">
                    </li>
                    <li><a class="dropdown-item" href="#">Separated link</a></li>
                </ul>
            </div>

        </div>
    </Card3>
</template>
<script lang="ts" setup>
import { ref, defineAsyncComponent } from 'vue'

const Card3 = defineAsyncComponent(() => import("@/components/common/card/CardData3.vue"))
let desc = ref<string>("When the<code>.show </code>class starts, dropdown appears. And <code>.dropdown-divider</code> to change dropdown section.")
</script>