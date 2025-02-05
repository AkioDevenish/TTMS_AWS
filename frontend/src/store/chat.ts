import { defineStore } from 'pinia'
import { ref, computed, onBeforeUnmount, watch, onMounted } from "vue"
import { useAuth } from '@/composables/useAuth'
import axios from 'axios'

interface User {
    id: number;
    username: string;
    email: string;
    first_name?: string;
    last_name?: string;
    support_chat?: boolean;
}

interface Participant extends User {
  id: number;
}

interface MessageSender {
    id: number;
    username: string;
    email: string;
    first_name?: string;
    last_name?: string;
}

interface Message {
    id: number;
    content: string;
    chat_id: number;
    sender: MessageSender;
    created_at: string;
    read_at: string | null;
    time?: string;
}

interface ProcessedMessage extends Message {
    isCurrentUser: boolean;
    alignment: string;
}

interface Chat {
  id: number;
  name: string;
  user: MessageSender;
  support_chat: boolean;
  created_at: string;
  messages: Message[];
  participants: MessageSender[];
}

interface UserPresence {
  id: number;
  is_online: boolean;
  last_seen: string;
}

interface CurrentUser {
  id: number;
  username: string;
  email: string;
  role: string;
  is_superuser: boolean;
  is_staff: boolean;
  first_name: string | null;
  last_name: string | null;
}

interface ProcessedChat {
  id: number;
  name: string;
  messages: ProcessedMessage[];
  lastMessageTime: Date;
  participants: MessageSender[];
  support_chat: boolean;
  created_at: string;
  user: MessageSender;
}

