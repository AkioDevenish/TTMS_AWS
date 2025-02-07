<template>
	<li class="back-btn"><router-link to="/"><img class="img-fluid" src="@/assets/images/logo/logo-icon.png" alt=""></router-link>
		<div class="mobile-back text-end"><span>Back</span><i class="fa fa-angle-right ps-2" aria-hidden="true"></i></div>
	</li>
	<li class="pin-title sidebar-main-title" :class="showPinTitle ? 'show' : ''">
		<div>
			<h6>Pinned</h6>
		</div>
	</li>
	<li v-for="(menuItem, index) in filteredMenu" :key="index" class="sidebar-list" :class="[{ ' sidebar-main-title': menuItem.type == 'headtitle' }, menuItem.isPinned ? 'pined' : '']">
		<div v-if="menuItem.type == 'headtitle'">
			<h6 class="lan-1">{{ $t(menuItem.headTitle1) }}</h6>
		</div>
		<i v-if="menuItem.type != 'headtitle'" class="fa fa-thumb-tack" @click="togglePinnedName({ item: menuItem })"></i>
		<a href="javascript:void(0)" class="sidebar-link sidebar-title" v-if="menuItem.type == 'sub'" :class="menuItem.title == store.perentName ? 'active' : ''" @click="store.subMenuToggle(menuItem.title)">
			<svg class="stroke-icon">
				<use :xlink:href="require('@/assets/svg/icon-sprite.svg') + `#${menuItem.icon}`"></use>
			</svg>
			<svg class="fill-icon">
				<use :xlink:href="require('@/assets/svg/icon-sprite.svg') + `#${menuItem.icon1}`"></use>
			</svg>
			<span class="lan-6">
				{{ $t(menuItem.title) }}
			</span>
			<div class="according-menu" v-if="menuItem.children">
				<i class="pull-right" :class="[menuItem.title == store.perentName ? 'fa fa-angle-down' : 'fa fa-angle-right']"></i>
			</div>
		</a>
		<router-link :to="menuItem.path" class="sidebar-link sidebar-title" v-if="menuItem.type == 'link'" :class="menuItem.title == store.perentName ? 'active' : ''" @click="store.subMenuToggle(menuItem.title)">
			<svg class="stroke-icon">
				<use :xlink:href="require('@/assets/svg/icon-sprite.svg') + `#${menuItem.icon}`"></use>
			</svg>
			<svg class="fill-icon">
				<use :xlink:href="require('@/assets/svg/icon-sprite.svg') + `#${menuItem.icon1}`"></use>
			</svg>
			<span>
				{{ $t(menuItem.title) }}
			</span>
			<i class="fa fa-angle-right pull-right" v-if="menuItem.children"></i>
		</router-link>
		<a :href="menuItem.path" class="sidebar-link sidebar-title" v-if="menuItem.type == 'extLink'">
			<svg class="stroke-icon">
				<use :xlink:href="require('@/assets/svg/icon-sprite.svg') + `#${menuItem.icon}`"></use>
			</svg>
			<svg class="fill-icon">
				<use :xlink:href="require('@/assets/svg/icon-sprite.svg') + `#${menuItem.icon1}`"></use>
			</svg>
			<span>
				{{ $t(menuItem.title) }}
			</span>
			<i class="fa fa-angle-right pull-right" v-if="menuItem.children"></i>
		</a>
		<a :href="menuItem.path" target="_blank" class="sidebar-link sidebar-title" v-if="menuItem.type == 'extTabLink'">
			<svg class="stroke-icon">
				<use :xlink:href="require('@/assets/svg/icon-sprite.svg') + `#${menuItem.icon}`"></use>
			</svg>
			<svg class="fill-icon">
				<use :xlink:href="require('@/assets/svg/icon-sprite.svg') + `#${menuItem.icon1}`"></use>
			</svg>
			<span>
				{{ $t(menuItem.title) }}
			</span>
			<i class="fa fa-angle-right pull-right" v-if="menuItem.children"></i>
		</a>
		<ul class="sidebar-submenu" v-if="menuItem.children" :style="menuItem.title == store.perentName ? 'display:block' : 'display:none'">
			<li v-for="(childrenItem, index) in menuItem.children" :key="index">
				<a class="lan-4" :class="{ 'active': childrenItem.active }" href="javascript:void(0)" v-if="childrenItem.type == 'sub'" @click="store.subChildMenu(childrenItem.title)">
					{{ $t(childrenItem.title) }}
					<label :class="'badge badge-' + childrenItem.badgeType + ' pull-right'" v-if="childrenItem.badgeType">{{
						childrenItem.badgeValue }}</label>
					<i class="fa pull-right" v-bind:class="[childrenItem.title == store.subName ? 'fa fa-angle-down' : 'fa fa-angle-right']" v-if="childrenItem.children"></i>
				</a>
				<router-link class="lan-4" :class="{ 'active': childrenItem.active }" :to="childrenItem.path" v-if="childrenItem.type == 'link'">
					{{ $t(childrenItem.title) }}
					<label :class="'badge badge-' + childrenItem.badgeType + ' pull-right'" v-if="childrenItem.badgeType">{{
						(childrenItem.badgeValue) }}</label>
					<i class="fa fa-angle-right pull-right mt-1" v-if="childrenItem.children"></i>
				</router-link>
				<ul class="nav-sub-childmenu submenu-content" v-if="childrenItem.children" :class="childrenItem.title == store.subName ? 'opensubchild' : ''">
					<li v-for="(childrenSubItem, index) in childrenItem.children" :key="index">
						<router-link :class="{ 'active': childrenSubItem.active }" :to="childrenSubItem.path" v-if="childrenSubItem.type == 'link'">
							{{ $t(childrenSubItem.title) }}
							<label :class="'badge badge-' + childrenSubItem.badgeType + ' pull-right'" v-if="childrenSubItem.badgeType">{{ (childrenSubItem.badgeValue) }}</label>
							<i class="fa fa-angle-right pull-right" v-if="childrenSubItem.children"></i>
						</router-link>
					</li>
				</ul>
			</li>
		</ul>
	</li>
