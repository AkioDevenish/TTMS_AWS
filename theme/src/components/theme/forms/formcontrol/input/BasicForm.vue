<template>
    <Card3 colClass="col-md-6" pre="true" cardBodyClass="custom-input" preClass="f-m-light mt-1" headerTitle="true"
        title="Basic form" :desc="desc">
        <div class="card-wrapper border rounded-3">
            <form class="row g-3">
                <div class="col-md-12">
                    <label class="form-label" for="inputEmail4">Email</label>
                    <input class="form-control" id="inputEmail4" type="email" placeholder="Enter Your Email">
                </div>
                <div class="col-md-12">
                    <label class="form-label" for="inputPassword4">Password</label>
                    <input class="form-control" id="inputPassword4" type="password" placeholder="Enter Your Password">
                </div>
                <div class="col-12">
                    <div class="form-check checkbox-checked">
                        <input class="form-check-input" id="gridCheck1" type="checkbox">
                        <label class="form-check-label" for="gridCheck1">Check me out</label>
                    </div>
                </div>
                <div class="col-12">
                    <button class="btn btn-primary" type="submit">Sign in </button>
                </div>
            </form>
        </div>
    </Card3>
</template>
<script lang="ts" setup>
import { ref, defineAsyncComponent } from 'vue'
const Card3 = defineAsyncComponent(() => import("@/components/common/card/CardData3.vue"))
let desc = ref<string>("Use the <code>.form-label </code>and <code>.form-control </code>through create basic form.")
</script>