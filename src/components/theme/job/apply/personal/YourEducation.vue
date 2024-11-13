<template>
    <h6 class="mb-0">Your Education</h6>
    <form class="form theme-form">
        <div class="row">
            <div class="col-xl-6 xl-100">
                <div class="mb-3">
                    <label class="form-label" for="exampleFormControlInput5">College Name:<span
                            class="font-danger">*</span></label>
                    <input class="form-control" id="exampleFormControlInput5" type="text" placeholder="Enter college name">
                </div>
            </div>
            <DateView />
            <div class="col-xl-6 xl-100">
                <div class="mb-3">
                    <label class="form-label">Degree Level:<span class="font-danger">*</span></label>
                    <multiselect v-model="multiValue1" tag-placeholder="Add this as new tag" placeholder="Select Your Name"
                        label="name" track-by="code" :options="options1" :multiple="false" :taggable="true"></multiselect>
                </div>
            </div>
            <div class="col-xl-6 xl-100">
                <div class="mb-3">
                    <label class="form-label" for="exampleFormControlInput6">Specialization:<span
                            class="font-danger">*</span></label>
                    <input class="form-control" id="exampleFormControlInput6" type="text"
                        placeholder="Enter specialization">
                </div>
            </div>
        </div>
    </form>
    <h6 class="mb-0">Your Experience</h6>
    <form class="form theme-form">
        <div class="row">
            <div class="col-xl-6 xl-100">
                <div class="mb-3">
                    <label class="form-label" for="exampleFormControlInput7">Location:<span
                            class="font-danger">*</span></label>
                    <input class="form-control" id="exampleFormControlInput7" type="text" placeholder="Enter Location">
                </div>
            </div>
            <div class="col-xl-6 xl-100 xl-mt-job">
                <label class="col-form-label text-end pt-0">Period:<span class="font-danger">*</span></label>
                <div class="row">
                    <div class="col-sm-6">
                        <div class="input-group">
                            <Datepicker class="form-control" v-model="date" />
                        </div>
                    </div>
                    <div class="col-sm-6 xs-mt-period">
                        <div class="input-group">
                            <Datepicker class="form-control" v-model="date1" />
                        </div>
                    </div>
                </div>
            </div>
            <div class="col-xl-6 xl-100">
                <div class="mb-3">
                    <label class="form-label">Position:<span class="font-danger">*</span></label>
                    <multiselect v-model="multiValue" tag-placeholder="Add this as new tag" placeholder="Select Your Name"
                        label="name" track-by="code" :options="options" :multiple="false" :taggable="true"></multiselect>
                </div>
            </div>
            <div class="col-xl-6 xl-100">
                <div class="mb-3">
                    <label class="form-label" for="exampleFormControlInput8">Company Name:<span
                            class="font-danger">*</span></label>
                    <input class="form-control" id="exampleFormControlInput8" type="text" placeholder="Enter Company Name">
                </div>
            </div>
        </div>
    </form>
</template>
<script lang="ts" setup>
import { ref, reactive, defineAsyncComponent } from "vue"

const DateView = defineAsyncComponent(() => import("@/components/theme/job/apply/personal/DateView.vue"))
let date = ref();
let date1 = ref();
interface multi {
    code: number,
    name: string
}
const multiValue = ref([{ code: 1, name: 'Choose a option' },])
const multiValue1 = ref([{ code: 1, name: 'Student' },])
const options = ref<multi[]>([
    { code: 1, name: 'Choose a option' },
    { code: 2, name: 'Web Designer' },
    { code: 3, name: 'Graphic Designer' },
    { code: 4, name: 'UI Designer' },
    { code: 5, name: 'UI/UX Designer' },
])
const options1 = ref<multi[]>([
    { code: 1, name: 'Student' },
    { code: 2, name: 'Bachelor' },
    { code: 3, name: 'Master' },
    { code: 4, name: 'Associate' },
])
</script>