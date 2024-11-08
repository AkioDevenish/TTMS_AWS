<template>
    <div class="header-logo-wrapper col-auto p-0">
        <div class="logo-wrapper"><router-link to="/"><img class="img-fluid" src="@/assets/images/logo/logo.png"
                    alt=""></router-link></div>
        <div class="toggle-sidebar" @click="store.toggle_sidebar">
            <svg class="stroke-icon sidebar-toggle status_toggle middle">
                <use href="@/assets/svg/icon-sprite.svg#toggle-icon"></use>
            </svg>
        </div>
    </div>
</template>
<script lang="ts" setup>
import { useMenuStore } from "@/store/menu";
const store = useMenuStore();
</script>