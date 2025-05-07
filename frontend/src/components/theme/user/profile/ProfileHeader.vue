<template>
    <div class="col-sm-12">
        <div class="card hovercard text-center">
            <div class="cardheader"></div>
            <div class="user-image">
                <div class="avatar">
                    <img alt="Profile" src="@/assets/images/user/7.jpg">
                </div>
                <div class="icon-wrapper">
                    <i class="icofont icofont-pencil-alt-5"></i>
                </div>
            </div>
            <div class="info">
                <div class="row">
                    <div class="col-sm-6 col-lg-4 order-sm-1 order-xl-0">
                        <div class="row">
                            <div class="col-md-6">
                                <div class="ttl-info text-start">
                                    <h6><i class="fa fa-envelope"></i> Email</h6>
                                    <span>{{ email }}</span>
                                </div>
                            </div>
                            <div class="col-md-6">
                                <div class="ttl-info text-start">
                                    <h6><i class="fa fa-calendar"></i> Date Created</h6>
                                    <span>{{ formatDate(dateCreated) }}</span>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="col-sm-12 col-lg-4 order-sm-0 order-xl-1">
                        <div class="user-designation">
                            <div class="title">
                                <a href="#">{{ username }}</a>
                            </div>
                            <div class="desc">{{ subscription }}</div>
                        </div>
                    </div>
                    <div class="col-sm-6 col-lg-4 order-sm-2 order-xl-2">
                        <div class="row">
                            <div class="col-md-6">
                                <div class="ttl-info text-start">
                                    <h6><i class="fa fa-user"></i> Role</h6>
                                    <span>{{ role }}</span>
                                </div>
                            </div>
                            <div class="col-md-6">
                                <div class="ttl-info text-start">
                                    <h6><i class="fa fa-info-circle"></i> Status</h6>
                                    <span :class="statusClass">{{ status }}</span>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script lang="ts" setup>
import { ref, computed, watch } from 'vue'
import { useRoute } from 'vue-router'
import { useAuthStore } from '@/store/auth'
import { useUserStore } from '@/store/user'

const authStore = useAuthStore()
const currentUser = computed(() => authStore.currentUser)
const route = useRoute()
const userStore = useUserStore()

const userId = computed(() => route.query.id)
const userFromStore = computed(() => {
  if (!userId.value) return null
  return userStore.users.find(u => u.id === parseInt(userId.value as string))
})

const username = ref('')
const subscription = ref('')
const dateCreated = ref('')
const email = ref('')
const role = ref('')
const status = ref('')

const setUserData = (user: any) => {
    if (!user) return
    username.value = user.username || `${user.first_name} ${user.last_name}`.trim()
    email.value = user.email || ''
    role.value = user.role || (user.is_superuser ? 'Admin' : user.is_staff ? 'Staff' : 'User')
    status.value = user.status || 'Active'
    subscription.value = user.package || 'No Package'
    dateCreated.value = user.created_at || new Date().toISOString()
}

watch(() => route.query.id, async (newId) => {
    if (newId) {
        if (!userStore.initialized) await userStore.fetchUsers()
        const user = userStore.users.find(u => u.id === parseInt(newId as string))
        if (user) {
            setUserData(user)
        }
    } else if (currentUser.value) {
        setUserData(currentUser.value)
    }
}, { immediate: true })

// Watch for currentUser changes
watch(currentUser, (newUser) => {
    if (!route.query.id && newUser) {
        setUserData(newUser)
    }
}, { immediate: true })

const statusClass = computed(() => {
    return {
        'text-success': status.value === 'Active',
        'text-warning': status.value === 'Pending',
        'text-danger': status.value === 'Suspended',
        'text-muted': status.value === 'Inactive'
    }
})

const formatDate = (date: string) => {
    if (!date) return 'N/A'
    return new Date(date).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    })
}
</script>

<style scoped>
.user-image {
    position: relative;
    margin-bottom: 2rem;
}

.avatar img {
    width: 120px;
    height: 120px;
    border-radius: 50%;
    border: 5px solid #fff;
    box-shadow: 0 0 20px rgba(0,0,0,0.1);
}

.api-stats {
    padding: 1rem;
    text-align: center;
    border-radius: 8px;
    background: #f8f9fa;
    transition: all 0.3s ease;
}

.api-stats:hover {
    background: #e9ecef;
    transform: translateY(-2px);
}

.api-stats h3 {
    font-size: 1.5rem;
    font-weight: 600;
    margin-bottom: 0.5rem;
    color: #1a237e;
}

.api-stats p {
    color: #666;
    margin: 0;
    font-size: 0.9rem;
    font-weight: 500;
}

.user-designation .title {
    font-size: 1.5rem;
    font-weight: 600;
    margin-bottom: 0.5rem;
}

.user-designation .desc {
    color: #2196f3;
    font-weight: 500;
}

.ttl-info {
    padding: 1rem;
    background: #f8f9fa;
    border-radius: 8px;
    margin-bottom: 1rem;
}

.ttl-info h6 {
    color: #666;
    margin-bottom: 0.5rem;
}

.ttl-info span {
    color: #333;
    font-weight: 500;
}

.text-success {
    color: #28a745;
}

.text-warning {
    color: #ffc107;
}

.text-danger {
    color: #dc3545;
}

.text-muted {
    color: #6c757d;
}
</style>