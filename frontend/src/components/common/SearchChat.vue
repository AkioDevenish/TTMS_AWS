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
                           v-model="searchQuery"
                           @input="handleSearch">
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
                            <p>{{ searchQuery ? 'Search Results' : 'Recent chats' }}</p>
                        </div>
                        <ul class="chats-user" v-if="searchQuery">
                            <li class="common-space chat-user-item" 
                                v-for="user in filteredUsers" 
                                :key="user.id"
                                @click="startChat(user)">
                                <div class="chat-time">
                                    <div class="active-profile">
                                        <div v-if="(user as any).avatar && (user as any).avatar !== '120 x 120'" class="avatar-container">
                                            <img class="img-fluid rounded-circle" 
                                                 :src="(user as any).avatar" 
                                                 alt="user">
                                        </div>
                                        <div v-else class="avatar-fallback">
                                            <span class="avatar-initials">{{ getUserInitials(user) }}</span>
                                        </div>
                                    </div>
                                    <div class="user-info">
                                        <span class="user-name">{{ formatUserName(user) }}</span>
                                        <p class="user-status">Click to start chat</p>
                                    </div>
                                </div>
                            </li>
                        </ul>
                        <ul class="chats-user" v-else>
                            <li class="common-space chat-user-item" 
                                v-for="user in chatStore.users" 
                                :key="user.id"
                                @click="startChat(user)">
                                <div class="chat-time">
                                    <div class="active-profile">
                                        <div v-if="(user as any).avatar && (user as any).avatar !== '120 x 120'" class="avatar-container">
                                            <img class="img-fluid rounded-circle" 
                                                 :src="(user as any).avatar" 
                                                 alt="user">
                                        </div>
                                        <div v-else class="avatar-fallback">
                                            <span class="avatar-initials">{{ getUserInitials(user) }}</span>
                                        </div>
                                    </div>
                                    <div class="user-info">
                                        <span class="user-name">{{ formatUserName(user) }}</span>
                                        <p class="user-status">Click to view chat</p>
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
import { ref, computed, onMounted, watch } from 'vue'
import { useChatStore } from '@/store/chat'
import { getImages } from '@/composables/common/getImages'
import { useAuthStore } from '@/store/auth'

const chatStore = useChatStore()
const authStore = useAuthStore()
const currentUser = computed(() => authStore.currentUser)
const searchQuery = ref('')

// Use the User interface from the chat store
type User = {
    id: number;
    username: string;
    email: string;
    first_name?: string;
    last_name?: string;
    support_chat?: boolean;
    avatar?: string;
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
    console.log('SearchChat mounted');
    await chatStore.init();
    await chatStore.fetchAllChats();
    await chatStore.fetchAllUsers();
    console.log('Initialization complete');
})

const displayChats = computed(() => {
    return chatStore.chats.sort((a, b) => 
        b.lastMessageTime.getTime() - a.lastMessageTime.getTime()
    );
})

const filteredUsers = computed(() => {
    if (!searchQuery.value) return chatStore.users
    
    const query = searchQuery.value.toLowerCase()
    return chatStore.users.filter(user => {
        const fullName = formatUserName(user).toLowerCase()
        const username = user.username?.toLowerCase() || ''
        const email = user.email.toLowerCase()
        
        return fullName.includes(query) || 
               username.includes(query) || 
               email.includes(query)
    })
})

const formatUserName = (user: User) => {
    if (!user) return '';
    return `${user.first_name || ''} ${user.last_name || user.username || ''}`.trim();
}

