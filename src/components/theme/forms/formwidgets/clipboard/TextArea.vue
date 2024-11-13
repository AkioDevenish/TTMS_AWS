<template>
    <Card3 colClass="col-sm-12 col-md-6" headerTitle="true" title="Clipboard on textarea">
        <div class="clipboaard-container">
            <p class="f-16">Cut/copy from textarea</p>
            <textarea class="form-control f-14" id="clipboardExample2" v-model="textArea" rows="3"
                spellcheck="false">A web designer must always enhance their work since creating websites is a creative effort. Therefore, a web designer must be more imaginative to produce exceptional results. Blogs about web design assist web designers in learning about new technologies, offer lessons, news, direction for a freebie, and much more. These blogs allow web designers to stay creative and improve their abilities. Therefore, advice from web design blogs is required to improve your business.</textarea>
            <div class="mt-3 text-end">
                <button class="btn btn-warning btn-clipboard mx-1" type="button" @click="copyTextareaInput"
                    data-clipboard-action="copy" data-clipboard-target="#clipboardExample2"><i class="fa fa-copy"></i>
                    Copy</button>
                <button class="btn btn-success btn-clipboard-cut" type="button" @click="cut" data-clipboard-action="cut"
                    data-clipboard-target="#clipboardExample2"><i class="fa fa-cut"></i>
                    Cut</button>
            </div>
        </div>
    </Card3>
</template>
<script lang="ts" setup>
import { ref, defineAsyncComponent } from 'vue'
const Card3 = defineAsyncComponent(() => import("@/components/common/card/CardData3.vue"))
let textArea = ref<string>('A web designer must always enhance their work since creating websites is a creative effort. Therefore, a web designer must be more imaginative to produce exceptional results. Blogs about web design assist web designers in learning about new technologies, offer lessons, news, direction for a freebie, and much more. These blogs allow web designers to stay creative and improve their abilities. Therefore, advice from web design blogs is required to improve your business.')
function copyTextareaInput() {
    navigator.clipboard.writeText(textArea.value);
    alert('copied');
}
function cut() {
    navigator.clipboard.writeText(textArea.value);
    textArea.value = '';
    alert('cut');
}
</script>