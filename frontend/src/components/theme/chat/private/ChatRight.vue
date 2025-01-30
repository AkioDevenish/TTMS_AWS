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
                    <div v-for="message in currentChat.messages" :key="message.id" 
                         :class="['message', {
                             'sent': message.sender.id === (isSupportChat ? supportUserId : currentUserId),
                             'received': message.sender.id !== (isSupportChat ? supportUserId : currentUserId)
                         }]">
                        <div class="message-content">{{ message.content }}</div>
                        <div class="message-info">
                            <span class="message-time">{{ formatMessageTime(message.created_at) }}</span>
                        </div>
                    </div>
                </div>
            </div>

            <div v-if="currentChat" class="chat-footer">
                <form @submit.prevent="sendMessage" class="message-form">
                    <input v-model="newMessage" 
                           type="text" 
                           placeholder="Type a message..." 
                           class="form-control"
                           @keyup.enter="sendMessage">
                    <button type="submit" class="btn btn-primary">
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

const chatStore = useChatStore()
const auth = useAuth()
const messagesContainer = ref<HTMLElement | null>(null)

const newMessage = ref('')
const currentUserId = computed(() => auth.currentUser.value?.id)
const currentChat = computed(() => chatStore.currentChat)

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

function formatMessageTime(timestamp: string) {
    return new Date(timestamp).toLocaleTimeString([], { 
        hour: '2-digit', 
        minute: '2-digit' 
    })
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
</script>

<style scoped>
.messages-container {
    height: calc(100vh - 300px);
    overflow-y: auto;
    padding: 1rem;
    display: flex;
    flex-direction: column;
}

.message {
    margin-bottom: 1rem;
    max-width: 70%;
    word-wrap: break-word;
}

.message.sent {
    margin-left: auto;
    background-color: #007bff;
    color: white;
    border-radius: 15px 15px 0 15px;
    padding: 10px 15px;
}

.message.received {
    margin-right: auto;
    background-color: #f1f1f1;
    border-radius: 15px 15px 15px 0;
    padding: 10px 15px;
}

.message-info {
    font-size: 0.8rem;
    opacity: 0.7;
    margin-top: 0.25rem;
    text-align: right;
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
</style>