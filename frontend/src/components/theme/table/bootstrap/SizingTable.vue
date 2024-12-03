<template>
    <Card3 colClass="col-sm-12" table="true" text="true" headerTitle="true" title="Sizing Tables" :desc="desc">
        <div class="card-block row">
            <div class="col-sm-12 col-lg-12 col-xl-12">
                <div class="table-responsive theme-scrollbar">
                    <table class="table table-lg">
                        <thead>
                            <tr>
                                <th scope="col">Id</th>
                                <th scope="col">Employee Name</th>
                                <th scope="col">Date</th>
                                <th scope="col">Status</th>
                                <th scope="col">Hours</th>
                                <th scope="col">Performance</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="(item, index) in sizingTablesXl" :key="index">
                                <th scope="row">{{ item.id }}</th>
                                <td>{{ item.Name }}</td>
                                <td>{{ item.Date }}</td>
                                <td :class="item.statusClass">{{ item.Status }}</td>
                                <td>{{ item.hours }}</td>
                                <td>{{ item.performance }}</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    </Card3>
</template>
<script lang="ts" setup>
import { ref, defineAsyncComponent } from 'vue'
import { sizingTablesXl } from "@/core/data/table"
import { getImages } from "@/composables/common/getImages"
const Card3 = defineAsyncComponent(() => import("@/components/common/card/CardData3.vue"))
let desc = ref<string>("Example of Extra large table, Add<code>.table-xl</code> class to the<code>.table</code> , Large table Add <code> .table-lg</code> , Default table Add <code>.table-de</code> , Small table Add <code>.table-sm </code>, Extra Small table Add <code>.table-xs</code>to create a table.")
</script>