import { defineStore } from 'pinia'
import { ref, computed, onBeforeUnmount, watch, onMounted, Ref } from "vue"
import { useAuth } from '@/composables/useAuth'
import axios from 'axios'

interface User {
  id: number;
  username: string;
  email: string;
  first_name: string | null;
  last_name: string | null;
  is_staff: boolean;
  is_superuser: boolean;
  role: string;
}

interface Participant extends User {
  id: number;
}

interface MessageSender {
  id: number;
  username: string;
  email: string;
  first_name: string | null;
  last_name: string | null;
}

interface Message {
  id: number;
  chat: number;
  chat_id: number;
  content: string;
  created_at: string;
  read_at: string | null;
  sender: {
    id: number;
    email: string;
    first_name?: string;
    last_name?: string;
    username?: string;
  };
}

export interface ProcessedMessage extends Message {
  isCurrentUser: boolean;
  alignment: 'left' | 'right';
  senderName?: string;
  time: string;
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
    stopPolling()
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
          const chatUser = chats.value.find(c => c.user.id === message.sender.id)?.user
          if (chatUser && chatUser.email) {
            userMap.set(message.sender.id, {
              id: chatUser.id,
              username: chatUser.username,
              email: chatUser.email,
              first_name: chatUser.first_name || null,
              last_name: chatUser.last_name || null,
              is_staff: false,
              is_superuser: false,
              role: ''
            })
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
    const isMDPS = currentUser.value?.email === 'mdpssupport@metoffice.gov.tt';
    return {
      ...msg,
      isCurrentUser: msg.sender.email === currentUser.value?.email,
      alignment: msg.sender.email === currentUser.value?.email ? 'right' : 'left',
      senderName: isMDPS ?
        (msg.sender.email === 'mdpssupport@metoffice.gov.tt' ? 'You' : msg.sender.username) :
        (msg.sender.email === 'mdpssupport@metoffice.gov.tt' ? 'MDPS Support' : 'You'),
      time: new Date(msg.created_at).toLocaleTimeString([], {
        hour: '2-digit',
        minute: '2-digit',
        hour12: true
      })
    };
  }

  function getSenderDisplayName(sender: MessageSender): string {
    if (sender.email === 'mdpssupport@metoffice.gov.tt') {
      return 'MDPS Support';
    }
    return `${sender.first_name || ''} ${sender.last_name || ''}`.trim() || sender.username || 'Unknown';
  }

