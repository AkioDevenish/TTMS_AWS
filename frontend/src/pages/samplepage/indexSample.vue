<template>
    <div class="container-fluid">
        <div class="row">

            <Card3 colClass="col-sm-12" headerTitle="true" title="Sample Card" :desc="desc" text="true">
                <p>"Sample-page" is a generic term used to refer to a basic, placeholder, or example page that
                    developers or designers use as a starting point for building or testing a website or
                    application. It is not an official or standard term but rather a descriptive name commonly
                    used in web development and design contexts A sample page typically contains basic elements
                    like headings, paragraphs, images, buttons, and links. It may also include placeholder text
                    or images to represent content that will be replaced with actual content in the final
                    version.</p>
            </Card3>

        </div>
    </div>
</template>
<script lang="ts" setup>
import { ref, defineAsyncComponent } from 'vue'
const Card3 = defineAsyncComponent(() => import("@/components/common/card/CardData3.vue"))
let desc = ref<string>("lorem ipsum dolor sit amet, consectetur adipisicing elit")
</script>