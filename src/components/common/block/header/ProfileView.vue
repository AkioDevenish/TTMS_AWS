<template>
    <div class="d-flex profile-media align-items-center"><img class="img-30" src="@/assets/images/dashboard/profile.png"
            alt="">
        <div class="flex-grow-1"><span>Joshua Woo</span>
            <p class="mb-0 font-outfit">Climate Data Scientist<i class="fa fa-angle-down"></i></p>
        </div>
    </div>
    <ul class="profile-dropdown onhover-show-div">
        <li v-for="(item, index) in profile" :key="index"><router-link :to="item.path"><vue-feather
                    :type="item.icon"></vue-feather><span>{{ item.title }}</span></router-link></li>
        <li><a @click="logout"><vue-feather type="log-in"></vue-feather><span>Log Out</span></a></li>
    </ul>
</template>
<script lang="ts" setup>
import { ref, onMounted } from 'vue';
import { profile } from "@/core/data/header"
import { useRouter } from 'vue-router'
let router = useRouter()
function logout() {

    router.replace('/auth/login');
    localStorage.clear('user')
}
</script>