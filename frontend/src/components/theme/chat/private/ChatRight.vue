<template>
    <div class="col-xxl-9 col-xl-8 col-md-7 box-col-7">
        <div class="card right-sidebar-chat">
            <div class="right-sidebar-title">
                <div class="common-space">
                    <div class="chat-time" v-if="currentChat">
                        <div class="active-profile">
                            <div v-if="(currentChat?.user as any)?.avatar && (currentChat?.user as any)?.avatar !== '120 x 120'" class="avatar-container">
                                <img class="img-fluid rounded-circle" 
                                     :src="(currentChat.user as any).avatar" 
                                     alt="user">
                            </div>
                            <div v-else class="avatar-fallback">
                                <span class="avatar-initials">{{ getUserInitials(currentChat.user) }}</span>
                            </div>
                        </div>
                        <div class="chat-header-info">
                            <span class="chat-name">{{ chatName }}</span>
                            <div class="chat-status">
                                <span class="status-indicator online"></span>
                                <span class="status-text">Online</span>
                            </div>
                        </div>
                    </div>
                    <div v-else class="no-chat-selected">
                        <div class="no-chat-icon">
                            <svg width="48" height="48" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                                <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                            </svg>
                        </div>
                        <p>Select a chat to start messaging</p>
                    </div>
                </div>
            </div>

            <div class="right-sidebar-Chats" v-if="currentChat">
                <div class="msger">
                    <div class="msger-chat" ref="messagesContainer">
                        <div v-for="message in sortedMessages" 
                             :key="message.id"
                             class="msg"
                             :class="[
                                 { clearfix: message.sender?.email === 'mdpssupport@metoffice.gov.tt' },
                                 { 'right-msg': !isSupportUser(message.sender) },
                                 { 'left-msg': isSupportUser(message.sender) }
                             ]">
                            <div class="msg-img">
                                <div v-if="(message.sender as any)?.avatar && (message.sender as any)?.avatar !== '120 x 120'" class="avatar-container">
                                    <img class="rounded-circle chat-user-img"
                                         :src="(message.sender as any).avatar"
                                         :class="{ 
                                             'float-start': isSupportUser(message.sender),
                                             'float-end': !isSupportUser(message.sender)
                                         }"
                                         alt="">
                                </div>
                                <div v-else class="avatar-fallback">
                                    <span class="avatar-initials">{{ getMessageSenderInitials(message.sender) }}</span>
                                </div>
                            </div>
                            <div class="msg-bubble">
                                <div class="msg-info" :class="{ 'text-start': isSupportUser(message.sender) }">
                                    <div class="msg-info-name">{{ formatSenderName(message.sender) }}</div>
                                    <div class="msg-info-time">{{ formatMessageTime(message.created_at) }}</div>
                                </div>
                                <div class="msg-text">{{ message.content }}</div>
                            </div>
                        </div>
                    </div>
                    <AddChat />
                </div>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, computed, watch, nextTick } from 'vue'
import { useChatStore } from '@/store/chat'
import { useAuthStore } from '@/store/auth'
import { getImages } from '@/composables/common/getImages'
import AddChat from './AddChat.vue'

interface MessageSender {
    id: number;
    username: string;
    email: string;
    first_name?: string;
    last_name?: string;
    avatar?: string;
}

interface Message {
    id: number;
    content?: string;
    text?: string;
    time?: string;
    created_at: string;
    sender: {
        id: number;
        first_name?: string;
        last_name?: string;
        username?: string;
        email: string;
        avatar?: string;
    };
}

const chatStore = useChatStore()
const authStore = useAuthStore()
const messagesContainer = ref<HTMLElement | null>(null)

const newMessage = ref('')
const currentUser = computed(() => authStore.currentUser)
const currentUserId = computed(() => currentUser.value?.id)
const currentChat = computed(() => {
    const chat = chatStore.currentChat
    if (!chat) return null;

    // Find the actual user object from participants
    const chatUser = chat.participants?.find(p => p.id === Number(chat.user))
    
    return {
        ...chat,
        user: chatUser,
        messages: chat.messages.map(msg => ({
            ...msg,
            sender: msg.sender || {},
            content: msg.content
        }))
    };
})

