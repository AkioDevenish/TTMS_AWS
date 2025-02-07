<template>
	<div class="container-fluid">
		<div class="row">
			<Card3 colClass="col-sm-12">
				<Addinstrument />
			</Card3>
		</div>
	</div>
</template>
<script lang="ts" setup>
import { ref, defineAsyncComponent } from 'vue'
const Addinstrument = defineAsyncComponent(() => import("@/components/theme/dashboards/createproject/Addinstrument.vue"))
const Card3 = defineAsyncComponent(() => import("@/components/common/card/CardData3.vue"))
</script>