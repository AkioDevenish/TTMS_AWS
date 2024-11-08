<template>
    <Card3 colClass="col-sm-12" table="true" text="true" headerTitle="true" title="Hoverable Rows With Horizontal Border"
        :desc="desc">
        <div class="table-responsive theme-scrollbar signal-table">
            <table class="table table-hover">
                <thead>
                    <tr>
                        <th scope="col">Id</th>
                        <th scope="col">Status</th>
                        <th scope="col">Signal Name </th>
                        <th scope="col">Security</th>
                        <th scope="col">Stage</th>
                        <th scope="col">Schedule</th>
                        <th scope="col">Team Lead</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="(data, index) in hoverable" :key="index">
                        <th scope="row">{{ data.id }}</th>
                        <td :Class="data.status" class="d-flex align-items-center">

                            <vue-feather :class="data.bgClass" :type="data.icon"></vue-feather>
                            <span :class="data.font">{{ data.status }}</span>
                        </td>
                        <td>{{ data.signalName }}</td>
                        <td>{{ data.security }}</td>
                        <td>{{ data.stage }}</td>
                        <td>{{ data.schedule }}</td>
                        <td>{{ data.teamLead }}</td>
                    </tr>

                </tbody>
            </table>
        </div>
    </Card3>
</template>
<script lang="ts" setup>
import { ref, defineAsyncComponent } from 'vue'
import { hoverable } from "@/core/data/table"
import { getImages } from "@/composables/common/getImages"
const Card3 = defineAsyncComponent(() => import("@/components/common/card/CardData3.vue"))
let desc = ref<string>("Hoverable row use a class <code>table-hover</code> and for Horizontal border use a class <code>.table-border-horizontal</code> , dashed border Use a class<code>.border-dashed .table</code>class.")
</script>