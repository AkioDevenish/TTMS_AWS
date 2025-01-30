import { defineStore } from 'pinia'
import { ref, computed, onBeforeUnmount } from "vue"
import { useAuth } from '@/composables/useAuth'
import axios from 'axios'

interface User {
    id: number;
    username: string;
    email: string;
    role: string;
    is_superuser: boolean;
    is_staff: boolean;
    first_name: string | null;
    last_name: string | null;
}

interface MessageSender {
    id: number;
    username: string;
    first_name: string | null;
    last_name: string | null;
}

interface Message {
    id: number
    content: string
    chat_id: number
    sender: {
        id: number
        username: string
        first_name: string
        last_name: string
    }
    created_at: string
    read_at: string | null
}

interface Chat {
    id: number;
    name: string | null;
    user: User;
    support_chat: boolean;
    messages: Message[];
    created_at: string;
}

interface UserPresence {
    id: number;
    is_online: boolean;
    last_seen: string;
}

export const useChatStore = defineStore('chat', () => {
    const { currentUser } = useAuth()
    const isAdmin = computed(() => currentUser.value?.role === 'admin')
    
    const SUPPORT_USER = ref<User | null>(null)
    const chats = ref<Chat[]>([])
    const activeChat = ref<Chat | null>(null)
    const messages = ref<Message[]>([])
    const searchUser = ref<User[]>([])
    const userPresences = ref<Map<number, UserPresence>>(new Map())
    const users = ref<User[]>([])

    // Helper function to get headers
    const getHeaders = () => ({
        'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
        'Content-Type': 'application/json'
    })

    async function handleLogout() {
        if (currentUser.value) {
            await updateUserPresence(currentUser.value.id, false)
        }
    }

    async function init() {
        try {
            console.log('🟢 Starting chat initialization...')
            
            // Get support user first - no auth check needed
            console.log('🔍 Fetching support user...')
            const supportResponse = await axios.get<User[]>('http://127.0.0.1:8000/api/users/', {
                params: { 
                    email: 'mdpssupport@metoffice.gov.tt'
                }
            });

            console.log('Support API Response:', supportResponse.data);

            // Find the correct support user from the response
            const supportUser = supportResponse.data.find(user => 
                user.email === 'mdpssupport@metoffice.gov.tt' && 
                user.username === 'mdps.support'  // Only check email and username
            );

            if (supportUser) {
                SUPPORT_USER.value = supportUser;
                console.log('✅ Support User Set:', {
                    id: SUPPORT_USER.value.id,
                    email: SUPPORT_USER.value.email,
                    username: SUPPORT_USER.value.username,
                    role: SUPPORT_USER.value.role
                });
            } else {
                console.error('❌ Support user not found in response')
                return;
            }

            // Only check auth for loading chats
            if (!currentUser.value) {
                console.log('🔴 Cannot load chats: No authenticated user')
                return
            }

            // Load chats
            const chatsResponse = await axios.get<Chat[]>('http://127.0.0.1:8000/api/chats/', {
                headers: getHeaders()
            });
            chats.value = chatsResponse.data;
        } catch (error) {
            console.error('❌ Error in init:', error);
            SUPPORT_USER.value = null;
        }
    }

    function setSearchUsers(searchTerm: string) {
        const uniqueUserIds = new Set<number>()
        const userMap = new Map<number, User>()

        chats.value.forEach(chat => {
            chat.messages.forEach(message => {
                if (message.sender.id !== SUPPORT_USER.value?.id && !uniqueUserIds.has(message.sender.id)) {
                    uniqueUserIds.add(message.sender.id)
                    // Get full user data from the chat's user property
                    const chatUser = chats.value.find(c => c.user.id === message.sender.id)?.user
                    if (chatUser) {
                        userMap.set(message.sender.id, chatUser)
                    }
                }
            })
        })

        searchUser.value = Array.from(userMap.values())
            .filter(user => user.username.toLowerCase().includes(searchTerm.toLowerCase()))
    }

    const currentChat = computed(() => {
        if (!activeChat.value) return null
        
        return {
            ...activeChat.value,
            messages: messages.value.filter(m => 
                activeChat.value && m.chat_id === activeChat.value.id
            )
        }
    })

    async function setActiveChat(chatId: number) {
        try {
            // Load messages for the chat
            const response = await axios.get(`http://127.0.0.1:8000/api/chats/${chatId}/messages/`, {
                headers: getHeaders()
            });
            
            const chat = chats.value.find(c => c.id === chatId);
            if (!chat) {
                console.error('Chat not found');
                return;
            }
            
            if (response.data) {
                // Transform the messages to match your Message interface
                const transformedMessages = response.data.map((msg: any) => ({
                    id: msg.id,
                    content: msg.content,
                    chat_id: chatId,
                    sender: {
                        id: msg.sender.id,
                        username: msg.sender.username,
                        first_name: msg.sender.first_name || 'Unknown',
                        last_name: msg.sender.last_name || ''
                    },
                    created_at: msg.created_at,
                    read_at: msg.read_at || null  // Add null as fallback
                }));
                
                // Update both the messages array and the active chat
                messages.value = transformedMessages;
                activeChat.value = {
                    ...chat,
                    messages: transformedMessages
                };
                
                console.log('Messages loaded:', messages.value.length);
            }
        } catch (error) {
            console.error('Error loading messages:', error);
        }
    }

    async function setActiveuser(user: User) {
        try {
            const isSupportChat = SUPPORT_USER.value?.id === user.id;
            
            // First check if a chat exists with this user
            const existingChats = await axios.get<Chat[]>('http://127.0.0.1:8000/api/chats/', {
                params: {
                    user_id: isSupportChat ? currentUser.value?.id : user.id,
                    support_chat: isSupportChat
                },
                headers: getHeaders()
            });

            let chat: Chat | null = null;
            
            if (existingChats.data.length > 0) {
                chat = existingChats.data[0];
                // Update local chats if not present
                if (!chats.value.some(c => c.id === chat?.id)) {
                    chats.value.push(chat);
                }
            } else {
                // Create new chat only if none exists
                const response = await axios.post<Chat>('http://127.0.0.1:8000/api/chats/', {
                    user: isSupportChat ? currentUser.value?.id : user.id,
                    support_chat: isSupportChat
                }, {
                    headers: getHeaders()
                });
                
                if (response.data) {
                    chat = response.data;
                    chats.value.push(chat);
                }
            }
            
            if (chat) {
                activeChat.value = chat;
                await setActiveChat(chat.id);
            }
        } catch (error) {
            console.error('Error setting active user:', error);
        }
    }

    async function addMessage(content: string) {
        if (!activeChat.value) {
            console.error('No active chat');
            return;
        }

        try {
            const senderId = currentUser.value?.id ?? SUPPORT_USER.value?.id;
            if (!senderId) {
                console.error('No valid sender ID');
                return;
            }

            const message = {
                content,
                chat: activeChat.value.id,
                sender: senderId
            };

            const response = await axios.post('http://127.0.0.1:8000/api/messages/', message, {
                headers: getHeaders()
            });

            if (response.data) {
                const sender = {
                    id: senderId,
                    username: currentUser.value?.username ?? SUPPORT_USER.value?.username ?? 'Unknown',
                    first_name: currentUser.value?.first_name ?? SUPPORT_USER.value?.first_name ?? 'Unknown',
                    last_name: currentUser.value?.last_name ?? SUPPORT_USER.value?.last_name ?? ''
                };

                const newMessage: Message = {
                    id: response.data.id,
                    content: response.data.content,
                    chat_id: activeChat.value.id,
                    sender,
                    created_at: response.data.created_at,
                    read_at: response.data.read_at
                };

                // Only update messages array, not activeChat.messages
                messages.value.push(newMessage);
                
                console.log('Message sent:', newMessage);
            }
        } catch (error) {
            console.error('Error sending message:', error);
        }
    }

    async function updateUserPresence(userId: number, isOnline: boolean) {
        if (!currentUser.value) return
        
        try {
            const response = await axios.post(
                `http://127.0.0.1:8000/api/users/${userId}/presence/`, 
                { is_online: isOnline },
                { headers: getHeaders() }
            )
            
            if (response.data) {
                userPresences.value.set(userId, response.data)
            }
        } catch (error) {
            console.error('Error updating user presence:', error)
        }
    }

    return {
        chats,
        messages,
        currentChat: computed(() => activeChat.value),
        SUPPORT_USER,
        init,
        addMessage,
        setActiveChat,
        setActiveuser,
        setSearchUsers,
        searchUser,
        isAdmin,
        userPresences: computed(() => userPresences.value),
        updateUserPresence,
        handleLogout,
        users: computed(() => users.value)
    }
})