</template>
<style scoped>
.page-wrapper.compact-wrapper .page-body-wrapper div.sidebar-wrapper .sidebar-main .sidebar-links>li .sidebar-link.active {
	margin-bottom: 0;
}
</style>
<script lang="ts" setup>
import { ref, onMounted, computed } from 'vue';
import { useMenuStore } from "@/store/menu";
import { useRoute } from 'vue-router'
import { useAuth } from '@/composables/useAuth';

const { currentUser, checkAuth } = useAuth();
const store = useMenuStore();
const menu = store.data;

onMounted(async () => {
	await checkAuth();
});

const filteredMenu = computed(() => {
	return menu.filter(item => {
		if (item.headTitle1 === 'User Management' || item.title === 'User Management') {
			const isAdmin = currentUser.value?.is_superuser === true;
			return isAdmin;
		}
		return true;
	});
});

const showPinTitle = computed(() => {
	let show = false;
	menu.filter(item => {
		item.isPinned && (show = true)
		return !show
	})
	return show
})

function togglePinnedName({ item }) {

	item.isPinned = !item.isPinned;
	if (menu.length > 0) {

	} else {

	}
};

const handleUnload = () => {
	let pinsArray: string[] = [];
	menu.forEach(item => {
		item.isPinned && pinsArray.push(item.title);
	});
	localStorage.setItem('pins', JSON.stringify(pinsArray));
};

onMounted(() => {
	window.addEventListener('unload', handleUnload);
	let localPins = JSON.parse(localStorage.getItem('pins') || '[]');
	localPins.forEach((pin: string) => {
		let pinIndex = menu.findIndex(menus => menus.title === pin);


		pinIndex > -1 && (menu[pinIndex].isPinned = true);
	});
});

</script>