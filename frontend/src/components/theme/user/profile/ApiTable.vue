<template>
    <div class="col-md-12">
        <div class="card">
            <div class="card-header">
                <h4 class="card-title mb-0">API History</h4>
                <div class="card-options"><a class="card-options-collapse" href="#" data-bs-toggle="card-collapse"><i
                            class="fe fe-chevron-up"></i></a><a class="card-options-remove" href="#"
                        data-bs-toggle="card-remove"><i class="fe fe-x"></i></a></div>
            </div>
            <div class="table-responsive add-project">
                <table class="table card-table table-vcenter text-nowrap">
                    <thead>
                        <tr>
                            <th>Date</th>
                            <th>First Used</th>
                            <th>Last Used</th>
                            <th>Status</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="(item, index) in useapihistory" :key="index">
                         
                            <td>{{ item.date }}</td>
                            <td><a class="text-inherit" href="#">{{ item.title }}</a></td>
                            <td><span class="status-icon " :class="item.class"></span> {{ item.status }}</td>
                            <td>{{ item.price }}</td>
                            <td class="text-end"><a class="icon" href="javascript:void(0)"></a><a
                                    class="btn btn-transparent btn-sm" href="javascript:void(0)"><i class="fa fa-link"></i>
                                    View</a><a class="icon" href="javascript:void(0)"></a></td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    </div>
</template>
<script lang="ts" setup>
import { useapihistory } from "@/core/data/user"
</script>