const isOnline = computed(() => {
    if (!currentChat.value?.user?.id) return false
    const presence = chatStore.userPresences.get(currentChat.value.user.id)
    return presence?.is_online || false
})

const userPresenceClass = computed(() => 
    isOnline.value ? 'online' : 'offline'
)

const isSupportChat = computed(() => currentChat.value?.support_chat ?? false)
const supportUserId = computed(() => chatStore.SUPPORT_USER?.id)

const chatName = computed(() => {
    if (!currentChat.value?.user) return '';
    const user = currentChat.value.user;
    return `${user.first_name || ''} ${user.last_name || user.username || ''}`.trim();
});

function formatMessageTime(timestamp: string) {
    if (!timestamp) return ''
    try {
        const date = new Date(timestamp)
        if (isNaN(date.getTime())) return ''
        return date.toLocaleTimeString([], { 
            hour: '2-digit', 
            minute: '2-digit',
            hour12: true
        })
    } catch (e) {
        return ''
    }
}

function formatSenderName(sender: MessageSender | undefined) {
    if (!sender) return '';
    
    const isSupportUser = sender.email === 'mdpssupport@metoffice.gov.tt';
    if (isSupportUser) {
        return 'MDPS Support';
    }
    
    return `${sender.first_name || ''} ${sender.last_name || sender.username || ''}`.trim();
}

async function sendMessage() {
    if (!newMessage.value.trim()) return
    
    await chatStore.addMessage(newMessage.value)
    newMessage.value = ''
    await scrollToBottom()
}

async function scrollToBottom() {
    await nextTick()
    if (messagesContainer.value) {
        messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
    }
}

// Auto-scroll when new messages arrive
watch(() => currentChat.value?.messages, async () => {
    await scrollToBottom()
}, { deep: true })

// Initial scroll when chat loads
watch(currentChat, async () => {
    await scrollToBottom()
})

const formatUserName = (user: MessageSender) => {
    if (!user) return '';
    return `${user.first_name || ''} ${user.last_name || user.username || ''}`.trim();
};

const sortedMessages = computed(() => {
    if (!currentChat.value?.messages) return [];
    
    return [...currentChat.value.messages].sort((a, b) => 
        new Date(a.created_at).getTime() - new Date(b.created_at).getTime()
    );
});

const isCurrentUserMessage = (message: Message) => {
    if (!currentUserId.value) return false;
    
    // For MDPS Support, show all messages in the chat
    if (currentUser.value?.email === 'mdpssupport@metoffice.gov.tt') {
        return true;
    }
    
    return message.sender?.id === currentUserId.value;
}

const isSupportUser = (sender: MessageSender | undefined) => {
    if (!sender) return false;
    return sender.email === 'mdpssupport@metoffice.gov.tt';
}

// Add these computed properties for avatars
const defaultAvatar = computed(() => '/path/to/default/avatar.jpg')
const userAvatar = computed(() => '/path/to/user/avatar.jpg')

function getUserInitials(user: MessageSender | undefined) {
    if (!user) return '';
    const firstName = user.first_name || '';
    const lastName = user.last_name || '';
    return `${firstName.charAt(0)}${lastName.charAt(0)}`.toUpperCase();
}

function getMessageSenderInitials(sender: MessageSender | undefined) {
    if (!sender) return '';
    const firstName = sender.first_name || '';
    const lastName = sender.last_name || '';
    return `${firstName.charAt(0)}${lastName.charAt(0)}`.toUpperCase();
}
</script>

<style lang="scss" scoped>
/* Chat Right Component Styles */
.right-sidebar-chat {
    background: white;
    border-radius: 12px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
    border: 1px solid #e9ecef;
    height: calc(100vh - 120px);
    overflow: hidden;
    display: flex;
    flex-direction: column;
}

