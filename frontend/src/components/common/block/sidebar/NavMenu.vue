<template>
	<li class="back-btn"><router-link to="/"><img class="img-fluid" src="@/assets/images/logo/logo-icon.png" alt=""></router-link>
		<div class="mobile-back text-end"><span>Back</span><i class="fa fa-angle-right ps-2" aria-hidden="true"></i></div>
	</li>
	<li class="pin-title sidebar-main-title" :class="showPinTitle ? 'show' : ''">
		<div>
			<h6>Pinned</h6>
		</div>
	</li>
	<li v-for="(menuItem, index) in filteredMenu" :key="index"
		v-show="shouldShowMenuItem(menuItem)"
		class="sidebar-list"
		:class="[{ ' sidebar-main-title': menuItem.type == 'headtitle' }, menuItem.isPinned ? 'pined' : '']">
		<div v-if="menuItem.type == 'headtitle'">
			<h6 class="lan-1">{{ $t(menuItem.headTitle1 || '') }}</h6>
		</div>
		<i v-if="menuItem.type != 'headtitle'" class="fa fa-thumb-tack" @click="togglePinnedName({ item: menuItem })"></i>
		<a href="javascript:void(0)" class="sidebar-link sidebar-title" v-if="menuItem.type == 'sub'" :class="(menuItem.title || '') == store.perentName ? 'active' : ''" @click="store.subMenuToggle(menuItem.title || '')">
			<svg class="stroke-icon">
				<use :xlink:href="require('@/assets/svg/icon-sprite.svg') + `#${menuItem.icon || ''}`"></use>
			</svg>
			<svg class="fill-icon">
				<use :xlink:href="require('@/assets/svg/icon-sprite.svg') + `#${menuItem.icon1 || ''}`"></use>
			</svg>
			<span class="lan-6">
				{{ $t(menuItem.title || '') }}
			</span>
			<div class="according-menu" v-if="menuItem.children">
				<i class="pull-right" :class="[(menuItem.title || '') == store.perentName ? 'fa fa-angle-down' : 'fa fa-angle-right']"></i>
			</div>
		</a>
		<router-link :to="menuItem.path || ''" class="sidebar-link sidebar-title" v-if="menuItem.type == 'link'" :class="(menuItem.title || '') == store.perentName ? 'active' : ''" @click="store.subMenuToggle(menuItem.title || '')">
			<svg class="stroke-icon">
				<use :xlink:href="require('@/assets/svg/icon-sprite.svg') + `#${menuItem.icon || ''}`"></use>
			</svg>
			<svg class="fill-icon">
				<use :xlink:href="require('@/assets/svg/icon-sprite.svg') + `#${menuItem.icon1 || ''}`"></use>
			</svg>
			<span>
				{{ $t(menuItem.title || '') }}
			</span>
			<i class="fa fa-angle-right pull-right" v-if="menuItem.children"></i>
		</router-link>
		<a :href="menuItem.path || ''" class="sidebar-link sidebar-title" v-if="menuItem.type == 'extLink'">
			<svg class="stroke-icon">
				<use :xlink:href="require('@/assets/svg/icon-sprite.svg') + `#${menuItem.icon || ''}`"></use>
			</svg>
			<svg class="fill-icon">
				<use :xlink:href="require('@/assets/svg/icon-sprite.svg') + `#${menuItem.icon1 || ''}`"></use>
			</svg>
			<span>
				{{ $t(menuItem.title || '') }}
			</span>
			<i class="fa fa-angle-right pull-right" v-if="menuItem.children"></i>
		</a>
		<a :href="menuItem.path || ''" target="_blank" class="sidebar-link sidebar-title" v-if="menuItem.type == 'extTabLink'">
			<svg class="stroke-icon">
				<use :xlink:href="require('@/assets/svg/icon-sprite.svg') + `#${menuItem.icon || ''}`"></use>
			</svg>
			<svg class="fill-icon">
				<use :xlink:href="require('@/assets/svg/icon-sprite.svg') + `#${menuItem.icon1 || ''}`"></use>
			</svg>
			<span>
				{{ $t(menuItem.title || '') }}
			</span>
			<i class="fa fa-angle-right pull-right" v-if="menuItem.children"></i>
		</a>
		<ul class="sidebar-submenu" v-if="menuItem.children" :style="(menuItem.title || '') == store.perentName ? 'display:block' : 'display:none'">
			<li v-for="(childrenItem, index) in menuItem.children" :key="index">
				<a class="lan-4" :class="{ 'active': childrenItem.active }" href="javascript:void(0)" v-if="childrenItem.type == 'sub'" @click="store.subChildMenu(childrenItem.title || '')">
					{{ $t(childrenItem.title || '') }}
					<label :class="'badge badge-' + childrenItem.badgeType + ' pull-right'" v-if="childrenItem.badgeType">{{
						childrenItem.badgeValue }}</label>
					<i class="fa pull-right" v-bind:class="[(childrenItem.title || '') == store.subName ? 'fa fa-angle-down' : 'fa fa-angle-right']" v-if="childrenItem.children"></i>
				</a>
				<router-link class="lan-4" :class="{ 'active': childrenItem.active }" :to="childrenItem.path || ''" v-if="childrenItem.type == 'link'">
					{{ $t(childrenItem.title || '') }}
					<label :class="'badge badge-' + childrenItem.badgeType + ' pull-right'" v-if="childrenItem.badgeType">{{
						(childrenItem.badgeValue) }}</label>
					<i class="fa fa-angle-right pull-right mt-1" v-if="childrenItem.children"></i>
				</router-link>
				<ul class="nav-sub-childmenu submenu-content" v-if="childrenItem.children" :class="(childrenItem.title || '') == store.subName ? 'opensubchild' : ''">
					<li v-for="(childrenSubItem, index) in childrenItem.children" :key="index">
						<router-link :class="{ 'active': childrenSubItem.active }" :to="childrenSubItem.path || ''" v-if="childrenSubItem.type == 'link'">
							{{ $t(childrenSubItem.title || '') }}
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
import type { MenuItem } from '@/core/data/menu';
import { ref, onMounted, computed, watch, nextTick } from 'vue';
import { useMenuStore } from "@/store/menu";
import { useRoute } from 'vue-router'
import { useAuthStore } from '@/store/auth';
import { menu } from '@/core/data/menu'

