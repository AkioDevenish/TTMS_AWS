<template>
	<div class="col-4 col-xl-4 page-title" v-if="useRoute().path == '/'">
		<h4 class="f-w-700">Default dashboard</h4>
		<nav>
			<ol class="breadcrumb justify-content-sm-start align-items-center mb-0">
				<li class="breadcrumb-item"><router-link to="/"> <vue-feather type="home"> </vue-feather></router-link></li>
				<li class="breadcrumb-item f-w-400 text-capitalize">Dashboard</li>
				<li class="breadcrumb-item f-w-400 active text-capitalize">Dashboard Default</li>
			</ol>
		</nav>
	</div>
	<div class="col-4 col-xl-4 page-title" v-else>
		<h4 class="f-w-700 text-capitalize">{{ route.name /*route.path.replaceAll("_", " ").split('/').slice(1)[1]*/ }}</h4>
		<nav>
			<ol class="breadcrumb justify-content-sm-start align-items-center mb-0">
				<li class="breadcrumb-item"><router-link to="/"> <vue-feather type="home"> </vue-feather></router-link></li>
				<li class="breadcrumb-item f-w-400 text-capitalize">{{ route.path.split('/').slice(1)[0] }}
				</li>
				<li class="breadcrumb-item f-w-400 text-capitalize" v-if="route.path.split('/').slice(1).length > 1 && route.path.split('/').slice(1).length > 3">{{
					route.path.split('/').slice(1)[route.path.split('/').slice(1).length - 2]
				}}</li>
				<li class="breadcrumb-item f-w-400 active text-capitalize">{{
					route.path.replaceAll("_", " ").split('/').slice(1)[route.path.replaceAll("_", "")
						.split('/').slice(1).length - 1] }}</li>
			</ol>
		</nav>
	</div>
</template>
<script lang="ts" setup>
import { ref, onMounted, computed } from 'vue';
import { useRoute } from 'vue-router'
let route = useRoute()

</script>