<template>
	<!-- <div class="loader-wrapper" v-if="showLoader">
    <div class="loader loader-1">
      <div class="loader-outter"></div>
      <div class="loader-inner"></div>
      <div class="loader-inner-1"></div>
    </div>
  </div> -->
	<router-view />
</template>

<script lang="ts" setup>
import { onMounted, ref, watch, onUnmounted } from "vue"
import { useRouter } from 'vue-router'
import { useProductsStore } from "@/store/products"
import { useAuthStore } from '@/store/auth'
import { useProgress } from '@/composables/useProgress';
import { useAWSStationsStore } from '@/store/awsStations'
// let showLoader = ref<boolean>(false)
let router = useRouter()
const { start, done } = useProgress();

const authStore = useAuthStore()
const awsStationsStore = useAWSStationsStore()

router.beforeEach((to, from, next) => {
	start();
	next();
})

router.afterEach(() => {
	done();
})

watch(
	() => router,
	() => {
		// showLoader.value = true;
		// setTimeout(() => {
		//   showLoader.value = false
		// }, 3000);
	},
	{ deep: true },
);
function add() {
	let localItem = JSON.stringify(useProductsStore().cart);
	localStorage.setItem('cart', localItem)

}
onMounted(() => {
	let allBgImageCover = document.getElementsByClassName('bg-img-cover');
	window.addEventListener('beforeunload', add)
	useProductsStore().intialUpload(JSON.parse(localStorage.getItem('cart')) || [])
	setTimeout(() => {
		for (let i = 0; i < allBgImageCover.length; i++) {
			var image = allBgImageCover[i]
			var parentEl: any = allBgImageCover[i].parentElement
			var src = image.getAttribute('src')
			parentEl.style.backgroundImage = "url(" + src + ")"
			parentEl.style.backgroundSize = "cover"
			parentEl.style.backgroundPosition = "center"
			parentEl.classList.add('bg-size')
			image.classList.add('d-none')
		}
	}, 0);

	console.log('App mounted')
	// Removed authStore.checkAuth() to avoid duplicate /me requests
	awsStationsStore.init()
})
onUnmounted(() => {
	window.removeEventListener('beforeunload', add)

})
</script>