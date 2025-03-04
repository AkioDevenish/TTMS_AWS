<template>
    <form class="msger-inputarea clearfix" @submit.prevent="addChat()">
        <input class="msger-input form-control rounded-pill" placeholder="Type Message here.." v-model="text"
            v-on:keyup.enter="addChat()">
        <button type="submit" class="btn btn-primary rounded-circle msger-send-btn">
            <i class="fa fa-paper-plane"></i>
        </button>
    </form>
</template>
<script lang="ts" setup>
import { ref } from "vue"
import { useChatStore } from "@/store/chat"
import { storeToRefs } from "pinia";

const store = useChatStore()
const { currentChat } = storeToRefs(useChatStore())
let text = ref<string>("")

function addChat() {
    var container: any = document.querySelector(".msger-chat")
    setTimeout(function () {
        container.scrollBy({ top: 200, behavior: 'smooth' });
    }, 310);
    setTimeout(function () {
        container.scrollBy({ top: 200, behavior: 'smooth' });
    }, 1100);
    if (text.value !== '') {
        store.addMessage(text.value);
        text.value = '';
    }
}
</script>