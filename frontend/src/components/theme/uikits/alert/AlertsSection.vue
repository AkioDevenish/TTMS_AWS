<template>
    <Card3 colClass="col-sm-12 col-xl-6" cardClass="height-equal" pre="true" preClass="f-m-light mt-1" headerTitle="true"
        title="Dismissing dark alert" :desc="desc">
        <div class="alert alert-secondary dark alert-dismissible fade show" role="alert"><i data-feather="heart"></i>
            <p>Check your update! You should check in on some of those fields below.</p>
            <button class="btn-close" type="button" data-bs-dismiss="alert" aria-label="Close"></button>
        </div>
    </Card3>

    <Card3 colClass="col-sm-12 col-xl-6" cardClass="height-equal" pre="true" preClass="f-m-light mt-1" headerTitle="true"
        title="Dismissing light alert" :desc="desc">
        <div class="alert alert-warning alert-dismissible fade show" role="alert"><i data-feather="bell"></i>
            <p>Hidden content You should check in on some of those fields below.</p>
            <button class="btn-close" type="button" data-bs-dismiss="alert" aria-label="Close"></button>
        </div>
    </Card3>

    <Card3 colClass="col-xl-6" cardbodyClass="live-dark" cardClass="height-equal" pre="true" preClass="f-m-light mt-1"
        headerTitle="true" title="Live alert" :desc="desc">
        <div id="liveAlertPlaceholder">
            <div v-for="(item, index) in data" :key="index">
                <div class="alert alert-light-dark txt-dark mb-3 alert-dismissible" role="alert">
                    <div>{{ item }}</div> <button type="button" class="btn-close" data-bs-dismiss="alert"
                        aria-label="Close"></button>
                </div>
            </div>
        </div>
        <button class="btn btn-dark" id="liveAlertBtn" type="button" @click="addAlert">Show live alert</button>
    </Card3>

    <Card3 colClass="col-xl-6" cardbodyClass="live-dark" cardClass="height-equal" pre="true" preClass="f-m-light mt-1"
        headerTitle="true" title="Left border alert" :desc="desc">
        <div class="alert alert-light-dark light alert-dismissible fade show text-dark border-left-wrapper" role="alert"><i
                data-feather="help-circle"></i>
            <p>You can check in on some of those fields below.</p>
            <button class="btn-close" type="button" data-bs-dismiss="alert" aria-label="Close"></button>
        </div>
    </Card3>
</template>
<script lang="ts" setup>
import { ref, defineAsyncComponent } from 'vue'
import { alert } from "@/core/data/uikits"
import { getImages } from "@/composables/common/getImages"
const Card3 = defineAsyncComponent(() => import("@/components/common/card/CardData3.vue"))
let desc = ref<string>("Use the <code>.alert-dismissible</code> utility class to quickly remove the alerts.")
let desc1 = ref<string>(" Click the button below to show an alert,then dismiss it with the built-in close button.")
let desc2 = ref<string>("Use the <code>.border-left-wrapper </code>to change border-left radius.")
let data = ref<string[]>([])
function addAlert() {
    data.value.push("Nice, you triggered this alert message!")
}
</script>