<template>
    <div class="notification-box">
        <svg>
            <use href="@/assets/svg/icon-sprite.svg#notification"></use>
        </svg><span class="badge rounded-pill badge-primary">4 </span>
    </div>
    <div class="onhover-show-div notification-dropdown">
        <h5 class="f-18 f-w-600 mb-0 dropdown-title">Notifications </h5>
        <ul class="notification-box">
            <li class="d-flex" v-for="(item, index) in notification" :key="index">
                <div class="flex-shrink-0 " :class="item.class"><img :src="getImages(item.img)" alt="Wallet"></div>
                <div class="flex-grow-1"> <router-link to="/app/private_chat">
                        <h6>{{ item.title }}</h6>
                    </router-link>
                    <p>{{ item.desc }}</p>
                </div>
            </li>

            <li><router-link class="f-w-700" to="/app/private_chat">Check all </router-link></li>
        </ul>
    </div>
</template>
<script lang="ts" setup>
import { ref, onMounted } from 'vue';
import { notification } from "@/core/data/header"
import { getImages } from "@/composables/common/getImages"

</script>