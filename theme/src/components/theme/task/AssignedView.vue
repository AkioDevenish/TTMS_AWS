<template>
    <div class="fade tab-pane" id="pills-assigned" role="tabpanel" aria-labelledby="pills-assigned-tab">
        <div class="card mb-0">
            <div class="card-header d-flex">
                <h4 class="mb-0">Assigned to me</h4><a @click="printWindow()"><vue-feather class="me-2"
                        type="printer"></vue-feather>Print</a>
            </div>
            <div class="card-body p-0">
                <div class="taskadd">
                    <div class="table-responsive theme-scrollbar">
                        <table class="table">
                            <tbody>
                                <tr v-for="(row, index) in task" :key="index">
                                    <td>
                                        <h6 class="task_title_0 f-w-600">{{ row.title }}</h6>
                                        <p class="project_name_0">General</p>
                                    </td>
                                    <td>
                                        <p class="task_desc_0">{{ row.desc }}</p>
                                    </td>
                                    <td><a class="me-2" href="javascript:void(0)"><vue-feather
                                                type="link"></vue-feather></a><a href="javascript:void(0)"><vue-feather
                                                type="more-horizontal"></vue-feather></a>
                                    </td>
                                    <td><a href="javascript:void(0)"><vue-feather type="trash-2"
                                                @click='removeProduct(index)'></vue-feather></a></td>
                                </tr>
                            </tbody>

                        </table>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
<script lang="ts" setup>
import { useTaskStore } from "@/store/task"
import Swal from 'sweetalert2'
const store = useTaskStore()
let task = store.task

function removeProduct(index: any) {
    Swal.fire({
        icon: 'warning',
        title: "Are you sure?",
        text: 'This Task will be deleted from your Personal task ',
        showCancelButton: true,
        cancelButtonText: 'Cancel', confirmButtonText: 'Ok', confirmButtonColor: 'var(--theme-deafult)',
    }).then((result: any) => {
        if (result.value) {
            task.splice(index, 1)
            Swal.fire({
                icon: 'success',
                text: 'Poof! Your imaginary file has been deleted!',
                confirmButtonColor: 'var(--theme-deafult)',
            });
        } else {
            Swal.fire({
                text: 'Your contact is safe!', confirmButtonColor: 'var(--theme-deafult)',
            });
        }
    });
}
function printWindow() {
    window.print();
}
</script>