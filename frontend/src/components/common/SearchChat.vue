<template>
    <div class="col-xxl-3 col-xl-4 col-md-5 box-col-5">
        <div class="left-sidebar-wrapper card">
            <div class="advance-options">
                <div class="tab-content pt-0">
                    <div class="tab-pane fade show active">
                        <ul class="chats-user mt-0">
                            <li v-for="chat in displayChats" 
                                :key="chat.id" 
                                @click="setActiveChat(chat)">
                                <div class="chat-time">
                                    <div class="active-profile">
                                        <div class="status" 
                                             :class="isUserOnline(chat.user) ? 'bg-success' : 'bg-danger'">
                                        </div>
                                    </div>
                                    <div class="chat-info">
                                        <span>{{ formatUserName(chat.user) }}</span>
                                        <p class="text-muted text-truncate">
                                            {{ getLastMessage(chat) }}
                                        </p>
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

const displayChats = computed(() => {
    return chatStore.chats.sort((a, b) => 
        b.lastMessageTime.getTime() - a.lastMessageTime.getTime()
    );
})

const formatUserName = (user) => {
    if (!user) return '';
    return `${user.first_name || ''} ${user.last_name || user.username || ''}`.trim();
}

const getLastMessage = (chat) => {
    const lastMessage = chat.messages[chat.messages.length - 1];
    return lastMessage?.content || 'No messages yet';
}

const setActiveChat = async (chat) => {
    await chatStore.setActiveChat(chat);
}

const isUserOnline = (user) => {
    const presence = chatStore.userPresences.get(user?.id || 0)
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