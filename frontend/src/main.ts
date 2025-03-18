import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import "bootstrap/dist/css/bootstrap.min.css"
import "bootstrap"
import 'bootstrap/dist/js/bootstrap.bundle'
import "bootstrap/dist/js/bootstrap.min.js";
import "./assets/scss/app.scss"
import '@vuepic/vue-datepicker/dist/main.css'
import 'vue-rate/dist/vue-rate.css'
import "vue-multiselect/dist/vue-multiselect.css"
import 'vue3-simple-typeahead/dist/vue3-simple-typeahead.css';
import 'vue3-perfect-scrollbar/dist/vue3-perfect-scrollbar.css'
import '@globalhive/vuejs-tour/dist/style.css';
import 'vue3-timeline/dist/style.css'

import VueFeather from "vue-feather";
import VueApexCharts from "vue3-apexcharts";
import Datepicker from '@vuepic/vue-datepicker';
import OpenLayersMap from 'vue3-openlayers'
import { quillEditor } from "vue3-quill";
import Lightbox from 'vue-easy-lightbox'
import rate from 'vue-rate'
import VueNumber from "vue-number-animation";
import VueJsTour from '@globalhive/vuejs-tour';
import Multiselect from 'vue-multiselect'
import AosVue from "aos-vue";
import SimpleTypeahead from 'vue3-simple-typeahead';
import { VueMasonryPlugin } from 'vue-masonry';
import vueChartist from "vue-chartist"
import { plugin } from 'vue3-timeline'
import PerfectScrollbar from 'vue3-perfect-scrollbar'
import VueTour from 'v3-tour'

import English from "@/core/locales/en.json"
import Russian from "@/core/locales/ru.json"
import Arabic from "@/core/locales/ar.json"
import German from "@/core/locales/ge.json"
import لعربية from "@/core/locales/ae.json"
import 简体中文 from "@/core/locales/cn.json"
import Português from "@/core/locales/pt.json"
import Français from "@/core/locales/fr.json"
import Deutsch from "@/core/locales/de.json"
import Español from "@/core/locales/es.json"

import { createI18n } from 'vue-i18n'
import './plugins/axios';
import { library } from '@fortawesome/fontawesome-svg-core';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import { fas } from '@fortawesome/free-solid-svg-icons';
import { vRole } from './directives/roleDirective'

// Add all icons to the library
library.add(fas);

const i18n = createI18n({
  legacy: false,
  locale: 'English',
  messages: {
    English: English,
    German: German,
    Russian: Russian,
    Arabic: Arabic,
    Español: Español,
    Deutsch: Deutsch,
    Français: Français,
    Português: Português,
    简体中文: 简体中文,
    لعربية: لعربية,
  }
})

const app = createApp(App)
  .use(router)
  .use(createPinia())
  .use(VueApexCharts)
  .use(OpenLayersMap)
  .use(quillEditor)
  .use(rate)
  .use(AosVue)
  .use(vueChartist)
  .use(VueMasonryPlugin)
  .use(Lightbox)
  .use(VueNumber)
  .use(i18n)
  .use(VueTour)
  .use(VueJsTour)
  .use(plugin)
  .use(PerfectScrollbar)
  .use(SimpleTypeahead)
  .component(VueFeather.name, VueFeather)
  .component('Datepicker', Datepicker)
  .component('multiselect', Multiselect)
  .component('font-awesome-icon', FontAwesomeIcon)
  .directive('role', vRole)

app.mount('#app')
