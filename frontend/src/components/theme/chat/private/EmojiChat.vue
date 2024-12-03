<template>
    <div class="open-emoji" @click="toggleEmojiPicker">
        <div class="second-btn uk-button"></div>
    </div>
    <div class="emoji_picker shadow" v-if="show">
        <div class="picker_container">
            <div class="category p-0" v-for="category in categories" :key="`category_${category}`">
                <span>{{ category }}</span>
                <div class="emojis_container">
                    <button @click.prevent="handleEmojiClick(emoji)" v-for="(emoji, index) in getEmojiValue(category)"
                        :key="`emoji_${index}`">
                        {{ emoji }}
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>
 
<script setup lang="ts">
import { computed, ref, defineEmits } from "vue"
import { emoji } from '@/core/data/emoji'

let emit = defineEmits(['selectEmoji'])
let categories = computed(() => {
    return Object.keys(emoji);
})
function getEmojiValue(value: string) {
    return Object.values(emoji[value])
}
function handleEmojiClick(emoji: string) {
    emit('selectEmoji', emoji)
}
let show = ref<boolean>(false);

function toggleEmojiPicker() {
    show.value = !show.value;
}
</script>