<template>
    <Card3 colClass="col-sm-12" table="true" text="true" headerTitle="true" title="Inverse Table" :desc="desc">
        <div class="table-responsive theme-scrollbar">
            <table class="table table-inverse">
                <thead>
                    <tr class="border-bottom-light">
                        <th scope="col">Id</th>
                        <th scope="col">First Name</th>
                        <th scope="col">Last Name</th>
                        <th scope="col">Office</th>
                        <th scope="col">Position</th>
                        <th scope="col">Salary</th>
                        <th scope="col">Join Date </th>
                        <th scope="col">Age</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="(data, index) in inverse" :key="index">
                        <th scope="row">{{ data.id }}</th>
                        <td>{{ data.firstName }}</td>
                        <td>{{ data.lastName }}</td>
                        <td>{{ data.office }}</td>
                        <td>{{ data.role }}</td>
                        <td>{{ data.salary }}</td>
                        <td>{{ data.join }}</td>
                        <td>{{ data.age }}</td>
                    </tr>

                </tbody>
            </table>
        </div>
    </Card3>
</template>
<script lang="ts" setup>
import { ref, defineAsyncComponent } from 'vue'
import { inverse } from "@/core/data/table"
import { getImages } from "@/composables/common/getImages"
const Card3 = defineAsyncComponent(() => import("@/components/common/card/CardData3.vue"))
let desc = ref<string>("Use a class <code>table-inverse</code> inside table element.")
</script>