  function processChat(chat: Chat): ProcessedChat {
    const processedMessages = processMessages(chat.messages || []);
    const lastMessage = processedMessages[processedMessages.length - 1];

    let otherParticipant: MessageSender;
    const isMDPSSupport = currentUser.value?.email === 'mdpssupport@metoffice.gov.tt';

    const participant = isMDPSSupport
      ? chat.participants.find(p => p.email !== 'mdpssupport@metoffice.gov.tt')
      : chat.participants.find(p => p.email === 'mdpssupport@metoffice.gov.tt');

    otherParticipant = participant || {
      id: -1,
      username: 'Unknown',
      email: '',
      first_name: '',
      last_name: ''
    };

    const chatName = isMDPSSupport
      ? `${otherParticipant.first_name || ''} ${otherParticipant.last_name || ''}`.trim() || otherParticipant.username
      : 'MDPS Support';

    return {
      id: chat.id,
      name: chatName,
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

  let pollInterval: number | null = null;
  const POLL_INTERVAL = 5000; // 5 seconds

  async function startPolling() {
    if (pollInterval) return;

    // Initial fetch
    await Promise.all([
      fetchAllChats(),
      fetchAllUsers()
    ]);

    // Start polling
    pollInterval = window.setInterval(async () => {
      if (activeChat.value?.id) {
        await handleChatUpdate(activeChat.value.id);
      }
      await fetchAllChats();
    }, POLL_INTERVAL);
  }

  function stopPolling() {
    if (pollInterval) {
      window.clearInterval(pollInterval);
      pollInterval = null;
    }
  }

  // Add cleanup on component unmount
  onBeforeUnmount(() => {
    stopPolling();
  });

  // Modify handleChatUpdate to handle polling updates
  async function handleChatUpdate(chatId: number) {
    try {
      const messagesResponse = await axios.get<Message[]>(`/messages/`, {
        headers: getHeaders()
      });

      if (!messagesResponse.data) return;

      // Get all messages for this chat, including both chat and chat_id matches
      const chatMessages = messagesResponse.data.filter((msg: Message) => {
        const isChatMatch = msg.chat === chatId || msg.chat_id === chatId;
        if (isChatMatch) {
          console.log('Matched message:', msg);
        }
        return isChatMatch;
      });

      if (!chatMessages.length) return;

      const processedMessages = chatMessages
        .map((msg: Message) => ({
          ...msg,
          ...processMessage(msg)
        }))
        .sort((a: ProcessedMessage, b: ProcessedMessage) =>
          new Date(a.created_at).getTime() - new Date(b.created_at).getTime()
        );

      // Force update the messages array
      messages.value = [...processedMessages];

      if (activeChat.value?.id === chatId) {
        activeChat.value = {
          ...activeChat.value,
          messages: [...processedMessages],
          lastMessageTime: processedMessages.length ?
            new Date(processedMessages[processedMessages.length - 1].created_at) :
            activeChat.value.lastMessageTime
        };
      }
    } catch (error) {
      console.error('Error updating chat:', error);
    }
  }

  async function setActiveChat(chat: Chat) {
    try {
      const processedChat = processChat(chat);
      activeChat.value = processedChat;

      const messagesResponse = await axios.get<Message[]>(`/messages/`, {
        headers: getHeaders()
      });

      if (messagesResponse.data) {
        const chatMessages = messagesResponse.data.filter((msg: Message) =>
          msg.chat === chat.id || msg.chat_id === chat.id
        );

        const processedMessages = chatMessages
          .map((msg: Message) => processMessage(msg))
          .sort((a: ProcessedMessage, b: ProcessedMessage) =>
            new Date(a.created_at).getTime() - new Date(b.created_at).getTime()
          );

        messages.value = processedMessages;
        activeChat.value = {
          ...processedChat,
          messages: processedMessages,
          lastMessageTime: processedMessages.length ?
            new Date(processedMessages[processedMessages.length - 1].created_at) :
            new Date(chat.created_at)
        };
      }
    } catch (error) {
      console.error('Error setting active chat:', error);
    }
  }

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

      if (activeChat.value?.id) {
        await handleChatUpdate(activeChat.value.id);
      }
    } catch (error) {
      console.error('Error handling new message:', error);
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

  async function addMessage(content: string) {
    if (!activeChat.value?.id || !currentUser.value?.email) return;

    const tempMessage: ProcessedMessage = {
      id: Date.now(),
      content: content,
      chat_id: activeChat.value.id,
      chat: activeChat.value.id,
      sender: {
        id: currentUser.value.id || 0,
        username: currentUser.value.username || '',
        first_name: currentUser.value.first_name || undefined,
        last_name: currentUser.value.last_name || undefined,
        email: currentUser.value.email
      },
      created_at: new Date().toISOString(),
      read_at: null,
      isCurrentUser: true,
      alignment: 'right',
      time: new Date().toLocaleTimeString([], {
        hour: '2-digit',
        minute: '2-digit',
        hour12: true
      })
    };

    try {
      messages.value = [...messages.value, tempMessage];

      if (activeChat.value) {
        activeChat.value.messages = [...activeChat.value.messages, tempMessage];
        activeChat.value.lastMessageTime = new Date();
      }

      const response = await axios.post('/messages/', {
        content: content,
        chat: activeChat.value.id
      }, {
        headers: getHeaders()
      });

      if (response.data) {
        const realMessage = processMessage(response.data);
        messages.value = messages.value.map(msg =>
          msg.id === tempMessage.id ? realMessage : msg
        );

        if (activeChat.value) {
          activeChat.value.messages = activeChat.value.messages.map(msg =>
            msg.id === tempMessage.id ? realMessage : msg
          );
        }

        await handleChatUpdate(activeChat.value.id);
      }
    } catch (error) {
      console.error('Error sending message:', error);
      messages.value = messages.value.filter(msg => msg.id !== tempMessage.id);
      if (activeChat.value) {
        activeChat.value.messages = activeChat.value.messages.filter(msg =>
          msg.id !== tempMessage.id
        );
      }
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

      const processedChats = response.data
        .filter(chat => chat.participants.some(p => p.id === currentUser.value?.id))
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
    startPolling,
    stopPolling
  }
})