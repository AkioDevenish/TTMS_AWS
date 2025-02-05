<template>
    <div class="col-xxl-9 col-xl-8 col-md-7 box-col-7">
        <div class="card right-sidebar-chat">
            <div v-if="currentChat" class="right-sidebar-title">
                <div class="common-space">
                    <div class="chat-time">
                        <div class="active-profile">
                            <div class="status" :class="userPresenceClass"></div>
                        </div>
                        <div> 
                            <span>{{ currentChat.user?.first_name }} {{ currentChat.user?.last_name }}</span>
                            <p>{{ isOnline ? 'Online' : 'Offline' }}</p>
                        </div>
                    </div>
                </div>
            </div>
            <div v-else class="right-sidebar-title">
                <div class="common-space">
                    <p>Select a chat to start messaging</p>
                </div>
            </div>
            
            <div v-if="currentChat" class="chat-body">
                <div class="messages-container" ref="messagesContainer">
                    <template v-for="(message, index) in currentChat?.messages" :key="message.id">
                        <div class="message"
                            :class="{
                                'sent': message.sender?.id === currentUserId,
                                'received': message.sender?.id !== currentUserId,
                                'message-group': index > 0 && 
                                    currentChat.messages[index - 1].sender?.id === message.sender?.id
                            }">
                            <div class="message-bubble">
                                <div v-if="index === 0 || currentChat.messages[index - 1].sender?.id !== message.sender?.id" 
                                     class="message-sender">
                                    {{ message.sender?.id === currentUserId ? 'You' : 
                                       (message.sender?.first_name ? 
                                        `${message.sender.first_name} ${message.sender.last_name || ''}` : 
                                        'MDPS Support') }}
                                </div>
                                <div class="message-content">{{ message.content }}</div>
                                <div class="message-time">{{ formatMessageTime(message.time || message.created_at) }}</div>
                            </div>
                        </div>
                    </template>
                </div>
            </div>

            <div v-if="currentChat" class="chat-footer">
                <form @submit.prevent="sendMessage" class="message-form">
                    <input 
                        v-model="newMessage"
                        type="text"
                        placeholder="Type your message..."
                        class="form-control"
                    />
                    <button type="button" class="btn btn-secondary emoji-btn" @click="toggleEmojiPicker">
                        <i class="fa fa-smile-o"></i>
                    </button>
                    <button type="submit" class="btn btn-primary">
                        <i class="fa fa-paper-plane"></i>
                    </button>
                </form>
                <div v-if="showEmojiPicker" class="emoji-picker">
                    <EmojiChat @selectEmoji="onSelectEmoji" />
                </div>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, computed, watch, nextTick, defineAsyncComponent } from 'vue'
import { useChatStore } from '@/store/chat'
import { useAuth } from '@/composables/useAuth'
import { ProcessedMessage } from '@/store/chat'

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
    };
}

const chatStore = useChatStore()
const auth = useAuth()
const messagesContainer = ref<HTMLElement | null>(null)

const newMessage = ref('')
const currentUserId = computed(() => auth.currentUser.value?.id)
const currentChat = computed(() => {
    const chat = chatStore.currentChat
    if (chat?.messages) {
        return {
            ...chat,
            messages: chat.messages.map((msg: ProcessedMessage) => ({
                ...msg,
                sender: msg.sender || {},
                content: msg.content || msg.text,
                senderName: msg.senderName,
                time: msg.time || new Date(msg.created_at).toLocaleTimeString([], { 
                    hour: '2-digit', 
                    minute: '2-digit',
                    hour12: true 
                })
            }))
        }
    }
    return chat
})

const isOnline = computed(() => {
    if (!currentChat.value?.user?.id) return false
    const presence = chatStore.userPresences.get(currentChat.value.user.id)
    return presence?.is_online || false
})

const userPresenceClass = computed(() => 
    isOnline.value ? 'bg-success' : 'bg-secondary'
)

const isSupportChat = computed(() => currentChat.value?.support_chat ?? false)
const supportUserId = computed(() => chatStore.SUPPORT_USER?.id)

const EmojiChat = defineAsyncComponent(() => import("@/components/theme/chat/private/EmojiChat.vue"))
const showEmojiPicker = ref(false)

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

function toggleEmojiPicker() {
    showEmojiPicker.value = !showEmojiPicker.value
}

function onSelectEmoji(emoji: string) {
    newMessage.value += emoji
    showEmojiPicker.value = false
}
</script>

<style scoped>
.messages-container {
    height: calc(100vh - 300px);
    overflow-y: auto;
    padding: 1rem;
    display: flex;
    flex-direction: column;
    gap: 1rem;
}

.message {
    margin: 8px 0;
    display: flex;
    flex-direction: column;
}

.sent {
    align-items: flex-end;
}

.received {
    align-items: flex-start;
}

.message-group {
    margin-top: 2px;
}

.message-bubble {
    max-width: 70%;
    padding: 8px 12px;
    border-radius: 12px;
}

.sent .message-bubble {
    background-color: #007bff;
    color: white;
}

.received .message-bubble {
    background-color: #f1f1f1;
    color: black;
}

.message-sender {
    font-weight: bold;
    margin-bottom: 4px;
    font-size: 0.9em;
}

.message-time {
    font-size: 0.8em;
    opacity: 0.7;
    margin-top: 4px;
}

.chat-footer {
    padding: 1rem;
    border-top: 1px solid #eee;
    background: white;
}

.message-form {
    display: flex;
    gap: 1rem;
}

.message-form input {
    flex: 1;
    border-radius: 20px;
    padding: 0.5rem 1rem;
}

.message-form button {
    border-radius: 50%;
    width: 40px;
    height: 40px;
    padding: 0;
    display: flex;
    align-items: center;
    justify-content: center;
}

.emoji-btn {
    border-radius: 50%;
    width: 40px;
    height: 40px;
    padding: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-right: 0.5rem;
}

.emoji-picker {
    position: absolute;
    bottom: 100%;
    right: 1rem;
    z-index: 1000;
    background: white;
    border-radius: 8px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}
</style>