<template>
    <Card3 colClass="col-xl-6" pre="true" cardClass="height-equal" preClass="f-m-light mt-1" headerTitle="true"
        title="Validation form" :desc="desc">
        <form class="row g-3 needs-validation custom-input" novalidate @submit.prevent="onCustomStyleSubmit()">
            <div class="col-12">
                <label class="form-label" for="validationCustom01">First name</label>
                <input type="text" class="form-control"
                    v-bind:class="formSubmitted ? inputs.firstname.errorMessage.length ? 'is-invalid' : 'is-valid' : ''"
                    id="name" placeholder="Your name" v-model="inputs.firstname.data">
                <div class="invalid-feedback" v-if="inputs.firstname.errorMessage.length">{{
                    inputs.firstname.errorMessage
                }}</div>
                <div class="valid-feedback" v-else>Looks Good!</div>
            </div>
            <div class="col-12">
                <label class="col-sm-12 col-form-label" for="inputPassword1">Password</label>
                <input class="form-control" id="inputPassword1" type="password" v-model="inputs.password.data"
                    v-bind:class="formSubmitted ? inputs.password.errorMessage.length ? 'is-invalid' : 'is-valid' : ''">
                <div class="invalid-feedback" v-if="inputs.password.errorMessage.length">{{
                    inputs.password.errorMessage
                }}</div>
                <div class="valid-feedback" v-else>Looks Good!</div>
            </div>
            <div class="col-12">
                <label class="form-label" for="validationCustom04">State</label>
                <select class="form-select" id="validationCustom04"
                    v-bind:class="formSubmitted ? inputs.state.errorMessage.length ? 'is-invalid' : 'is-valid' : ''"
                    v-model="inputs.state.data" required>
                    <option selected disabled value="">Choose...</option>
                    <option v-for="(value, index) in optionValues" :value="value" :key="value + index">{{
                        value
                    }}
                    </option>
                </select>
                <div class="invalid-feedback" v-if="inputs.state.errorMessage.length">{{
                    inputs.state.errorMessage
                }}</div>
                <div class="valid-feedback" v-else>Looks Good!</div>
            </div>
            <div class="col-md-6">
                <label class="form-label" for="validationCustom03">City</label>
                <input class="form-control" id="validationCustom03" type="text"
                    v-bind:class="formSubmitted ? inputs.city.errorMessage.length ? 'is-invalid' : 'is-valid' : ''"
                    placeholder="City" required v-model="inputs.city.data">
                <div class="invalid-feedback" v-if="inputs.city.errorMessage.length">{{
                    inputs.city.errorMessage
                }}</div>
                <div class="valid-feedback" v-else>Looks Good!</div>
            </div>
            <div class="col-md-6">
                <label class="form-label" for="validationCustom05">Zip</label>
                <input class="form-control" id="validationCustom05" type="text"
                    v-bind:class="formSubmitted ? inputs.zip.errorMessage.length ? 'is-invalid' : 'is-valid' : ''"
                    v-model="inputs.zip.data" placeholder="Zip" required>
                <div class="invalid-feedback" v-if="inputs.zip.errorMessage.length">{{
                    inputs.zip.errorMessage
                }}</div>
                <div class="valid-feedback" v-else>Looks Good!</div>
            </div>
            <div class="col-12">
                <div class="card-wrapper border rounded-3 checkbox-checked">
                    <h6 class="sub-title">Select your payment method</h6>
                    <div class="radio-form">
                        <div class="form-check">
                            <input class="form-check-input" id="validationFormCheck25" type="radio" name="radio-stacked"
                                required>
                            <label class="form-check-label" for="validationFormCheck25">MaterCard</label>
                        </div>
                        <div class="form-check">
                            <input class="form-check-input" id="validationFormCheck23" type="radio" name="radio-stacked"
                                required>
                            <label class="form-check-label" for="validationFormCheck23">VISA</label>
                        </div>
                    </div>
                </div>
            </div>
            <div class="col-12">
                <select class="form-select" required aria-label="select example"
                    v-bind:class="formSubmitted ? inputs.feedback.errorMessage.length ? 'is-invalid' : 'is-valid' : ''"
                    v-model="inputs.feedback.data">
                    <option selected disabled value="">Select Your Favorite Pixelstrap theme</option>
                    <option v-for="(value, index) in feedbacks" :value="value" :key="value + index">{{
                        value
                    }}
                    </option>

                </select>
                <div class="invalid-feedback" v-if="inputs.feedback.errorMessage.length">{{
                    inputs.feedback.errorMessage
                }}</div>
                <div class="valid-feedback" v-else>Looks Good!</div>
            </div>
            <div class="col-12">
                <label class="form-label" for="formFile1">Choose File</label>
                <input class="form-control" id="formFile1" type="file" aria-label="file example" required>
                <div class="invalid-feedback">Invalid form file selected</div>
            </div>
            <div class="col-12">
                <label class="form-label" for="validationTextarea">Description</label>
                <textarea class="form-control" id="validationTextarea" placeholder="Enter your comment" required></textarea>
                <div class="invalid-feedback">Please enter a message in the textarea.</div>
            </div>
            <div class="col-12">
                <div class="form-check">
                    <input class="form-check-input" id="invalidCheck" type="checkbox" value required>
                    <label class="form-check-label" for="invalidCheck">Agree to terms and conditions</label>
                    <div class="invalid-feedback">You must agree before submitting.</div>
                </div>
            </div>
            <div class="col-12">
                <button class="btn btn-primary" type="submit">Submit form</button>
            </div>
        </form>
    </Card3>
</template>
<script lang="ts" setup>
import { ref, defineAsyncComponent } from 'vue'
const Card3 = defineAsyncComponent(() => import("@/components/common/card/CardData3.vue"))
import { onCustomStyleSubmit, inputs, Submitted, optionValues, formSubmitted, feedbacks } from "@/composables/common/validationForm"
let desc = ref<string>("Custom feedback styles apply custom colors, borders, focus styles, and background icons to better communicate feedback.Background icons for <code>&lt;select&gt;</code>s are only available with <code>.form-select</code> and not <code>.form-control.</code>")
</script>