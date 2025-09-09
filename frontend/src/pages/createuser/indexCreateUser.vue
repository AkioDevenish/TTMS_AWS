<template>
  <div v-if="isAdmin" class="container-fluid">
    <div class="row">
      <Card3
          colClass="col-sm-8"
          title="Create New User"
          headerTitle="true"
          descs="Add a new user account to the system"
          cardhaderClass="title-header">
        <NewUserForm />
      </Card3>
    </div>
  </div>
  <div v-else>
    <h3>Access Denied</h3>
    <p>You don't have permission to access this page.</p>
  </div>
</template>

<script lang="ts" setup>
import { defineAsyncComponent, onMounted } from 'vue';
import { useAuthStore } from '@/store/auth';

const Card3 = defineAsyncComponent(() => import('@/components/common/card/CardData3.vue'));
const NewUserForm = defineAsyncComponent(() => import('@/components/theme/users_management/createuser/NewUserForm.vue'));
const authStore = useAuthStore();
const { isAdmin } = authStore;

onMounted(() => {
  // Use isAdmin directly
});
</script>
