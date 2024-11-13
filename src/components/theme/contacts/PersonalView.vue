<template>
    <div class="card mb-0">
        <div class="card-header d-flex">
            <h4>Personal</h4><span class="f-14 pull-right mt-0">{{ personal.length }} Contacts</span>
        </div>
        <div class="card-body p-0">
            <div class="row list-persons" id="addcon">
                <div class="col-xl-4 xl-50 col-md-5">
                    <div class="nav flex-column nav-pills" id="v-pills-tab" role="tablist" aria-orientation="vertical">
                        <a class="contact-tab-0 nav-link " :class="contact.active ? 'active show' : ''"
                            v-for="(contact, index) in personal" :key="index" id="v-pills-user-tab" data-bs-toggle="pill"
                            :href="'#v-pills-user' + contact.id" role="tab" aria-controls="v-pills-user"
                            aria-selected="true">
                            <div class="d-flex"><img class="img-50 img-fluid m-r-20 rounded-circle update_img_0"
                                    :src="contact.imgUrl || getImages(contact.image)" alt="">
                                <div class="flex-grow-1">
                                    <h6> <span class="first_name_1">{{ contact.name1 }}</span> <span class="last_name_1">{{
                                        contact.name2 }}</span>
                                    </h6>
                                    <p class="email_add_0">{{ contact.email }}</p>
                                </div>
                            </div>
                        </a>
                    </div>
                </div>
                <PersonalDetail />
            </div>
        </div>
    </div>
</template>
<script lang="ts" setup>
import { useContactsStore } from "@/store/contacts"
import { getImages } from "@/composables/common/getImages"
import { defineAsyncComponent } from 'vue';
const PersonalDetail = defineAsyncComponent(() => import("@/components/theme/contacts/PersonalDetail.vue"))
const store = useContactsStore()
const personal = store.personals
</script>