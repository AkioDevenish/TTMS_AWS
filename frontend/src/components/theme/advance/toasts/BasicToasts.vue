<template>
    <Card3 colClass="col-sm-6" cardbodyClass="btn-showcase" headerTitle="true" title="Toastr">
        <button class="btn btn-success " type="button" @click="success" variant="success">Success</button>

        <button class="btn btn-info " type="button" @click="info" variant="info">Info</button>

        <button class="btn btn-danger " type="button" @click="error" variant="danger">Error</button>
    </Card3>
</template>
<script lang="ts" setup>
import { toast } from 'vue3-toastify';
import 'vue3-toastify/dist/index.css';
import { defineAsyncComponent } from 'vue'
const Card3 = defineAsyncComponent(() => import("@/components/common/card/CardData3.vue"))

function success() {
    toast.success(' New order has been placed ', {
        hideProgressBar: true, autoClose: 2000, theme: 'colored', position: 'top-right'
    });
}
function info() {
    toast.info(' New order has been placed ', {
        hideProgressBar: true, autoClose: 2000, theme: 'colored', position: 'top-right'
    });
}
function error() {
    toast.error(' New order has been placed ', {
        hideProgressBar: true, autoClose: 2000, theme: 'colored', position: 'top-right'
    });
}
</script>