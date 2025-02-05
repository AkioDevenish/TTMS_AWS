<template>
    <div class="col-xxl-3 col-xl-4 col-md-5 box-col-5">
        <div class="left-sidebar-wrapper card">
            <div class="advance-options">
                <ul class="nav border-tab mb-0" id="chat-options-tab" role="tablist">
                    <li class="nav-item">
                        <a class="nav-link active py-1" id="chats-tab" data-bs-toggle="tab" href="#chats"
                            role="tab" aria-controls="chats" aria-selected="true">Support Chats</a>
                    </li>
                </ul>
                <div class="tab-content pt-0" id="chat-options-tabContent">
                    <div class="tab-pane fade show active" id="chats" role="tabpanel" aria-labelledby="chats-tab">
                        <ul class="chats-user mt-0">
                            <li v-for="user in filteredUsers" :key="user.id" 
                                @click="setActiveuser(user)">
                                <div class="chat-time">
                                    <div class="active-profile">
                                        <img class="img-fluid rounded-circle"
                                            :src="getImages(user.avatar || 'user.jpg')" 
                                            :alt="user.first_name">
                                        <div class="status" 
                                             :class="isUserOnline(user) ? 'bg-success' : 'bg-danger'">
                                        </div>
                                    </div>
                                    <div class="chat-info">
                                        <span>
                                            {{ `${user.first_name} ${user.last_name || user.username || ''}`.trim() }}
                                        </span>
                                        <p class="text-muted text-truncate">{{ user.last_message?.content || 'No messages yet' }}</p>
                                    </div>
                                </div>
                                <div class="last-message-info">
                                    <small class="text-muted">{{ formatTime(user.last_message?.created_at) }}</small>
                                    <div v-if="user.unread_count" 
                                         class="badge badge-light-primary">
                                        {{ user.unread_count }}
                                    </div>
                                </div>
                            </li>
                        </ul>

                        <!-- Search box -->
                        <div class="search-box p-3">
                            <div class="input-group">
                                <input type="text" class="form-control" v-model="searchQuery" 
                                       placeholder="Search users...">
                            </div>
                        </div>
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
const auth = useAuth()
const searchQuery = ref('')

interface User {
    id: number;
    username: string;
    email: string;
    first_name?: string;
    last_name?: string;
    support_chat?: boolean;  // Changed from has_support_chat to match backend
}

interface DisplayUser {
    id: number;
    first_name: string;
    last_name: string;
    username: string;
    email: string;
    avatar: string;
    chat: ProcessedChat;
    last_message?: Message;
    unread_count: number;
}

onMounted(async () => {
    await chatStore.init();
    await chatStore.fetchAllChats(); // Always fetch chats first
    
    if (auth.currentUser.value?.email === 'mdpssupport@metoffice.gov.tt') {
        await chatStore.fetchAllUsers(); // Only fetch users for MDPS Support
    }
})

const filteredUsers = computed((): DisplayUser[] => {
    const currentUserEmail = auth.currentUser.value?.email;
    const currentUserId = auth.currentUser.value?.id;
    
    if (!chatStore.chats.length) return [];

    return chatStore.chats
        .map(chat => {
            let displayUser;
            
            if (currentUserEmail === 'mdpssupport@metoffice.gov.tt') {
                displayUser = chat.participants.find(p => 
                    p.email !== 'mdpssupport@metoffice.gov.tt'
                );
            } else {
                displayUser = chat.participants.find(p => 
                    p.email === 'mdpssupport@metoffice.gov.tt'
                );
            }
            
            if (!displayUser) return null;

            return {
                id: displayUser.id,
                first_name: currentUserEmail === 'mdpssupport@metoffice.gov.tt'
                    ? (displayUser.first_name || displayUser.username || '')
                    : 'MDPS',
                last_name: currentUserEmail === 'mdpssupport@metoffice.gov.tt'
                    ? (displayUser.last_name || '')
                    : 'Support',
                username: displayUser.username || '',
                email: displayUser.email,
                avatar: 'user/1.jpg',
                chat: {
                    ...chat,
                    name: currentUserEmail === 'mdpssupport@metoffice.gov.tt'
                        ? `${displayUser.first_name || displayUser.username || ''} ${displayUser.last_name || ''}`.trim()
                        : 'MDPS Support'
                },
                last_message: chat.messages[chat.messages.length - 1],
                unread_count: chat.messages.filter(m => 
                    !m.read_at && m.sender.id === displayUser.id
                ).length || 0
            };
        })
        .filter((user): user is DisplayUser => user !== null);
});

const setActiveuser = async (user) => {
    console.log('Setting active user:', user);
    
    if (user.chat) {
        // If chat exists, load it directly
        await chatStore.setActiveChat(user.chat);
    } else {
        // Create new chat and load it
        const chat = await chatStore.setActiveuser(user);
        if (chat) {
            await chatStore.setActiveChat(chat);
            // Refresh chats to update the list
            await chatStore.fetchAllChats();
        }
    }
}

const isUserOnline = (user) => {
    const presence = chatStore.userPresences.get(user.id)
    return presence?.is_online || false
}

const formatTime = (timestamp: string | undefined) => {
    if (!timestamp) return ''
    const date = new Date(timestamp)
    return date.toLocaleTimeString([], { 
        hour: '2-digit', 
        minute: '2-digit',
        hour12: true 
    })
}
</script>

<style lang="scss" scoped>
.nav-link {
    padding-top: 0.25rem;
    padding-bottom: 0.25rem;
}

.chats-user {
    padding-top: 0.5rem;
}

.chat-info {
    flex: 1;
    min-width: 0;
    
    span {
        display: block;
        font-weight: 500;
    }
    
    p {
        margin: 0;
        font-size: 12px;
    }
}

.last-message-info {
    text-align: right;
    min-width: 80px;
}

.status {
    width: 12px;
    height: 12px;
    position: absolute;
    bottom: 0;
    right: 0;
    border-radius: 50%;
    border: 2px solid white;
}

.text-truncate {
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}
</style>