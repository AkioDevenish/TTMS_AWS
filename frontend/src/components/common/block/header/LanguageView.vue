<template>
    <div class="translate_wrapper" :class="active ? 'active' : ''">
        <div class="current_lang">
            <div class="lang" @click="openDropDown()"><i class="flag-icon " :class="selectedLanguage.icon"></i><span
                    class="lang-txt">{{
                        selectedLanguage.txt }}
                </span>
            </div>
        </div>
    </div>
    <div class="more_lang" :class="active ? 'active' : ''">
        <div class="lang" v-for="(lang, index) in data" :key="index" @click.prevent="selectLanguage(lang)"><i
                class="flag-icon " :class="lang.icon"></i><span class="lang-txt">{{ lang.lan }}<span>
                    {{ lang.span }}</span></span></div>
    </div>
</template>
<script lang="ts" setup>
import { ref } from 'vue';
import { language } from "@/core/data/language"
import { useI18n } from "vue-i18n";
const i18n = useI18n()
const active = ref<boolean>(false)
const selectedLanguage = ref({
    lan: 'English',
    txt: 'EN',
    icon: 'flag-icon-us'
})
const data = language

function selectLanguage(language: string) {
    active.value = false;
    i18n.locale.value = language.lan;
    selectedLanguage.value = language;
}

function openDropDown() {
    active.value = !active.value;
}

function hideDropdown() {
    active.value = false;
}
</script>