.right-sidebar-title {
    padding: 1.5rem;
    border-bottom: 1px solid #e9ecef;
    background: #f8f9fa;
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

.chat-header-info {
    flex: 1;
    
    .chat-name {
        display: block;
        font-weight: 600;
        color: #495057;
        font-size: 1.1rem;
        margin-bottom: 0.25rem;
    }
    
    .chat-status {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        
        .status-indicator {
            width: 8px;
            height: 8px;
            border-radius: 50%;
            display: inline-block;
            
            &.online {
                background-color: #28a745;
            }
            
            &.offline {
                background-color: #dc3545;
            }
        }
        
        .status-text {
            font-size: 0.85rem;
            color: #6c757d;
        }
    }
}

.no-chat-selected {
    text-align: center;
    padding: 2rem;
    
    .no-chat-icon {
        margin-bottom: 1rem;
        color: #6c757d;
    }
    
    p {
        margin: 0;
        color: #6c757d;
        font-size: 1rem;
    }
}

.right-sidebar-Chats {
    flex: 1;
    display: flex;
    flex-direction: column;
    overflow: hidden;
}

.msger {
    flex: 1;
    display: flex;
    flex-direction: column;
}

.msger-chat {
    flex: 1;
    overflow-y: auto;
    padding: 1.5rem;
    background: #f8f9fa;
    
    &::-webkit-scrollbar {
        width: 6px;
    }
    
    &::-webkit-scrollbar-track {
        background: #e9ecef;
        border-radius: 3px;
    }
    
    &::-webkit-scrollbar-thumb {
        background: #adb5bd;
        border-radius: 3px;
        
        &:hover {
            background: #6c757d;
        }
    }
}

.msg {
    display: flex;
    align-items: flex-end;
    margin-bottom: 1.5rem;
    gap: 0.75rem;
    
    &:last-of-type {
        margin-bottom: 0;
    }
}

.msg-img {
    flex-shrink: 0;
    
    .avatar-container {
        width: 40px;
        height: 40px;
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
        width: 40px;
        height: 40px;
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
            font-size: 1rem;
            text-transform: uppercase;
        }
    }
}

.msg-bubble {
    max-width: 70%;
    padding: 1rem 1.25rem;
    border-radius: 18px;
    position: relative;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.msg-info {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 0.5rem;
    font-size: 0.85rem;
}

.msg-info-name {
    font-weight: 600;
    color: #495057;
}

.msg-info-time {
    color: #6c757d;
    font-size: 0.8rem;
}

.msg-text {
    line-height: 1.4;
    color: #495057;
}

/* Message Alignment */
.left-msg {
    .msg-bubble {
        background: white;
        color: #495057;
        border-bottom-left-radius: 4px;
    }
    
    .msg-info {
        text-align: left;
    }
}

.right-msg {
    flex-direction: row-reverse;
    
    .msg-bubble {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-bottom-right-radius: 4px;
        
        .msg-info-name,
        .msg-info-time,
        .msg-text {
            color: white;
        }
    }
    
    .msg-info {
        text-align: right;
    }
}

/* Dark Mode Support */
body.dark-only {
    .right-sidebar-chat {
        background: #2a2b36 !important;
        border-color: #3a3b46 !important;
        color: white !important;
    }
    
    .right-sidebar-title {
        background: #1d1e26 !important;
        border-bottom-color: #3a3b46 !important;
    }
    
    .active-profile {
        .avatar-container,
        .avatar-fallback {
            border-color: #3a3b46 !important;
        }
    }
    
    .chat-header-info {
        .chat-name {
            color: #e9ecef !important;
        }
        
        .chat-status .status-text {
            color: #adb5bd !important;
        }
    }
    
    .no-chat-selected {
        .no-chat-icon {
            color: #adb5bd !important;
        }
        
        p {
            color: #adb5bd !important;
        }
    }
    
    .msger-chat {
        background: #1d1e26 !important;
    }
    
    .msg-bubble {
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3) !important;
    }
    
    .left-msg .msg-bubble {
        background: #2a2b36 !important;
        color: white !important;
        
        .msg-info-name,
        .msg-info-time,
        .msg-text {
            color: white !important;
        }
    }
    
    .msg-img {
        .avatar-container,
        .avatar-fallback {
            border-color: #3a3b46 !important;
        }
    }
}

/* Responsive Design */
@media (max-width: 768px) {
    .right-sidebar-chat {
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
    
    .msg-img {
        .avatar-container,
        .avatar-fallback {
            width: 35px;
            height: 35px;
        }
    }
    
    .msg-bubble {
        max-width: 85%;
        padding: 0.75rem 1rem;
    }
    
    .msg-info {
        font-size: 0.8rem;
    }
    
    .msg-text {
        font-size: 0.9rem;
    }
}
</style>