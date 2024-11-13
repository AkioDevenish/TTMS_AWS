<template>
    <Card3 colClass="col-12" pre="true" preClass="f-m-light mt-1" headerTitle="true" title="Default checkbox " :desc="desc">
        <div class="row g-3">
            <div class="col-sm-6 col-xl-4">
                <div class="card-wrapper border rounded-3 checkbox-checked">
                    <h6 class="sub-title">Default Checks</h6>
                    <div class="form-check">
                        <input class="form-check-input" id="flexCheckDefault" type="checkbox" value="">
                        <label class="form-check-label" for="flexCheckDefault">Default checkbox</label>
                    </div>
                    <div class="form-check">
                        <input class="form-check-input" id="flexCheckChecked" type="checkbox" value="" checked>
                        <label class="form-check-label" for="flexCheckChecked">Checked checkbox</label>
                    </div>
                </div>
            </div>
            <div class="col-sm-6 col-xl-4">
                <div class="card-wrapper border rounded-3 checkbox-checked">
                    <h6 class="sub-title">Disabled Checks</h6>
                    <div class="form-check">
                        <input class="form-check-input" id="flexCheckDisabled" type="checkbox" value disabled>
                        <label class="form-check-label" for="flexCheckDisabled">Disabled checkbox</label>
                    </div>
                    <div class="form-check">
                        <input class="form-check-input" id="flexCheckCheckedDisabled" type="checkbox" value checked
                            disabled>
                        <label class="form-check-label" for="flexCheckCheckedDisabled">Disabled checked
                            checkbox</label>
                    </div>
                </div>
            </div>
            <div class="col-sm-6 col-xl-4">
                <div class="card-wrapper border rounded-3 checkbox-checked">
                    <h6 class="sub-title">Right Checks </h6>
                    <div class="form-check form-check-reverse">
                        <input class="form-check-input" id="reverseCheck1" type="checkbox" value>
                        <label class="form-check-label" for="reverseCheck1">Reverse checkbox</label>
                    </div>
                    <div class="form-check form-check-reverse">
                        <input class="form-check-input" id="reverseCheck2" type="checkbox" value disabled checked>
                        <label class="form-check-label" for="reverseCheck2">Disabled reverse checkbox</label>
                    </div>
                </div>
            </div>
            <div class="col-xl-12 col-sm-6">
                <div class="card-wrapper border rounded-3 checkbox-checked">
                    <h6 class="sub-title">Indeterminate </h6>
                    <div class="form-check">
                        <input class="form-check-input" id="flexCheckIndeterminate" type="checkbox" value="">
                        <label class="form-check-label" for="flexCheckIndeterminate">Indeterminate checkbox</label>
                    </div>
                </div>
            </div>
        </div>
    </Card3>
</template>
<script lang="ts" setup>
import { ref, defineAsyncComponent } from 'vue'
const Card3 = defineAsyncComponent(() => import("@/components/common/card/CardData3.vue"))
let desc = ref<string>(" Use the <code>.form-check-input </code>and <code>.form-check-label </code>for checkbox.")
</script>