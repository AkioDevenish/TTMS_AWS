<template>
  <div class="col-4 col-xl-4 page-title" v-if="useRoute().path == '/'">
    <h4 class="f-w-700">Dashboard</h4>
    <nav>
      <ol class="breadcrumb justify-content-sm-start align-items-center mb-0">
        <li class="breadcrumb-item">
          <router-link to="/">
            <vue-feather type="home"></vue-feather>
          </router-link>
        </li>
        <li class="breadcrumb-item f-w-400 text-capitalize">Dashboard</li>
        <li class="breadcrumb-item f-w-400 active text-capitalize">Dashboard</li>
      </ol>
    </nav>
  </div>
  <div class="col-4 col-xl-4 page-title" v-else>
    <h4 class="f-w-700 text-capitalize">{{ route.name }}</h4>
    <nav>
      <ol class="breadcrumb justify-content-sm-start align-items-center mb-0">
        <li class="breadcrumb-item">
          <router-link to="/">
            <vue-feather type="home"></vue-feather>
          </router-link>
        </li>
        <!--<li class="breadcrumb-item f-w-400 text-capitalize">1. {{ route.path.split('/').slice(1)[0] }}</li>-->
        <!--<li-->
        <!--    class="breadcrumb-item f-w-400 text-capitalize"-->
        <!--    v-if="route.path.split('/').slice(1).length > 1 && route.path.split('/').slice(1).length > 3">-->
        <!--  2. {{ route.path.split('/').slice(1)[route.path.split('/').slice(1).length - 2] }}-->
        <!--</li>-->
        <!--<li-->
        <!--    class="breadcrumb-item f-w-400 active text-capitalize">-->
        <!--  3. {{-->
        <!--    route.path.replaceAll('_', ' ').split('/').slice(1)[route.path.replaceAll('_', '').split('/').slice(1).length - 1]-->
        <!--  }}-->
        <!--</li>-->

        <li
            v-for="(segment, idx) in formattedRoute"
            :key="idx"
            class="breadcrumb-item f-w-400 text-capitalize"
            :class="{ active: idx === formattedRoute.length - 1 }"
        >
          {{ segment }}
        </li>
      </ol>
    </nav>
  </div>
</template>
<script lang="ts" setup>
  import { ref, onMounted, computed } from 'vue';
  import { useRoute } from 'vue-router';

  let route = useRoute();

  const formattedRoute = computed(() => {
    return route.path
        .split('/')
        .filter(Boolean)
        .map(segment => segment
            .replace(/_/g, ' ')
            .replace(/\b\w/g, c => c.toUpperCase())
        );
  });

</script>
