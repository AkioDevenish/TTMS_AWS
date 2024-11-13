<template>
    <Card3 colClass="col-md-6" pre="true" cardBodyClass="custom-input" preClass="f-m-light mt-1" headerTitle="true"
        title="Floating form " :desc="desc">
        <div class="card-wrapper border rounded-3">
            <form class="row g-3 floating-wrapper">
                <div class="col-12">
                    <div class="form-floating mb-3">
                        <input class="form-control" id="floatingInput22" type="email" placeholder="name@example.com">
                        <label for="floatingInput22">Email address</label>
                    </div>
                </div>
                <div class="col-12">
                    <div class="form-floating">
                        <input class="form-control" id="floatingPassword" type="password" placeholder="Password">
                        <label for="floatingPassword">Password</label>
                    </div>
                </div>
                <div class="col-12">
                    <div class="form-check checkbox-checked">
                        <input class="form-check-input" id="gridCheck" type="checkbox">
                        <label class="form-check-label" for="gridCheck">Check me out</label>
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
let desc = ref<string>("Use the <code>.form-floating</code> through create floating form.")
</script>