<template>
    <div class="col-md-6">
        <div class="card">
            <div class="card-header">
                <h4>Flat input style</h4>
                <p class="f-m-light mt-1">
                    Use the <code>.btn-square </code>through defined 0px border-radius.</p>
            </div>
            <form class="form theme-form dark-inputs">
                <div class="card-body">
                    <div class="row">
                        <div class="col">
                            <div class="mb-3">
                                <label class="form-label" for="exampleFormControlSelect12">Select your favorite roman
                                    number</label>
                                <select class="form-select btn-square digits" id="exampleFormControlSelect12">
                                    <option v-for="(item, index) in roman" :key="index">{{ item }} </option>
                                </select>
                            </div>
                        </div>
                    </div>
                    <div class="row">
                        <div class="col">
                            <div class="mb-3">
                                <label class="form-label" for="exampleFormControlSelect13">Select your multiple
                                    paintings</label>
                                <select class="form-select btn-square digits" id="exampleFormControlSelect13" multiple>
                                    <option class="rounded-0" v-for="(item, index) in paint" :key="index">{{ item }}
                                    </option>
                                </select>
                            </div>
                        </div>
                    </div>
                    <div class="row">
                        <div class="col">
                            <div>
                                <label class="form-label" for="exampleFormControlTextarea14">Please do comments</label>
                                <textarea class="form-control btn-square" id="exampleFormControlTextarea14"
                                    rows="3"></textarea>
                            </div>
                        </div>
                    </div>
                </div>
            </form>
        </div>
    </div>
</template>
<script lang="ts" setup>
import { ref, defineAsyncComponent } from 'vue'
const Card3 = defineAsyncComponent(() => import("@/components/common/card/CardData3.vue"))
let desc = ref<string>("For default file/multiple file/disabled file/small file/large file input for use <code>&lt;input&gt; </code>with <code>(type='file').</code>")
let paint = ref<string[]>(["Landscape", "Portrait", "Oil Painting", "Abstract art", "Acrylic"])
let roman = ref<string[]>(["I", "II", "III", "IV", "V"])
</script>