const getUserInitials = (user: User) => {
    if (!user) return '';
    const firstName = user.first_name || '';
    const lastName = user.last_name || '';
    const username = user.username || '';
    
    if (firstName && lastName) {
        return `${firstName.charAt(0)}${lastName.charAt(0)}`.toUpperCase();
    } else if (firstName) {
        return firstName.charAt(0).toUpperCase();
    } else if (lastName) {
        return lastName.charAt(0).toUpperCase();
    } else if (username) {
        return username.charAt(0).toUpperCase();
    }
    return '?';
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

const handleSearch = () => {
    // Debounce the search if needed
    if (searchQuery.value.length >= 2) {
        chatStore.fetchAllUsers() // Refresh user list
    }
}

const startChat = async (user: User) => {
    const chat = await chatStore.setActiveuser(user)
    if (chat) {
        await setActiveChat(chat as ProcessedChat)
    }
    searchQuery.value = '' // Clear search after starting chat
}

// Add this watch effect to update user list when new messages arrive
watch(() => chatStore.messages, async () => {
    if (currentUser.value?.email === 'mdpssupport@metoffice.gov.tt') {
        // Refresh user list for MDPS support when new messages arrive
        await chatStore.fetchAllUsers();
    }
}, { deep: true });
</script>

<style lang="scss" scoped>
/* Chat Layout Improvements */
.left-sidebar-wrapper {
    background: white;
    border-radius: 12px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
    border: 1px solid #e9ecef;
    height: calc(100vh - 120px);
    overflow: hidden;
}

.left-sidebar-chat {
    padding: 1.5rem;
    border-bottom: 1px solid #e9ecef;
}

.input-group {
    .form-control {
        border: 2px solid #e9ecef;
        border-radius: 8px;
        padding: 0.75rem 1rem;
        font-size: 0.95rem;
        transition: all 0.3s ease;
        
        &:focus {
            border-color: #667eea;
            box-shadow: 0 0 0 0.2rem rgba(102, 126, 234, 0.25);
            outline: none;
        }
        
        &::placeholder {
            color: #adb5bd;
            font-style: italic;
        }
    }
    
    .input-group-text {
        background: #f8f9fa;
        border: 2px solid #e9ecef;
        border-right: none;
        border-radius: 8px 0 0 8px;
        color: #6c757d;
    }
}

.advance-options {
    padding: 1rem 1.5rem;
    
    .nav-tabs {
        border-bottom: 2px solid #e9ecef;
        
        .nav-link {
            border: none;
            color: #6c757d;
            font-weight: 600;
            padding: 0.75rem 1rem;
            margin-right: 1rem;
            border-radius: 0;
            transition: all 0.3s ease;
            
            &.active {
                color: #667eea;
                border-bottom: 2px solid #667eea;
                background: transparent;
            }
            
            &:hover {
                color: #667eea;
                border-bottom: 2px solid #667eea;
            }
        }
    }
}

.common-space {
    padding: 1rem 0;
    border-bottom: 1px solid #f8f9fa;
    transition: all 0.3s ease;
    cursor: pointer;
    
    &:hover {
        background: #f8f9fa;
        transform: translateX(5px);
    }
    
    &:last-child {
        border-bottom: none;
    }
    
    p {
        margin: 0;
        font-size: 0.9rem;
        color: #6c757d;
        font-weight: 500;
    }
}

.chat-time {
    display: flex;
    align-items: center;
    gap: 1rem;
}

.active-profile {
    position: relative;
    
    .avatar-container {
        width: 50px;
        height: 50px;
        border-radius: 50%;
        overflow: hidden;
        border: 2px solid #e9ecef;
        transition: all 0.3s ease;
        
        &:hover {
            border-color: #667eea;
            transform: scale(1.05);
        }
        
        img {
            width: 100%;
            height: 100%;
            object-fit: cover;
        }
    }
    
    .avatar-fallback {
        width: 50px;
        height: 50px;
        border-radius: 50%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        display: flex;
        align-items: center;
        justify-content: center;
        border: 2px solid #e9ecef;
        transition: all 0.3s ease;
        
        &:hover {
            border-color: #667eea;
            transform: scale(1.05);
        }
        
        .avatar-initials {
            color: white;
            font-weight: 600;
            font-size: 1.2rem;
            text-transform: uppercase;
        }
    }
}

.user-info {
    flex: 1;
    
    .user-name {
        display: block;
        font-weight: 600;
        color: #495057;
        font-size: 1rem;
        margin-bottom: 0.25rem;
    }
    
    .user-status {
        margin: 0;
        font-size: 0.85rem;
        color: #6c757d;
        font-style: italic;
    }
}

/* Dark Mode Support */
body.dark-only {
    .left-sidebar-wrapper {
        background: #2a2b36 !important;
        border-color: #3a3b46 !important;
        color: white !important;
    }
    
    .left-sidebar-chat {
        border-bottom-color: #3a3b46 !important;
    }
    
    .input-group {
        .form-control {
            background: #1d1e26 !important;
            border-color: #3a3b46 !important;
            color: white !important;
            
            &::placeholder {
                color: rgba(255, 255, 255, 0.6) !important;
            }
        }
        
        .input-group-text {
            background: #1d1e26 !important;
            border-color: #3a3b46 !important;
            color: #e9ecef !important;
        }
    }
    
    .advance-options {
        .nav-tabs {
            border-bottom-color: #3a3b46 !important;
            
            .nav-link {
                color: #adb5bd !important;
                
                &.active {
                    color: #667eea !important;
                    border-bottom-color: #667eea !important;
                }
                
                &:hover {
                    color: #667eea !important;
                    border-bottom-color: #667eea !important;
                }
            }
        }
    }
    
    .common-space {
        border-bottom-color: #3a3b46 !important;
        
        &:hover {
            background: #1d1e26 !important;
        }
        
        p {
            color: #adb5bd !important;
        }
    }
    
    .active-profile {
        .avatar-container,
        .avatar-fallback {
            border-color: #3a3b46 !important;
        }
    }
    
    .user-info {
        .user-name {
            color: #e9ecef !important;
        }
        
        .user-status {
            color: #adb5bd !important;
        }
    }
}

/* Responsive Design */
@media (max-width: 768px) {
    .left-sidebar-wrapper {
        height: auto;
        margin-bottom: 1rem;
    }
    
    .chat-time {
        gap: 0.75rem;
    }
    
    .active-profile {
        .avatar-container,
        .avatar-fallback {
            width: 40px;
            height: 40px;
        }
    }
    
    .user-info {
        .user-name {
            font-size: 0.9rem;
        }
        
        .user-status {
            font-size: 0.8rem;
        }
    }
}
</style>