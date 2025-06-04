<template>
    <div class="container-fluid">
        <div class="row">
            <Card3 colClass="col-sm-12" title="API Key Usage Logs" headerTitle="true" cardhaderClass="title-header" text="true">
                <!-- The API Key Usage Log Table Component will go here -->
                <!-- We will pass the api_key_uuid to it as a prop -->
                 <ApiKeyUsageLogTable :apiKeyUuid="apiKeyUuid" />
            </Card3>
        </div>
    </div>
</template>

<script lang="ts" setup>
import { ref, defineAsyncComponent, onMounted, watch } from 'vue';
import { useRoute } from 'vue-router';
const Card3 = defineAsyncComponent(() => import("@/components/common/card/CardData3.vue"));
// We will define and import the ApiKeyUsageLogTable component next
const ApiKeyUsageLogTable = defineAsyncComponent(() => import("@/components/theme/api_management/ApiKeyUsageLogTable.vue"));

const route = useRoute();
const apiKeyUuid = ref<string | string[] | null>(null);

// Watch for changes in the route parameters to get the api_key_uuid
watch(() => route.params.uuid, (newUuid) => {
    apiKeyUuid.value = newUuid;
}, { immediate: true }); // Set initial value on mount

</script> 