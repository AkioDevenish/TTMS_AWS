<template>
    <Card3 colClass="col-sm-12 col-xl-6" cardClass="shadow-none border" pre="true" preClass="f-m-light mt-1"
        headerTitle="true" title="Without shadow Card" :desc="desc">
        <div class="flex-space flex-wrap align-items-center"><img class="tab-img" src="@/assets/images/avtar/3.jpg"
                alt="profile">
            <p> <strong>Visit Us: </strong> 2600 Hollywood Blvd,Florida, United States- 33020<br><strong>Mail
                    Us:</strong>contact@us@gmail.com<br><strong>Contact Number: </strong>(954) 357-7760</p>
        </div>
    </Card3>
</template>
<script lang="ts" setup>
import { ref, defineAsyncComponent } from 'vue'
import { card } from "@/core/data/advance"
const Card3 = defineAsyncComponent(() => import("@/components/common/card/CardData3.vue"))
let desc = ref<string>("Use the<code>.shadow-none </code>&<code>.border </code>class through shadow removes.")
</script>