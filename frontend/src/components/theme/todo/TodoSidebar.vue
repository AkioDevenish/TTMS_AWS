<template>
    <div class="col-xxl-3 col-xl-4 box-col-30">
        <div class="email-sidebar md-sidebar"><a class="btn btn-primary email-aside-toggle md-sidebar-toggle"
                @click="collapseFilter()">To Do
                filter</a>
            <div class="email-left-aside md-sidebar-aside" :class="filtered ? 'open' : ''">
                <div class="card">
                    <div class="card-body">
                        <div class="email-app-sidebar left-bookmark custom-scrollbar">
                            <div class="d-flex align-items-center">
                                <div class="media-size-email"><img class="me-3 rounded-circle"
                                        src="@/assets/images/user/user.png" alt=""></div>
                                <div class="flex-grow-1">
                                    <h6 class="f-w-600">Mark Jecno</h6>
                                    <p>Markjecno@gmail.com</p>
                                </div>
                            </div>
                            <ul class="nav main-menu">
                                <li class="nav-item">
                                    <button class="btn-primary text-white badge-light btn-mail w-100"><vue-feather
                                            class="me-2" type="check-circle"></vue-feather>To Do List</button>
                                </li>

                                <li class="nav-item" v-for="(item, index) in todosidebar" :key="index"><a
                                        href="javascript:void(0)"><span class="iconbg "
                                            :class="item.badgeclass"><vue-feather
                                                :type="item.icon"></vue-feather></span><span class="title ms-2">{{
                                                    item.title }}</span><span :class="item.pillclass">{{ item.badge }}</span></a>
                                </li>

                            </ul>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
<script lang="ts" setup>
import { ref, defineAsyncComponent } from "vue"
import { todosidebar } from "@/core/data/todo"
import { getImages } from "@/composables/common/getImages"
let filtered = ref<boolean>(false)
function collapseFilter() {
    filtered.value = !filtered.value
}
</script>