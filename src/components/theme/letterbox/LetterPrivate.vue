<template>
    <div class="tab-pane fade" id="private-pill" role="tabpanel" aria-labelledby="private-pill-tab">
        <div class="mail-body-wrapper">
            <ul>
                <li class="inbox-data">
                    <div class="inbox-user">
                        <div class="form-check form-check-inline m-0">
                            <input class="form-check-input checkbox-primary" id="emailCheckbox1" type="checkbox"
                                value="option1" />
                            <label class="form-check-label" for="emailCheckbox1"></label>
                        </div>
                        <svg class="important-mail" @click="toggleStar()" :class="[{ active: activeStars }]">
                            <use href="@/assets/svg/icon-sprite.svg#fill-star"></use>
                        </svg>
                        <div class="rounded-border">
                            <div>
                                <p class="txt-primary">AD</p>
                            </div>
                        </div>
                        <p>Asther Dolly</p>
                    </div>
                    <div class="inbox-message">
                        <div class="email-data" @click="toogle()"><span>Confirm your booking id -<span>craft beer labore wes
                                    anderson cred
                                    nesciunt sapiente ea proident...</span></span>
                            <div class="badge badge-light-primary">new</div>
                            <div class="badge badge-light-success">Task</div>
                        </div>
                        <div class="email-timing"><span>1:00 PM</span></div>
                        <div class="email-options"><i class="fa fa-envelope-o envelope-1 show"></i><i
                                class="fa fa-envelope-open-o envelope-2 hide"></i><i class="fa fa-trash-o trash-3"></i><i
                                class="fa fa-print"></i></div>
                    </div>
                </li>
            </ul>
        </div>
    </div>
</template>
<script lang="ts" setup>
import { ref, defineEmits, onMounted, watch } from 'vue'
let activeStars = ref<boolean>(false)
let emit = defineEmits(['selected'])
function toggleStar() {
    activeStars.value = !activeStars.value;
}
function toogle() {
    emit('selected');
}
</script>