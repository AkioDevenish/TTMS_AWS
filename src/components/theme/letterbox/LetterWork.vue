<template>
    <div class="tab-pane fade" id="work-pill" role="tabpanel" aria-labelledby="work-pill-tab">
        <div class="mail-body-wrapper">
            <ul>
                <li class="inbox-data" v-for="(item, index) in data" :key="index">
                    <div class="inbox-user">
                        <div class="form-check form-check-inline m-0">
                            <input class="form-check-input checkbox-primary" id="emailCheckbox1" type="checkbox"
                                value="option1" />
                            <label class="form-check-label" for="emailCheckbox1"></label>
                        </div>
                        <svg class="important-mail" @click="toggleStar(item)" :class="item.isActive ? 'active' : ''">
                            <use href="@/assets/svg/icon-sprite.svg#fill-star"></use>
                        </svg>
                        <div class="rounded-border">
                            <div v-if="item.textclass">
                                <p :class="item.textclass">{{ item.text }}</p>
                            </div>
                            <img class="img-fluid" v-if="item.img" :src="getImages(item.img)" alt="user" />
                        </div>
                        <p>{{ item.name }}</p>
                    </div>
                    <div class="inbox-message">
                        <div class="email-data" @click="toogle()"><span>{{ item.desctitle }}<span>{{ item.desc
                        }}</span></span>
                            <div class="badge " :class="item.badgeclass">{{ item.badge }}</div>
                            <div class="badge " :class="item.badgeclass1">{{ item.badge1 }}</div>
                        </div>
                        <div class="email-timing"><span>1:00 PM</span></div>
                        <div class="email-options"><i @click="toggleEmail(index)" class="fa fa-envelope-o envelope-1 "
                                :class="activeEmail[index] ? 'hide' : 'show'"></i><i @click="toggleEmail(index)"
                                class="fa fa-envelope-open-o envelope-2 "
                                :class="activeEmail[index] ? 'show' : 'hide'"></i><i class="fa fa-trash-o trash-3"
                                @click="deleteItem(index)"></i><i class="fa fa-print"></i></div>
                    </div>
                </li>

            </ul>
        </div>
    </div>
</template>
<script lang="ts" setup>
import { ref, defineEmits, onMounted, watch } from 'vue'
import { useCommonStore } from "@/store/common"
import { getImages } from "@/composables/common/getImages"
let activeStars = ref<boolean[]>([])
let activeEmail = ref<boolean[]>([])
let store = useCommonStore()
let data = store.works
let emit = defineEmits(['selected'])
function toggleStar(index: any) {
    index.isActive = !index.isActive;
}
function toggleEmail(index: number) {
    activeEmail.value[index] = !activeEmail.value[index];
}
function toogle() {
    emit('selected');
}
function deleteItem(itemId: number) {
    data.splice(itemId, 1)
};
</script>