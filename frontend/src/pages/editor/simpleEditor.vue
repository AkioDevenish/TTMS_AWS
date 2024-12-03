<template>
    <div class="container-fluid">
        <div class="row">
            <Card3 colClass="col-sm-12" title="Simple Editor" headerTitle="true">
                <quill-editor v-model:value="state.content" :options="state.editorOption"
                    @change="onEditorChange($event)" />
            </Card3>
        </div>
    </div>
</template>
<script lang="ts" setup>
import { ref, reactive, defineAsyncComponent } from 'vue';

let Card3 = defineAsyncComponent(() => import("@/components/common/card/CardData3.vue"))
const state = reactive({
    content: '<h1>Some initial content</h1>',
    _content: '',
    editorOption: {
        placeholder: 'core',
    },
    disabled: false
})
const onEditorChange = (html: string) => {

    state._content = html
}
setTimeout(() => {
    state.disabled = true
}, 2000)
</script>