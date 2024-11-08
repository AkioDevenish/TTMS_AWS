<template>
    <div class="col-xl-6">
        <div class="card height-equal">
            <div class="card-header">
                <h4>Basic HTML input control</h4>
                <p class="f-m-light mt-1">
                    Give textual form controls like <code>&lt;input&gt;</code>s and <code>&lt;textarea&gt;</code>s an
                    upgrade with custom styles, sizing, focus states, and more.</p>
            </div>
            <form class="form theme-form">
                <div class="card-body custom-input">
                    <div class="row">
                        <div class="col">
                            <div class="mb-3 row" v-for="(item, index) in input" :key="index">
                                <label class="col-sm-3">{{ item.title }}</label>
                                <div class="col-sm-9">
                                    <input :class="item.class" :type="item.type" :placeholder="item.placeholder"
                                        :value="item.value">
                                </div>
                            </div>
                            <div class="mb-3 row">
                                <div class="col-sm-3">
                                    <label class="form-label" for="exampleDataList">Datalist example</label>
                                </div>
                                <div class="col-sm-9">
                                    <input class="form-control" id="exampleDataList" list="datalistOptions"
                                        placeholder="Look up your nation...">
                                    <datalist id="datalistOptions">
                                        <option v-for="(item, index) in nation" :key="index" :value="item"></option>
                                    </datalist>
                                </div>
                            </div>
                            <div class="mb-3 row">
                                <label class="col-sm-3">Time</label>
                                <div class="col-sm-9">
                                    <input class="form-control digits" type="time" value="21:45:00">
                                </div>
                            </div>
                            <div class="mb-3 row">
                                <label class="col-sm-3 pt-0">Color picker</label>
                                <div class="col-sm-2">
                                    <input class="form-control form-control-color" type="color" value="#563d7c">
                                </div>
                            </div>
                            <div class="mb-3 row">
                                <label class="col-sm-3">
                                    Maximum
                                    Length
                                </label>
                                <div class="col-sm-9">
                                    <input class="form-control" type="text" placeholder="Content must be in 6 characters"
                                        maxlength="6">
                                </div>
                            </div>
                            <div class="row">
                                <label class="col-sm-3">Static Text</label>
                                <div class="col-sm-9">
                                    <div class="form-control-static">
                                        Hello !... This is
                                        my magical text
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="card-footer text-end">
                    <div class="col-sm-9 offset-sm-3">
                        <button class="btn btn-primary me-3" type="submit">Submit</button>
                        <input class="btn btn-light" type="reset" value="Cancel">
                    </div>
                </div>
            </form>
        </div>
    </div>
</template>
<script lang="ts" setup>
import { ref } from "vue"
import { input } from "@/core/data/forms"
let nation = ref<string[]>(["San Francisco", "New York", "Seattle", "Los Angeles", "Chicago", "India"])
</script>