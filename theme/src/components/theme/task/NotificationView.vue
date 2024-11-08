<template>
    <div class="fade tab-pane" id="pills-notification" role="tabpanel" aria-labelledby="pills-notification-tab">
        <div class="card mb-0">
            <div class="card-header d-flex">
                <h4 class="mb-0">Notification</h4><a href="javascript:void(0)" @click="printWindow()"><vue-feather
                        class="me-2" type="printer"></vue-feather>Print</a>
            </div>
            <div class="card-body">
                <div class="details-bookmark text-center"><span>No tasks found.</span></div>
            </div>
        </div>
    </div>
</template>
<script lang="ts" setup>
function printWindow() {
    window.print();
}
</script>