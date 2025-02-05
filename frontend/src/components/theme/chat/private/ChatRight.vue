<template>
    <div class="col-xxl-9 col-xl-8 col-md-7 box-col-7">
        <div class="card right-sidebar-chat">
            <div v-if="currentChat" class="card-header chat-header">
                <div class="d-flex align-items-center">
                    <div class="status-indicator" :class="userPresenceClass"></div>
                    <div class="ms-3">
                        <h5 class="mb-0">{{ formatUserName(currentChat.user) }}</h5>
                        <small class="text-muted">{{ isOnline ? 'Online' : 'Offline' }}</small>
                    </div>
                </div>
            </div>
            
            <div v-if="currentChat" class="card-body chat-body p-3">
                <div class="messages-container" ref="messagesContainer">
                    <div v-for="message in sortedMessages" 
                         :key="message.id"
                         class="d-flex mb-3"
                         :class="{'justify-content-end': isCurrentUserMessage(message)}">
                        <div class="message" 
                             :class="{
                                 'message-sent': isCurrentUserMessage(message),
                                 'message-received': !isCurrentUserMessage(message)
                             }">
                            <div class="message-bubble">
                                <div class="message-sender small text-muted">
                                    {{ formatSenderName(message.sender) }}
                                </div>
                                <div class="message-content">{{ message.content }}</div>
                                <div class="message-time small text-end">
                                    {{ formatMessageTime(message.time || message.created_at) }}
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <div v-if="currentChat" class="card-footer chat-footer">
                <form @submit.prevent="sendMessage" class="d-flex gap-2">
                    <input 
                        v-model="newMessage"
                        type="text"
                        placeholder="Type your message..."
                        class="form-control rounded-pill"
                    />
                    <button type="submit" class="btn btn-primary rounded-circle">
                        <i class="fa fa-paper-plane"></i>
                    </button>
                </form>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, computed, watch, nextTick } from 'vue'
import { useChatStore } from '@/store/chat'
import { useAuth } from '@/composables/useAuth'

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
const auth = useAuth()
const messagesContainer = ref<HTMLElement | null>(null)

const newMessage = ref('')
const currentUserId = computed(() => auth.currentUser.value?.id)
const currentChat = computed(() => {
    const chat = chatStore.currentChat
    if (!chat) return null;

    return {
        ...chat,
        messages: chat.messages.map(msg => ({
            ...msg,
            sender: msg.sender || {},
            content: msg.content || msg.text
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
    if (!currentChat.value) return '';
    
    const isSupportUser = auth.currentUser.value?.email === 'mdpssupport@metoffice.gov.tt';
    const otherParticipant = currentChat.value.user;
    
    if (isSupportUser) {
        return `${otherParticipant?.first_name || ''} ${otherParticipant?.last_name || otherParticipant?.username || ''}`.trim();
    } else {
        return 'MDPS Support';
    }
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

const formatUserName = (user) => {
    if (!user) return '';
    
    const isSupportUser = user.email === 'mdpssupport@metoffice.gov.tt';
    if (isSupportUser) {
        return 'MDPS Support';
    }
    
    return `${user.first_name || ''} ${user.last_name || user.username || ''}`.trim();
}

const sortedMessages = computed(() => {
    if (!currentChat.value?.messages) return [];
    
    console.log('Current Chat Messages:', currentChat.value.messages);
    console.log('Current User:', auth.currentUser.value);
    console.log('Is Support User:', auth.currentUser.value?.email === 'mdpssupport@metoffice.gov.tt');
    
    const messages = [...currentChat.value.messages].sort((a, b) => 
        new Date(a.created_at).getTime() - new Date(b.created_at).getTime()
    );
    
    console.log('Sorted Messages:', messages);
    console.log('Message Senders:', messages.map(m => ({
        senderId: m.sender?.id,
        senderEmail: m.sender?.email,
        content: m.content
    })));
    
    return messages;
})

const isCurrentUserMessage = (message: Message) => {
    console.log('Checking message ownership:', {
        messageId: message.id,
        senderId: message.sender?.id,
        currentUserId: currentUserId.value,
        content: message.content,
        isSupportUser: auth.currentUser.value?.email === 'mdpssupport@metoffice.gov.tt'
    });
    
    if (!currentUserId.value) return false;
    
    // For MDPS Support, show all messages in the chat
    if (auth.currentUser.value?.email === 'mdpssupport@metoffice.gov.tt') {
        return true;
    }
    
    return message.sender?.id === currentUserId.value;
}
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
</style>