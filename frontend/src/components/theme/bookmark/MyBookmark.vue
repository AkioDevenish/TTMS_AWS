<template>
    <div class="fade tab-pane" id="pills-bookmark" role="tabpanel" aria-labelledby="pills-bookmark-tab">
        <div class="card mb-0">
            <div class="card-header d-flex">
                <h6 class="mb-0">My bookmark</h6>
                <ul>
                    <li><a class="grid-bookmark-view" href="javascript:void(0)"><vue-feather type="grid"
                                @click="liststyle = !liststyle"></vue-feather></a></li>
                    <li><a class="list-layout-view" href="javascript:void(0)"><vue-feather type="list"
                                @click="liststyle = !liststyle"></vue-feather></a></li>
                </ul>
            </div>
            <div class="card-body">
                <div class="details-bookmark text-center" v-bind:class="{ 'list-bookmark': liststyle }">
                    <div class="row" id="bookmarkData1">
                        <div class="col-xxl-3 col-xl-4 col-lg-3 col-md-4 col-sm-6 box-col-4" v-for="(item, index) in data"
                            :key="index">
                            <div class="card card-with-border bookmark-card o-hidden">
                                <div class="details-website"><img class="img-fluid" :src='getImages(item.image)' alt="">
                                    <div class="favourite-icon favourite_0" :class="(getActive(item.id)) ? 'favourite' : ''"
                                        @click="setFavourite(item)"><a href="javascript:void(0)"><i
                                                class="fa fa-star"></i></a></div>
                                    <div class="desciption-data">
                                        <div class="title-bookmark">
                                            <h5 class="title_0">{{ item.title }}</h5>
                                            <p class="weburl_0">{{ item.website_url }}</p>
                                            <div class="hover-block">
                                                <ul>
                                                    <li><a data-bs-toggle="modal"
                                                            data-bs-target="#edit-bookmark"><vue-feather
                                                                type="edit-2"></vue-feather> </a></li>
                                                    <li><a href="#"><vue-feather type="link"></vue-feather></a></li>
                                                    <li><a href="#"><vue-feather type="share-2"></vue-feather></a></li>
                                                    <li><a><vue-feather type="trash-2"
                                                                @click="basic_warning_alert(index)"></vue-feather></a></li>
                                                    <li class="pull-right text-right"><vue-feather type="tag"></vue-feather>
                                                    </li>
                                                </ul>
                                            </div>
                                            <div class="content-general">
                                                <p class="desc_0"> {{ item.desc }}</p><span
                                                    class="collection_0">General</span>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
<script lang="ts" setup>
import { getImages } from "@/composables/common/getImages"
import { useBookmarkStore } from "@/store/bookmark"
import { ref } from 'vue'
import Swal from 'sweetalert2'
let liststyle = ref<boolean>(false)
let store = useBookmarkStore()
let favourite = store.favourite
let data = store.item
function basic_warning_alert(index: number) {
    Swal.fire({
        icon: 'warning',
        title: "Are you sure?", text: 'This bookmark will be deleted from your bookmark ', showCancelButton: true,
        cancelButtonText: 'Cancel', confirmButtonText: 'Ok', confirmButtonColor: 'var(--theme-deafult)',
    }).then((result) => {
        if (result.value) {
            data.splice(index, 1)
            Swal.fire({
                icon: 'success', text: 'Poof! Your imaginary file has been deleted!', confirmButtonColor: 'var(--theme-deafult)',
            });
        } else {
            Swal.fire({
                text: 'Your contact is safe!', confirmButtonColor: 'var(--theme-deafult)',
            });
        }
    });
}

function getActive(itemId: number) {
    const objIndex = favourite.findIndex(((obj) => obj.id === itemId));
    if (objIndex > -1) {
        return true;
    } else {
        return false;
    }
}
function setFavourite(item: number) {
    const objIndex = favourite.findIndex(((obj) => obj.id === item.id));
    if (objIndex > -1) {
        favourite.splice(objIndex, 1);
    } else {
        favourite.push(item);
    }
}
</script>