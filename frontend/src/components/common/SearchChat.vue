<template>
    <div class="col-xxl-3 col-xl-4 col-md-5 box-col-5">
        <div class="left-sidebar-wrapper card">
            <div class="left-sidebar-chat">
                <div class="input-group">
                    <span class="input-group-text">
                        <vue-feather class="search-icon text-gray" type="search"></vue-feather>
                    </span>
                    <input class="form-control" 
                           type="text" 
                           placeholder="Search here.." 
                           v-model="search"
                           @keyup="setSerchUsers">
                </div>
            </div>
            <div class="advance-options">
                <ul class="nav border-tab" id="chat-options-tab" role="tablist">
                    <li class="nav-item">
                        <a class="nav-link active">Chats</a>
                    </li>
                </ul>
                <div class="tab-content">
                    <div class="tab-pane fade show active">
                        <div class="common-space">
                            <p>Recent chats</p>
                        </div>
                        <ul class="chats-user" v-if="!search">
                            <li class="common-space" 
                                v-for="(chat, index) in displayChats" 
                                :key="chat.id"
                                @click="setActiveChat(chat)">
                                <div class="chat-time">
                                    <div class="active-profile">
                                        <img class="img-fluid rounded-circle" 
                                             :src="chat.user?.avatar || getImages('user/1.jpg')" 
                                             alt="user">
                                        <div class="status" 
                                             :class="{ 
                                                 'bg-success': isUserOnline(chat.user),
                                                 'bg-danger': !isUserOnline(chat.user)
                                             }">
                                        </div>
                                    </div>
                                    <div>
                                        <span>{{ formatUserName(chat.user) }}</span>
                                        <p>{{ getLastMessage(chat) }}</p>
                                    </div>
                                </div>
                                <div>
                                    <p>{{ formatTime(chat.lastMessageTime.toISOString()) }}</p>
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
const search = ref('')
const searchQuery = ref('')

interface User {
    id: number;
    username: string;
    email: string;
    first_name?: string;
    last_name?: string;
    support_chat?: boolean;  // Changed from has_support_chat to match backend
}

interface Message {
    id: number;
    content: string;
    chat_id: number;
    sender: User;
    created_at: string;
    read_at: string | null;
    isCurrentUser?: boolean;
    alignment?: string;
    time?: string;
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

interface Chat {
    id: number;
    name: string;
    user: User;
    messages: Message[];
    participants: User[];
    support_chat: boolean;
    created_at: string;
}

interface ProcessedChat extends Chat {
    lastMessageTime: Date;
    messages: Message[];
    unread_count?: number;
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

const formatUserName = (user: User) => {
    if (!user) return '';
    return `${user.first_name || ''} ${user.last_name || user.username || ''}`.trim();
}

const getLastMessage = (chat: ProcessedChat) => {
    const lastMessage = chat.messages[chat.messages.length - 1];
    return lastMessage?.content || 'No messages yet';
}

const setActiveChat = async (chat: ProcessedChat) => {
    console.log('Setting Active Chat:', chat);
    console.log('Chat User:', chat.user);
    await chatStore.setActiveChat(chat as unknown as Chat);
}

const isUserOnline = (user: User) => {
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

function setSerchUsers() {
    if (search.value !== '') {
        chatStore.setSearchUsers(search.value)
    }
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