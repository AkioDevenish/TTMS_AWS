<template>
    <div class="col-xxl-9 col-xl-8 col-md-7 box-col-7">
        <div class="card right-sidebar-chat">
            <div v-if="currentChat" class="right-sidebar-title">
                <div class="common-space">
                    <div class="chat-time group-chat">
                        <ul>
                            <li v-for="(item, index) in group" :key="index">
                                <img class="img-fluid rounded-circle"
                                    :src="getImages(item.img)" 
                                    alt="user">
                            </li>
                            <li>
                                <div class="custom-name profile-count light-background">
                                    <p class="f-w-500">9+</p>
                                </div>
                            </li>
                        </ul>
                        <div> 
                            <span>Meeting Department</span>
                            <p>35 Members</p>
                        </div>
                    </div>
                    <div class="d-flex gap-2">
                        <div class="contact-edit chat-alert"><i class="icon-info-alt"></i></div>
                        <div class="contact-edit chat-alert">
                            <svg class="dropdown-toggle" role="menu" data-bs-toggle="dropdown" aria-expanded="false">
                                <use href="@/assets/svg/icon-sprite.svg#menubar"></use>
                            </svg>
                            <div class="dropdown-menu dropdown-menu-end">
                                <a class="dropdown-item" href="#!">View details</a>
                                <a class="dropdown-item" href="#!">Send messages</a>
                                <a class="dropdown-item" href="#!">Add to favorites</a>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div v-else class="right-sidebar-title">
                <div class="common-space">
                    <p>Select a group to start messaging</p>
                </div>
            </div>
            <div class="right-sidebar-Chats" v-if="currentChat">
                <div class="msger">
                    <div class="msger-chat">
                        <div class="msg" v-for="(chat, index) in currentChat?.messages" :key="index" 
                            v-bind:class="[{ clearfix: chat.sender == 0 }, {
                                'right-msg': chat.sender != 0, 
                                'left-msg': chat.sender == 0,
                            }]">
                            <div class="msg-img"><img class="rounded-circle float-start chat-user-img img-30"
                                    v-if="currentChat.thumb && chat.sender != 0" v-bind:src="getImages(currentChat.thumb)"
                                    alt=""></div>
                            <div class="msg-bubble">
                                <div class="msg-info" v-bind:class="{ 'text-start': chat.sender == 0 }">
                                    <div class="msg-info-name" v-if="chat.sender == 0">{{ currentChat.name }}</div>
                                    <div class="msg-info-name" v-if="chat.sender != 0">Theresa Webb</div>
                                    <div class="msg-info-time">{{ chat.time }}</div>
                                </div>
                                <div class="msg-text">{{ chat.text }}
                                </div>
                            </div>
                        </div>
                    </div>
                    <AddChat />
                </div>
            </div>
        </div>
    </div>
</template>
<script lang="ts" setup>
import { onMounted } from 'vue'
import { group } from "@/core/data/chat"
import { storeToRefs } from "pinia"
import { getImages } from "@/composables/common/getImages"
import { ref, defineAsyncComponent } from 'vue'
import { useChatStore } from "@/store/chat"

const chatStore = useChatStore()
const { currentChat } = storeToRefs(chatStore)

onMounted(async () => {
    await chatStore.init()
})

const AddChat = defineAsyncComponent(() => import("@/components/theme/chat/private/AddChat.vue"))
</script>