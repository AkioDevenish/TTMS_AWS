<template>
    <div class="col-md-12">
        <div class="card">
            <div class="card-header">
                <h4 class="card-title mb-0">API Key</h4>
                <div class="card-options">
                    <a class="card-options-collapse" href="#" data-bs-toggle="card-collapse">
                        <i class="fe fe-chevron-up"></i>
                    </a>
                    <a class="card-options-remove" href="#" data-bs-toggle="card-remove">
                        <i class="fe fe-x"></i>
                    </a>
                </div>
            </div>
            <div class="table-responsive">
                <table class="table">
                    <thead>
                        <tr>
                            <th>API Key Created</th>
                            <th>First Used</th>
                            <th>Last Used</th>
                            <th>Status</th>
                            <th class="text-end">Action</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="(item, index) in useapihistory" :key="index">
                            <td>{{ formatDate(item.date) }}</td>
                            <td>{{ formatDate(item.title) }}</td>
                            <td>{{ formatDate(item.status) }}</td>
                            <td>
                                <span class="badge" :class="item.class">{{ item.price }}</span>
                            </td>
                            <td class="text-end">
                                <a href="javascript:void(0)">
                                    <i class="fa fa-eye"></i> View
                                </a>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    </div>
</template>

<script lang="ts" setup>
import { useapihistory } from "@/core/data/user"

const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
    })
}
</script>