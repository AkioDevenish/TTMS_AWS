<template>
    <Card3 colClass="col-xl-6 col-sm-12" cardbodyClass="accordion-border icons-accordion" pre="true"
        preClass="f-m-light mt-1" headerTitle="true" title="With icons accordion" :desc="desc">
        <div class="accordion dark-accordion" id="accordionPanelsStayOpenExample">
            <div class="accordion-item">
                <h2 class="accordion-header" id="panelsStayOpen-headingOne">
                    <button class="accordion-button collapsed gap-2 bg-light-secondary active txt-secondary" type="button"
                        data-bs-toggle="collapse" data-bs-target="#panelsStayOpen-collapseOne"
                        aria-controls="panelsStayOpen-collapseOne" :aria-expanded="isActive ? 'true' : 'false'"
                        :class="[isActive ? 'active' : '', 'collapsible']" v-on:click="toggle"><vue-feather
                            class="svg-wrapper" type="bell"></vue-feather>Keep in touch<vue-feather class="svg-color"
                            type="chevron-down"></vue-feather></button>
                </h2>
                <div class="accordion-collapse collapse" :class="[isActive ? 'block' : ' show']" v-show="isActive"
                    id="panelsStayOpen-collapseOne" aria-labelledby="panelsStayOpen-headingOne">
                    <div class="accordion-body">
                        <p> <em class="txt-danger"> " This page might not behave as expected because Windows
                                Internet Explorer isn't configured to load unsigned ActiveX controls."</em> or
                            "Allow this page to install an unsigned ActiveX Control? Doing so from untrusted sources
                            may harm your computer." (Both phrased as conditions that may cause future problems.)
                        </p>
                    </div>
                </div>
            </div>
            <div class="accordion-item">
                <h2 class="accordion-header" id="panelsStayOpen-headingTwo">
                    <button class="accordion-button collapsed gap-2 bg-light-secondary active txt-secondary" type="button"
                        data-bs-toggle="collapse" data-bs-target="#panelsStayOpen-collapseTwo"
                        :aria-expanded="isActive2 ? 'true' : 'false'" :class="[isActive1 ? 'active' : '', 'collapsible']"
                        v-on:click="toggle1" aria-controls="panelsStayOpen-collapseTwo"><vue-feather class="svg-wrapper"
                            type="message-circle"></vue-feather>Chats with others<vue-feather class="svg-color"
                            type="chevron-down"></vue-feather></button>
                </h2>
                <div class="accordion-collapse collapse" :class="[isActive1 ? 'block' : ' show']" v-show="isActive1"
                    id="panelsStayOpen-collapseTwo" aria-labelledby="panelsStayOpen-headingTwo">
                    <div class="accordion-body">
                        <ul class="d-flex flex-column gap-2 accordions-content">
                            <li>You get the same features in Chat and Chat in Gmail, but the integrated Gmail
                                experience provides a central location to communicate with friends, family, or
                                coworkers between emails.</li>
                            <li> <strong>Chat:</strong> Use when you prefer a dedicated chat experience and don't
                                mind switching between different apps.</li>
                        </ul>
                    </div>
                </div>
            </div>
            <div class="accordion-item">
                <h2 class="accordion-header" id="panelsStayOpen-headingThree">
                    <button class="accordion-button collapsed gap-2 bg-light-secondary active txt-secondary" type="button"
                        data-bs-toggle="collapse" data-bs-target="#panelsStayOpen-collapseThree"
                        :aria-expanded="isActive2 ? 'true' : 'false'" :class="[isActive2 ? 'active' : '', 'collapsible']"
                        v-on:click="toggle2" aria-controls="panelsStayOpen-collapseThree"><vue-feather class="svg-wrapper"
                            type="check-square"></vue-feather>Right way to code <vue-feather class="svg-color"
                            type="chevron-down"></vue-feather></button>
                </h2>
                <div class="accordion-collapse collapse" :class="[isActive2 ? 'block' : ' show']" v-show="isActive2"
                    id="panelsStayOpen-collapseThree" aria-labelledby="panelsStayOpen-headingThree">
                    <div class="accordion-body">
                        <ul class="d-flex flex-column gap-2 accordions-content">
                            <li>1) Decide on the indentation and keep it that way.</li>
                            <li>2) Make comments.</li>
                            <li>3) Consistent name scheme.</li>
                            <li>4) Don't repeat code.</li>
                            <li>5) Avoid writing long code lines.</li>
                            <li>6) Break down a big task into smaller chunks.</li>
                            <li>7) Organize your program into smaller files.</li>
                            <li>8) Write clever code that is also readable.</li>
                        </ul>
                    </div>
                </div>
            </div>
        </div>
    </Card3>
</template>
<script lang="ts" setup>
import { ref, defineAsyncComponent } from 'vue'
import { useCommonStore } from "@/store/common"
const Card3 = defineAsyncComponent(() => import("@/components/common/card/CardData3.vue"))
let desc = ref<string>("Use the <code>.accordion </code>& <code>feather icons</code> through change look icons accordion.")
let store = useCommonStore()
let isActive = ref<boolean>(false)
let isActive1 = ref<boolean>(false)
let isActive2 = ref<boolean>(false)
function toggle() {
    isActive.value = !isActive.value
}
function toggle1() {
    isActive1.value = !isActive1.value
}
function toggle2() {
    isActive2.value = !isActive2.value
}
</script>