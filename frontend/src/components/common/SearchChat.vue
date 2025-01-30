<template>
    <div class="col-xxl-3 col-xl-4 col-md-5 box-col-5">
        <div class="left-sidebar-wrapper card">
            <div class="advance-options">
                <ul class="nav border-tab" id="chat-options-tab" role="tablist">
                    <li class="nav-item">
                        <a class="nav-link active" id="chats-tab" data-bs-toggle="tab" href="#chats"
                            role="tab" aria-controls="chats" aria-selected="true">Support Chats</a>
                    </li>
                </ul>
                <div class="tab-content" id="chat-options-tabContent">
                    <div class="tab-pane fade show active" id="chats" role="tabpanel" aria-labelledby="chats-tab">
                        <!-- Search box -->
                        <div class="search-box">
                            <div class="input-group">
                                <input type="text" class="form-control" v-model="searchQuery" 
                                       placeholder="Search users...">
                            </div>
                        </div>
                        
                        <ul class="chats-user">
                            <li v-for="user in filteredUsers" :key="user.id" 
                                class="common-space" 
                                @click="setActiveuser(user)">
                                <div class="chat-time">
                                    <div class="active-profile">
                                        <img class="img-fluid rounded-circle"
                                            :src="user.avatar || getImages('user/1.jpg')" 
                                            :alt="user.first_name">
                                        <div class="status" 
                                             :class="userPresenceClass(user)">
                                        </div>
                                    </div>
                                    <div>
                                        <span>{{ user.first_name }} {{ user.last_name }}</span>
                                        <p>{{ isUserOnline(user) ? 'Online' : 'Offline' }}</p>
                                    </div>
                                </div>
                                <div>
                                    <div v-if="user.unread_count" 
                                         class="badge badge-light-primary">
                                        {{ user.unread_count }}
                                    </div>
                                </div>
                            </li>
                        </ul>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script lang="ts" setup>
import { ref, computed, onMounted } from 'vue'
import { useChatStore } from '@/store/chat'
import { getImages } from '@/composables/common/getImages'
import { useAuth } from '@/composables/useAuth'

const chatStore = useChatStore()
const { currentUser } = useAuth()
const searchQuery = ref('')

onMounted(async () => {
  await chatStore.init()
})

// Get all users that have contacted support
const filteredUsers = computed(() => {
  // If current user is not support, only show support user
  if (currentUser.value?.email !== 'mdpssupport@metoffice.gov.tt') {
    return chatStore.SUPPORT_USER ? [chatStore.SUPPORT_USER] : []
  }

  // For support user, show all users who have chats
  const uniqueUserIds = new Set<number>()
  const userMap = new Map<number, User>()

  chatStore.chats.forEach(chat => {
    if (!uniqueUserIds.has(chat.user.id) && chat.user.id !== chatStore.SUPPORT_USER?.id) {
      uniqueUserIds.add(chat.user.id)
      userMap.set(chat.user.id, chat.user)
    }
  })

  const users = Array.from(userMap.values())
  
  if (!searchQuery.value) return users
  
  return users.filter(user => 
    user.first_name?.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
    user.last_name?.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
    user.username.toLowerCase().includes(searchQuery.value.toLowerCase())
  )
})

const isUserOnline = (user) => {
  const presence = chatStore.userPresences.get(user.id)
  return presence?.is_online || false
}

const userPresenceClass = (user) => 
  isUserOnline(user) ? 'bg-success' : 'bg-secondary'

const setActiveuser = (user) => {
  chatStore.setActiveuser(user)
}
</script>