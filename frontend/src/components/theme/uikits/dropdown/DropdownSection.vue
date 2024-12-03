<template>
    <Card3 colClass="col-xl-4 col-sm-6" cardClass="height-equal" cardbodyClass="rtl-dropdown heading-dropdown" pre="true"
        preClass="f-m-light mt-1" headerTitle="true" title="Heading dropdown" :desc="desc">
        <div class="common-flex">
            <div class="btn-group">
                <button class="btn btn-success rounded-pill dropdown-toggle" type="button" data-bs-toggle="dropdown"
                    aria-expanded="false">Party</button>
                <ul class="dropdown-menu dropdown-block">
                    <li><a class="dropdown-item fw-bold fs-6" href="#">Party List </a>
                        <ul>
                            <li> <a class="dropdown-item" href="#">Balloons</a></li>
                            <li> <a class="dropdown-item" href="#">Cake </a></li>
                        </ul>
                    </li>
                </ul>
            </div>

        </div>
    </Card3>


    <Card3 colClass="col-xl-4 col-sm-6" cardClass="height-equal" pre="true" preClass="f-m-light mt-1" headerTitle="true"
        title="With input type" :desc="desc1">
        <div class="common-flex">
            <button class="btn btn-warning" type="button" data-bs-toggle="dropdown" aria-expanded="false">Inputs
            </button>
            <ul class="dropdown-menu dropdown-block dropdown-wrapper dark-input-type">
                <li>
                    <div class="input-group rounded-0 border-0 shadow-none">
                        <div class="input-group-text">
                            <input class="form-check-input mt-0" type="checkbox" value=""
                                aria-label="Checkbox for following text input">
                        </div><span>Default checkbox</span>
                    </div>
                    <div class="input-group rounded-0 border-0 shadow-none">
                        <div class="input-group-text">
                            <input class="form-check-input mt-0" type="radio" value=""
                                aria-label="Radio button for following text input">
                        </div><span>Default radio</span>
                    </div>
                </li>
            </ul>
        </div>
    </Card3>


    <Card3 colClass="col-xl-4 col-sm-6" cardClass="height-equal" cardbodyClass="dropdown-basic m-0 rtl-dropdown" pre="true"
        preClass="f-m-light mt-1" headerTitle="true" title="Dark dropdown" :desc="desc2">
        <div class="common-flex dark-dropdown">
            <button class="btn btn-dark dropdown-toggle" type="button" data-bs-toggle="dropdown" aria-expanded="false">Dark
                Night</button>
            <ul class="dropdown-menu dropdown-menu-dark dropdown-block">
                <li><a class="dropdown-item active" href="#">Dark moon</a></li>
                <li><a class="dropdown-item" href="#">Dark owl </a></li>
                <li><a class="dropdown-item" href="#">Nightfall</a></li>
            </ul>

        </div>
    </Card3>
</template>
<script lang="ts" setup>
import { ref, defineAsyncComponent } from 'vue'
import { alert } from "@/core/data/uikits"
import { getImages } from "@/composables/common/getImages"
const Card3 = defineAsyncComponent(() => import("@/components/common/card/CardData3.vue"))
let desc = ref<string>("Main heading and any sub-content in dropdown.")
let desc1 = ref<string>("Use the checkbox using dropdown<code>(type='checkbox'/'radio')</code>.")
let desc2 = ref<string>("<code>.dropdown-menu-dark </code>class through make dark mode.")
</script>