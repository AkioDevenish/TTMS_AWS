<template>
    <Card3 colClass="col-xl-6" pre="true" cardbodyClass="main-custom-form card-wrapper input-group-wrapper"
        preClass="f-m-light mt-1" headerTitle="true" title="Buttons with dropdowns" :desc="desc">
        <div class="input-group">
            <button class="btn btn-outline-info dropdown-toggle" type="button" data-bs-toggle="dropdown"
                aria-expanded="false">Dropdown</button>
            <ul class="dropdown-menu dropdown-block">
                <li><a class="dropdown-item" href="javascript:void(0)">Ecommerce</a></li>
                <li><a class="dropdown-item" href="javascript:void(0)">Email</a></li>
                <li><a class="dropdown-item" href="javascript:void(0)">Users</a></li>
                <li>
                    <hr class="dropdown-divider">
                </li>
                <li><a class="dropdown-item" href="javascript:void(0)">Bookmarks</a></li>
            </ul>
            <input class="form-control" type="text" aria-label="Text input with dropdown button">
        </div>
        <div class="input-group">
            <input class="form-control" type="text" aria-label="Text input with dropdown button">
            <button class="btn btn-outline-danger dropdown-toggle" type="button" data-bs-toggle="dropdown"
                aria-expanded="false">Dropdown</button>
            <ul class="dropdown-menu dropdown-menu-end dropdown-block">
                <li><a class="dropdown-item" href="javascript:void(0)">Starter kit</a></li>
                <li><a class="dropdown-item" href="javascript:void(0)">Gallery</a></li>
                <li><a class="dropdown-item" href="javascript:void(0)">Blog</a></li>
                <li>
                    <hr class="dropdown-divider">
                </li>
                <li><a class="dropdown-item" href="javascript:void(0)">Maps</a></li>
            </ul>
        </div>
        <div class="input-group">
            <button class="btn btn-secondary dropdown-toggle" type="button" data-bs-toggle="dropdown"
                aria-expanded="false">Dropdown</button>
            <ul class="dropdown-menu dropdown-block">
                <li><a class="dropdown-item" href="javascript:void(0)">Widgets</a></li>
                <li><a class="dropdown-item" href="javascript:void(0)">Project</a></li>
                <li><a class="dropdown-item" href="javascript:void(0)">Contacts</a></li>
                <li>
                    <hr class="dropdown-divider">
                </li>
                <li><a class="dropdown-item" href="javascript:void(0)">Tasks</a></li>
            </ul>
            <input class="form-control" type="text" aria-label="Text input with 2 dropdown buttons">
            <button class="btn btn-primary dropdown-toggle" type="button" data-bs-toggle="dropdown"
                aria-expanded="false">Dropdown</button>
            <ul class="dropdown-menu dropdown-menu-end dropdown-block">
                <li><a class="dropdown-item" href="javascript:void(0)">To-Do</a></li>
                <li><a class="dropdown-item" href="javascript:void(0)">FAQ</a></li>
                <li><a class="dropdown-item" href="javascript:void(0)">Knowledgebase</a></li>
                <li>
                    <hr class="dropdown-divider">
                </li>
                <li><a class="dropdown-item" href="javascript:void(0)">Support Ticket</a></li>
            </ul>
        </div>
    </Card3>
</template>
<script lang="ts" setup>
import { ref, defineAsyncComponent } from 'vue'
import { customform } from "@/core/data/forms"
const Card3 = defineAsyncComponent(() => import("@/components/common/card/CardData3.vue"))
let desc = ref<string>("Use the<code>.input-group </code>and <code>[aria-label='']</code> through buttons with dropdowns.")
</script>