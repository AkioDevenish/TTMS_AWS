<template>
    <div class="col-xxl-9 col-xl-8 col-md-7 box-col-7">
        <div class="card right-sidebar-chat">
            <div class="right-sidebar-title">
                <div class="common-space">
                    <div class="chat-time" v-if="currentChat">
                        <div class="active-profile">
                            <img class="img-fluid rounded-circle" 
                                 :src="currentChat?.user?.avatar || getImages('user/1.jpg')" 
                                 alt="user">
                        </div>
                        <div>
                            <span>{{ chatName }}</span>
                        </div>
                    </div>
                    <div v-else>
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
                                <img class="rounded-circle chat-user-img img-30"
                                     :src="getImages('user/1.jpg')"
                                     :class="{ 
                                         'float-start': isSupportUser(message.sender),
                                         'float-end': !isSupportUser(message.sender)
                                     }"
                                     alt="">
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
</script>

<style lang="scss" scoped>
.chat-header {
    padding: 1rem;
    border-bottom: 1px solid #e9ecef;
    background: white;
}

.status-indicator {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    display: inline-block;
    margin-right: 8px;
    
    &.online {
        background-color: #28a745;
    }
    
    &.offline {
        background-color: #dc3545;
    }
}

.chat-body {
    height: calc(100vh - 180px);
    overflow-y: auto;
    background-color: #f8f9fa;
    padding: 1.5rem;
}

.messages-container {
    display: flex;
    flex-direction: column;
    gap: 1rem;
}

.message {
    display: flex;
    max-width: 80%;
    
    &.message-sent {
        margin-left: auto;
        
        .message-bubble {
            background-color: #6f42c1;
            color: white;
            border-radius: 15px 15px 0 15px;
            
            .message-time, .message-sender {
                color: rgba(255, 255, 255, 0.8);
            }
        }
    }
    
    &.message-received {
        margin-right: auto;
        
        .message-bubble {
            background-color: white;
            color: #212529;
            border-radius: 15px 15px 15px 0;
            box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
        }
    }
}

.message-bubble {
    padding: 0.8rem 1rem;
    min-width: 120px;
}

.message-sender {
    font-size: 0.875rem;
    margin-bottom: 0.25rem;
    font-weight: 500;
}

.message-content {
    word-break: break-word;
    line-height: 1.4;
}

.message-time {
    font-size: 0.75rem;
    margin-top: 0.25rem;
    opacity: 0.8;
}

.chat-footer {
    padding: 1rem;
    background: white;
    border-top: 1px solid #e9ecef;
    
    form {
        display: flex;
        gap: 0.5rem;
    }
    
    .form-control {
        border-radius: 20px;
        padding: 0.5rem 1rem;
        border: 1px solid #e9ecef;
        
        &:focus {
            box-shadow: none;
            border-color: #6f42c1;
        }
    }
    
    .btn-primary {
        width: 40px;
        height: 40px;
        padding: 0;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        background-color: #6f42c1;
        border-color: #6f42c1;
        
        &:hover {
            background-color: darken(#6f42c1, 5%);
            border-color: darken(#6f42c1, 5%);
        }
        
        i {
            font-size: 1.2rem;
        }
    }
}

// Custom scrollbar
.chat-body {
    &::-webkit-scrollbar {
        width: 6px;
    }
    
    &::-webkit-scrollbar-track {
        background: #f1f1f1;
    }
    
    &::-webkit-scrollbar-thumb {
        background: #c5c5c5;
        border-radius: 3px;
    }
    
    &::-webkit-scrollbar-thumb:hover {
        background: #a8a8a8;
    }
}

.user-status {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    
    .status {
        width: 12px;
        height: 12px;
        border-radius: 50%;
        border: 2px solid white;
    }
    
    .status-text {
        font-size: 0.875rem;
    }
}

.bg-success {
    background-color: #28a745;
}

.bg-danger {
    background-color: #dc3545;
}
</style>