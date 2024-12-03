<template>
    <Card3 colClass="col-md-12" pre="true" preClass="f-m-light mt-1" headerTitle="true" title="Shipping form" :desc="desc">
        <div class="row shopping-wizard">
            <div class="col-12">
                <div class="row shipping-form g-5">
                    <div class="col-xl-8 shipping-border">
                        <div class="nav nav-pills horizontal-options shipping-options" id="cart-options-tab" role="tablist"
                            aria-orientation="vertical"><a class="nav-link b-r-0 " v-for="(item, index) in tab" :key="index"
                                :id="item.id" data-bs-toggle="pill" :href="item.href" role="tab" aria-controls="bill-wizard"
                                v-bind:class="{ 'active': item.id === activeclass }" aria-selected="true">
                                <div class="cart-options">
                                    <div class="stroke-icon-wizard"><i class="fa " :class="item.icon"></i></div>
                                    <div class="cart-options-content">
                                        <h6>{{ item.label }}</h6>
                                    </div>
                                </div>
                            </a>
                        </div>
                        <div class="tab-content dark-field shipping-content" id="cart-options-tabContent">
                            <Billingfrom />
                            <ShippingForms />
                            <PaymentWizard />
                            <FinishWizard />
                        </div>
                    </div>
                    <CurrentCart />
                </div>
            </div>
        </div>
    </Card3>
</template>
<script lang="ts" setup>
import { ref, defineAsyncComponent } from 'vue'
import { tab } from "@/core/data/forms"
const Card3 = defineAsyncComponent(() => import("@/components/common/card/CardData3.vue"))
const Billingfrom = defineAsyncComponent(() => import("@/components/theme/forms/formlayout/formwizard/Billingfrom.vue"))
const ShippingForms = defineAsyncComponent(() => import("@/components/theme/forms/formlayout/formwizard/ShippingForms.vue"))
const PaymentWizard = defineAsyncComponent(() => import("@/components/theme/forms/formlayout/formwizard/PaymentWizard.vue"))
const FinishWizard = defineAsyncComponent(() => import("@/components/theme/forms/formlayout/formwizard/FinishWizard.vue"))
const CurrentCart = defineAsyncComponent(() => import("@/components/theme/forms/formlayout/formwizard/CurrentCart.vue"))
let desc = ref<string>("Fill up your true details and next proceed.")
let activeclass = ref<string>('bill-wizard-tab')
</script>