<template>
    <div class="d-flex profile-media align-items-center">
        <img class="img-30" src="@/assets/images/dashboard/profile.png" alt="">
        <div class="flex-grow-1">
            <span>{{ currentUser ? currentUser.username : 'Guest' }}</span>
            <p class="mb-0 font-outfit">{{ userRole }}<i class="fa fa-angle-down"></i></p>
        </div>
    </div>
    <ul class="profile-dropdown onhover-show-div">
        <li v-for="(item, index) in profile" :key="index">
            <router-link :to="item.path">
                <vue-feather :type="item.icon"></vue-feather>
                <span>{{ item.title }}</span>
            </router-link>
        </li>
        <li>
            <a @click="handleLogout">
                <vue-feather type="log-out"></vue-feather>
                <span>Log Out</span>
            </a>
        </li>
    </ul>
</template>

<script lang="ts" setup>
import { computed, onMounted } from 'vue'
import { profile } from "@/core/data/header"
import { useAuthStore } from '@/store/auth'
import { useRouter } from 'vue-router'

const router = useRouter()
const authStore = useAuthStore()
const { currentUser, logout } = authStore

const userRole = computed(() => {
    if (!currentUser) return 'Guest'
    if (currentUser.is_superuser) return 'Admin'
    if (currentUser.is_staff) return 'Staff'
    return 'User'
})

const handleLogout = async () => {
    await logout()
    router.push('/auth/login')
}

onMounted(() => {
    // No need to call checkAuth() here, as it's handled by useAuth
})
</script>