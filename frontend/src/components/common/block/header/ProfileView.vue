<template>
    <div class="d-flex profile-media align-items-center">
        <img class="img-30" src="@/assets/images/dashboard/profile.png" alt="">
        <div class="flex-grow-1">
            <span>{{ currentUser?.name || 'Guest' }}</span>
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
import { useAuth } from '@/composables/useAuth'
import { useRouter } from 'vue-router'

const router = useRouter()
const { currentUser, logout, checkAuth } = useAuth()

const userRole = computed(() => {
    if (!currentUser.value) return 'Guest'
    if (currentUser.value.is_superuser) return 'Admin'
    if (currentUser.value.is_staff) return 'Staff'
    return 'User'
})

const handleLogout = async () => {
    await logout()
    router.push('/auth/login')
}

onMounted(async () => {
    await checkAuth()
})
</script>