const authStore = useAuthStore();
const { currentUser, isAdmin, isStaff } = authStore;
const store = useMenuStore();

// Get the original menu directly
const rawMenu = computed<MenuItem[]>(() => menu);

// Use the original menu for filtering in the component
const filteredMenu = computed<MenuItem[]>(() => {
	// Log admin status directly
	console.log('NavMenu - filteredMenu computed - isAdmin:', isAdmin);
	
	return menu.filter(item => {
		// Regular items with admin property
		if (item.type !== 'headtitle' && item.admin === 1) {
			return isAdmin;
		}
		
		// System Management header
		if (item.type === 'headtitle' && 
			(item.headTitle1 === 'System Management' || item.headTitle2 === 'System Management')) {
			return isAdmin;
		}
		
		// Show everything else
		return true;
	});
});

onMounted(() => {
	// Force a re-evaluation
	console.log('Auth check completed, isAdmin:', isAdmin);
});

const showPinTitle = computed(() => {
	return filteredMenu.value.some(item => item.isPinned);
});

function togglePinnedName({ item }: { item: MenuItem }) {
	item.isPinned = !item.isPinned;
}

const handleUnload = () => {
	let pinsArray: string[] = [];
	menu.forEach(item => {
		if (item.isPinned && item.title) {
			pinsArray.push(item.title);
		}
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

function shouldShowMenuItem(item: MenuItem): boolean {
	return true; // Let the computed property handle the filtering
}

// Add a watcher to debug isAdmin changes
watch(() => isAdmin, (newValue) => {
	console.log('isAdmin value changed:', newValue);
});
</script>