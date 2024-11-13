<template>
	<div class="logo-wrapper">
		<router-link to="/">
			<!-- <img class="img-fluid" src="@/assets/images/logo/logo_light.png" alt=""> -->
			<h1 class="logo-text">MDPS</h1>
		</router-link>
		<div class="back-btn" @click="store.toggle_sidebar"><i class="fa fa-angle-left"></i></div>
		<div class="toggle-sidebar" @click="store.toggle_sidebar">
			<svg class="stroke-icon sidebar-toggle status_toggle middle">
				<use href="@/assets/svg/icon-sprite.svg#toggle-icon"></use>
			</svg>
			<svg class="fill-icon sidebar-toggle status_toggle middle">
				<use href="@/assets/svg/icon-sprite.svg#fill-toggle-icon"></use>
			</svg>
		</div>
	</div>
	<div class="logo-icon-wrapper"><router-link to="/"><img class="img-fluid" src="@/assets/images/logo/logo-icon.png" alt=""></router-link></div>
</template>
<script lang="ts" setup>
import { useMenuStore } from "@/store/menu";
const store = useMenuStore();
</script>
<style scoped>
.logo-text {
	color: #fff;
}
</style>