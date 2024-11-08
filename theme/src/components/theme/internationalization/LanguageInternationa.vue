<template>
    <div class="col-lg-12">
        <div class="site">
            <div class="site-bd">
                <div class="wrapper">
                    <div class="card">
                        <div class="card-header language-header">
                            <h4>Internationalization</h4>
                            <div class="main" role="main">
                                <select class="langChoice js-languageSelect" v-model="$i18n.locale">
                                    <option v-for="(lang, i) in langs" :key="`lang-${i}`" :selected="i == 0"
                                        :value="lang.lan"> {{ lang.lan }}
                                    </option>
                                </select>
                            </div>
                        </div>
                        <div class="card-body row">
                            <div class="col-md-6">
                                <h5 class="f-w-600 hdg hdg_main js-languagePageHdg pb-2">{{ $t('Static Sub Nav') }}</h5>
                                <div class="masthead" role="banner">
                                    <ul class="icon-lists border navs-icon hList hList_loose masthead-nav js-languageList">
                                        <li><a href="javascript:void(0)"><span> {{ $t('Base') }}</span></a></li>
                                        <li><a href="javascript:void(0)"><span> {{ $t('Advance') }}</span></a>
                                            <ul class="hList hList_loose masthead-nav js-languageList">
                                                <li class="pl-navs-inline"><a href="javascript:void(0)"><span>{{
                                                    $t('Scrollable')
                                                }}</span></a>
                                                </li>
                                                <li class="pl-navs-inline"><a href="javascript:void(0)"><span>{{
                                                    $t('Tree View')
                                                }}</span></a>
                                                </li>
                                                <li class="pl-navs-inline"><a href="javascript:void(0)"><span>{{
                                                    $t('Rating')
                                                }}</span></a>
                                                </li>
                                            </ul>
                                        </li>
                                        <li><a href="javascript:void(0)"><span data-mlr-text="">
                                                    {{ $t('Forms') }}</span></a></li>
                                        <li><a href="javascript:void(0)"><span data-mlr-text="">
                                                    {{ $t('Tables') }}</span></a></li>
                                    </ul>
                                </div>
                            </div>
                            <div class="col-md-6 language-xs">
                                <h5 class="f-w-600 hdg hdg_main js-languagePageHdg pb-2">{{ $t('Static Sub Nav') }}</h5>
                                <div class="masthead" role="banner">
                                    <ul class="icon-lists border navs-icon hList hList_loose masthead-nav js-languageList">
                                        <li><a href="javascript:void(0)"><span> {{ $t('Base') }}</span></a></li>
                                        <li><a href="javascript:void(0)"><span> {{ $t('Advance') }}</span></a>
                                            <ul class="hList hList_loose masthead-nav js-languageList">
                                                <li class="pl-navs-inline"><a href="javascript:void(0)"><span>{{
                                                    $t('Scrollable')
                                                }}</span></a><span
                                                        class="pull-right badge badge-primary">New</span></li>
                                                <li class="pl-navs-inline"><a href="javascript:void(0)"><span>{{
                                                    $t('Tree View')
                                                }}</span></a><span
                                                        class="pull-right badge badge-primary">Find</span></li>
                                                <li class="pl-navs-inline"><a href="javascript:void(0)"><span>{{
                                                    $t('Rating')
                                                }}</span></a>
                                                </li>
                                            </ul>
                                        </li>
                                        <li><a href="javascript:void(0)"><span data-mlr-text="">
                                                    {{ $t('Forms') }}</span></a></li>
                                        <li><a href="javascript:void(0)"><span data-mlr-text="">
                                                    {{ $t('Tables') }}</span></a></li>
                                    </ul>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
<script lang="ts" setup>
import { ref } from 'vue';
import { useI18n } from "vue-i18n";
const i18n = useI18n()
const lang = ref<string>("English")
let langs = [
    { id: 0, lan: "English" }, { id: 1, lan: "German" }, { id: 2, lan: "Russian" }, { id: 3, lan: "Arabic" }
]
</script>