export const useChatStore = defineStore('chat', () => {
  const auth = useAuth()

  // Wait for auth to be ready
  onMounted(async () => {
    await auth.checkAuth()
  })

  const currentUser = computed(() => auth.currentUser?.value)

  // Initialize auth state
  let authInitialized = ref(false)

  async function waitForAuth() {
    if (!auth.currentUser.value) {
      await new Promise<void>((resolve) => {
        const unwatch = watch(() => auth.currentUser.value, (user) => {
          if (user) {
            authInitialized.value = true
            unwatch()
            resolve()
          }
        })
      })
    } else {
      authInitialized.value = true
    }
  }

  const SUPPORT_USER = ref<User | null>(null)
  const chats = ref<ProcessedChat[]>([])
  const activeChat = ref<ProcessedChat | null>(null)
  const messages = ref<ProcessedMessage[]>([])
  const searchUser = ref<User[]>([])
  const userPresences = ref<Map<number, UserPresence>>(new Map())
  const users = ref<User[]>([])

  // Helper function to get headers
  function getHeaders() {
    return {
      'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
      'Content-Type': 'application/json'
    }
  }

  async function updateUserPresence(userId: number, isOnline: boolean) {
    try {
      await axios.post(`/users/${userId}/presence/`, {
        is_online: isOnline
      }, {
        headers: getHeaders()
      })
    } catch (error) {
      console.error('Error updating user presence:', error)
    }
  }

    async function handleLogout() {
        if (currentUser.value?.id) {
            await updateUserPresence(currentUser.value.id, false)
        }
    }

  async function init() {
    try {
      // Get support user without requiring auth
      const supportResponse = await axios.get<User[]>('/users/', {
        params: {
          email: 'mdpssupport@metoffice.gov.tt'
        }
      })

      const supportUser = supportResponse.data.find(user =>
        user.email === 'mdpssupport@metoffice.gov.tt' &&
        user.username === 'mdps.support'
      )

      if (supportUser) {
        SUPPORT_USER.value = supportUser
      }

      return true
    } catch (error) {
      console.error('Error in init:', error)
      return false
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
        
        // Don't filter messages, show all messages for the active chat
        return {
            ...activeChat.value,
            messages: messages.value
        }
    })

  function processMessages(chatMessages: Message[]): ProcessedMessage[] {
    return chatMessages.map(msg => {
      const isCurrentUser = msg.sender.id === currentUser.value?.id;
      return {
        ...msg,
        isCurrentUser,
        alignment: isCurrentUser ? 'right' : 'left',
        time: new Date(msg.created_at).toLocaleTimeString([], {
          hour: '2-digit',
          minute: '2-digit',
          hour12: true
        })
      };
    });
  }

    function processMessage(msg: Message): ProcessedMessage {
        const isCurrentUser = msg.sender.id === currentUser.value?.id;
        return {
            ...msg,
            isCurrentUser,
            alignment: isCurrentUser ? 'right' : 'left',
            time: new Date(msg.created_at).toLocaleTimeString([], { 
                hour: '2-digit', 
                minute: '2-digit',
                hour12: true 
            })
        };
    }

    function processChat(chat: Chat): ProcessedChat {
        const processedMessages = processMessages(chat.messages || []);
        const lastMessage = processedMessages[processedMessages.length - 1];
        
        let otherParticipant;
        const isMDPSSupport = currentUser.value?.email === 'mdpssupport@metoffice.gov.tt';
        
        if (isMDPSSupport) {
            // For MDPS support, show the other user's info
            otherParticipant = chat.participants.find(p => 
                p.email !== 'mdpssupport@metoffice.gov.tt'
            ) || chat.user;
        } else {
            // For regular users, show MDPS support info
            otherParticipant = chat.participants.find(p => 
                p.email === 'mdpssupport@metoffice.gov.tt'
            );
        }

        if (!otherParticipant) {
            otherParticipant = chat.user;
        }

        return {
            id: chat.id,
            name: formatParticipantName(otherParticipant, isMDPSSupport),
            messages: processedMessages,
            lastMessageTime: lastMessage 
                ? new Date(lastMessage.created_at)
                : new Date(chat.created_at),
            participants: chat.participants,
            support_chat: chat.support_chat,
            created_at: chat.created_at,
            user: otherParticipant
        };
    }

    function formatParticipantName(participant: MessageSender, isMDPSSupport: boolean): string {
        if (!isMDPSSupport) {
            return 'MDPS Support';
        }
        
        const firstName = participant.first_name || '';
        const lastName = participant.last_name || '';
        const username = participant.username || '';
        
        return `${firstName} ${lastName}`.trim() || username;
    }

    async function handleChatUpdate(chatId: number) {
        try {
            const messagesResponse = await axios.get('http://127.0.0.1:8000/api/messages/', {
                headers: getHeaders()
            });
            
            const chatResponse = await axios.get<Chat>(
                `http://127.0.0.1:8000/api/chats/${chatId}/`, 
                { headers: getHeaders() }
            );
            
            if (chatResponse.data && messagesResponse.data) {
                // Get all messages for this chat without filtering
                const chatMessages = messagesResponse.data.filter((msg: any) => msg.chat === chatId);
                const processedMessages = chatMessages.map((msg: any) => ({
                    id: msg.id,
                    content: msg.content,
                    chat_id: msg.chat,
                    sender: msg.sender,
                    created_at: msg.created_at,
                    read_at: msg.read_at,
                    time: new Date(msg.created_at).toLocaleTimeString([], { 
                        hour: '2-digit', 
                        minute: '2-digit',
                        hour12: true 
                    }),
                    isCurrentUser: msg.sender.id === currentUser.value?.id,
                    alignment: msg.sender.id === currentUser.value?.id ? 'right' : 'left'
                }));

                const processedChat = processChat(chatResponse.data);
                
                if (activeChat.value?.id === chatId) {
                    messages.value = processedMessages;
                    activeChat.value = {
                        ...processedChat,
                        messages: processedMessages
                    };
                }

                const chatIndex = chats.value.findIndex(c => c.id === chatId);
                if (chatIndex !== -1) {
                    chats.value[chatIndex] = {
                        ...processedChat,
                        messages: processedMessages
                    };
                }
                
                chats.value.sort((a, b) => b.lastMessageTime.getTime() - a.lastMessageTime.getTime());
            }
        } catch (error) {
            console.error('Error in handleChatUpdate:', error);
        }
    }

    // Add this new function to handle scrolling
    function scrollToLatestMessage() {
        setTimeout(() => {
            const container = document.querySelector(".chat-body");
            if (container) {
                container.scrollTop = container.scrollHeight;
            }
        }, 100); // Small delay to ensure content is rendered
    }

    // Modify handleNewMessage to include scrolling
    async function handleNewMessage(newMessage: Message) {
        try {
            const processedMessage = processMessage(newMessage);
            
            messages.value = [...messages.value, processedMessage];
            
            if (activeChat.value) {
                const updatedChat: ProcessedChat = {
                    ...activeChat.value,
                    messages: [...activeChat.value.messages, processedMessage],
                    lastMessageTime: new Date(newMessage.created_at)
                };
                activeChat.value = updatedChat;
                
                // Update in chats list
                const chatIndex = chats.value.findIndex(c => c.id === updatedChat.id);
                if (chatIndex !== -1) {
                    chats.value[chatIndex] = updatedChat;
                }
            }
            
            // Scroll to latest message
            scrollToLatestMessage();
            
            if (activeChat.value?.id) {
                await handleChatUpdate(activeChat.value.id);
            }
        } catch (error) {
            console.error('Error handling new message:', error);
        }
    }

    // Also modify setActiveChat to scroll when opening a chat
    async function setActiveChat(chat: Chat) {
        try {
            const response = await axios.get(`http://127.0.0.1:8000/api/chats/${chat.id}/`, {
                headers: getHeaders()
            });

            if (response.data) {
                const chatMessages = response.data.messages || [];
                const processedMessages = chatMessages.map((msg: Message) => ({
                    ...msg,
                    isCurrentUser: msg.sender.id === currentUser.value?.id,
                    alignment: msg.sender.id === currentUser.value?.id ? 'right' : 'left'
                }));

                activeChat.value = response.data;
                messages.value = processedMessages;
                
                // Scroll to latest message after setting chat
                scrollToLatestMessage();
            }
        } catch (error) {
            console.error('Error setting active chat:', error);
        }
    }

  async function fetchChatMessages(chatId: number) {
    try {
      const token = localStorage.getItem('access_token')
      if (!token) {
        console.error('No auth token found')
        return
      }

      // Use the messages endpoint instead of chat messages
      const response = await axios.get('/messages/', {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      })

      if (response.data) {
        // Filter messages for current chat
        const chatMessages = response.data.filter((msg: any) => msg.chat === chatId)
        const processedMessages = chatMessages.map((msg: any) => ({
          id: msg.id,
          content: msg.content,
          chat_id: msg.chat,
          sender: msg.sender,
          created_at: msg.created_at,
          time: msg.time || new Date(msg.created_at).toLocaleTimeString([], {
            hour: '2-digit',
            minute: '2-digit',
            hour12: true
          }),
          isCurrentUser: msg.sender.id === currentUser.value?.id,
          alignment: msg.sender.id === currentUser.value?.id ? 'right' : 'left'
        }))

        if (activeChat.value && activeChat.value.id === chatId) {
          messages.value = processedMessages
        }
      }
    } catch (error) {
      console.error('Error fetching messages:', error)
    }
  }

    // Add this function to handle message updates
    async function updateMessages(chatId: number) {
        // Wait 2 seconds before fetching updates
        setTimeout(async () => {
            try {
                const response = await axios.get(`http://127.0.0.1:8000/api/messages/`, {
                    headers: getHeaders()
                });

                if (response.data) {
                    // Filter and process messages for current chat
                    const chatMessages = response.data.filter((msg: any) => msg.chat === chatId);
                    const processedMessages = chatMessages.map((msg: any) => ({
                        id: msg.id,
                        content: msg.content,
                        chat_id: msg.chat,
                        sender: msg.sender,
                        created_at: msg.created_at,
                        time: new Date(msg.created_at).toLocaleTimeString([], { 
                            hour: '2-digit', 
                            minute: '2-digit',
                            hour12: true 
                        }),
                        isCurrentUser: msg.sender.id === currentUser.value?.id,
                        alignment: msg.sender.id === currentUser.value?.id ? 'right' : 'left'
                    }));

                    if (activeChat.value?.id === chatId) {
                        messages.value = processedMessages;
                    }
                }
            } catch (error) {
                console.error('Error updating messages:', error);
            }
        }, 2000);
    }

    // Modify the addMessage function to include the update
    async function addMessage(content: string) {
        try {
            if (!activeChat.value?.id) {
                console.error('No active chat ID');
                return;
            }

            const messageData = {
                content,
                chat: activeChat.value.id
            };

            const response = await axios.post('http://127.0.0.1:8000/api/messages/', messageData, {
                headers: getHeaders()
            });

            if (response.data) {
                // After sending message, update messages after 2 seconds
                updateMessages(activeChat.value.id);
            }
        } catch (error) {
            console.error('Error adding message:', error);
        }
    }

  function isCurrentUserMessage(message: Message) {
    return message.sender.id === currentUser.value?.id
  }

  async function setActiveuser(user: User) {
    try {
      console.log('Setting active user:', user)

      if (!auth.isAuthenticated.value) {
        console.error('User not authenticated')
        return
      }

      // Check if chat already exists
      const existingChat = chats.value.find(chat =>
        chat.participants.some(p => p.id === user.id)
      );

      if (existingChat) {
        console.log('Found existing chat:', existingChat);
        return existingChat;
      }

      // Create new chat
      const chatData = {
        name: `Chat with ${user.username}`,
        support_chat: SUPPORT_USER.value?.id === user.id,
        user_id: user.id
      }

      const chatResponse = await axios.post('/chats/', chatData, {
        headers: getHeaders()
      })

      if (chatResponse.data) {
        // Add to chats list
        chats.value.push(chatResponse.data);

        // Set as active chat
        activeChat.value = chatResponse.data;
        messages.value = processMessages(chatResponse.data.messages || []);

        return chatResponse.data;
      }
    } catch (error) {
      console.error('Error setting active user:', error)
    }
  }

  async function fetchSupportUser() {
    try {
      const response = await axios.get<User[]>('/users/', {
        params: {
          email: 'mdpssupport@metoffice.gov.tt'
        },
        headers: getHeaders()
      });

      const supportUser = response.data.find(user =>
        user.email === 'mdpssupport@metoffice.gov.tt' &&
        user.username === 'mdps.support'
      );

      if (supportUser) {
        SUPPORT_USER.value = supportUser;
      }
    } catch (error) {
      console.error('Error fetching support user:', error);
    }
  }

  async function fetchAllUsers() {
    try {
      const response = await axios.get<User[]>('/users/', {
        headers: getHeaders()
      });

      if (currentUser.value?.email === 'mdpssupport@metoffice.gov.tt') {
        // Get all users who have sent messages
        const usersWithMessages = new Set();

        chats.value.forEach(chat => {
          // Get unique users who have sent messages
          chat.messages.forEach(message => {
            if (message.sender.email !== 'mdpssupport@metoffice.gov.tt') {
              usersWithMessages.add(message.sender.id);
            }
          });
        });

        // Filter users who have sent messages
        users.value = response.data.filter(user => {
          const hasMessages = usersWithMessages.has(user.id);
          const isNotSupport = user.email !== 'mdpssupport@metoffice.gov.tt';

          return isNotSupport && hasMessages;
        });

        console.log('Users with messages:', users.value);
      } else {
        // Regular user logic
        users.value = response.data.filter(user =>
          user.email !== 'mdpssupport@metoffice.gov.tt'
        );
      }
    } catch (error) {
      console.error('Error fetching users:', error);
    }
  }

  async function fetchAllChats() {
    try {
      const response = await axios.get<Chat[]>('/chats/', {
        headers: getHeaders()
      });

            const isSupportUser = currentUser.value?.email === 'mdpssupport@metoffice.gov.tt';
            
            let filteredChats = response.data;
            if (!isSupportUser) {
                // Regular users only see their support chat
                filteredChats = response.data.filter(chat => 
                    chat.support_chat && 
                    chat.participants.some(p => p.id === currentUser.value?.id)
                );
            }

            // Process all messages for each chat
            const processedChats = filteredChats
                .map(chat => ({
                    ...chat,
                    messages: chat.messages || [] // Ensure messages array exists
                }))
                .map(processChat)
                .filter((chat): chat is ProcessedChat => chat !== null)
                .sort((a, b) => b.lastMessageTime.getTime() - a.lastMessageTime.getTime());

      chats.value = processedChats;
    } catch (error) {
      console.error('Error in fetchAllChats:', error);
    }
  }

  // Update fetchChats to process messages
  async function fetchChats() {
    try {
      const response = await axios.get<Chat[]>('/chats/', {
        headers: getHeaders()
      });

      const processedChats = response.data
        .map(processChat)
        .filter(chat => chat !== null)
        .sort((a, b) => b.lastMessageTime.getTime() - a.lastMessageTime.getTime());

      chats.value = processedChats;
    } catch (error) {
      console.error('Error fetching chats:', error);
    }
  }

  async function handleNewChat(chat: Chat) {
    const processedChat: ProcessedChat = {
      ...chat,
      messages: processMessages(chat.messages || []),
      lastMessageTime: chat.messages?.length
        ? new Date(chat.messages[chat.messages.length - 1].created_at)
        : new Date(chat.created_at)
    };

    // Add to chats if not exists
    const existingIndex = chats.value.findIndex(c => c.id === chat.id);
    if (existingIndex === -1) {
      chats.value.push(processedChat);
    } else {
      chats.value[existingIndex] = processedChat;
    }

    // Sort chats by latest message
    chats.value.sort((a, b) => b.lastMessageTime.getTime() - a.lastMessageTime.getTime());
  }

    return {
        currentUser,
        SUPPORT_USER,
        chats,
        activeChat,
        messages,
        searchUser,
        userPresences,
        users,
        currentChat,
        init,
        setActiveuser,
        addMessage,
        setActiveChat,
        handleLogout,
        updateUserPresence,
        setSearchUsers,
        fetchSupportUser,
        fetchAllChats,
        isCurrentUserMessage,
        fetchChats,
        fetchAllUsers,
        handleNewMessage,
        handleChatUpdate,
        handleNewChat,
        updateMessages,
        scrollToLatestMessage
    }
})