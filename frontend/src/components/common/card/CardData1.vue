<template>
    <div :class="colClass">
        <div class="card " :class="cardClass">
            <div class="card-header " :class="cardhaderClass" v-if="headerTitle">
                <div class="header-top" :class="titleClass">
                    <h4>{{ title }}</h4>
                    <div class="d-flex align-items-center gap-3" v-if="dropdown">
                        <div class="location-menu dropdown" v-if="location">
                            <button class="btn dropdown-toggle" id="locationdropdown" data-bs-toggle="dropdown"
                                aria-expanded="false">Location</button>
                            <div class="dropdown-menu dropdown-menu-end" aria-labelledby="userdropdown"><a
                                    class="dropdown-item" href="#">Address Selection</a><a class="dropdown-item"
                                    href="#">Geo-Menu</a><a class="dropdown-item" href="#">Place Picker</a></div>
                        </div>
                        <div class="location-menu dropdown" v-if="meet">
                            <button class="btn dropdown-toggle" id="userdropdown9" type="button" data-bs-toggle="dropdown"
                                aria-expanded="false">1pm-2pm</button>
                            <div class="dropdown-menu dropdown-menu-end" aria-labelledby="userdropdown9"><a
                                    class="dropdown-item" href="#">Address Selection</a><a class="dropdown-item"
                                    href="#">Geo-Menu</a><a class="dropdown-item" href="#">Place Picker</a></div>
                        </div>
                        <div class="dropdown icon-dropdown" v-else>
                            <button class="btn dropdown-toggle" id="userdropdown17" type="button" data-bs-toggle="dropdown"
                                aria-expanded="false"><i class="icon-more-alt"></i></button>
                            <div class="dropdown-menu dropdown-menu-end" aria-labelledby="userdropdown17"><a
                                    class="dropdown-item" href="#">Weekly</a><a class="dropdown-item" href="#">Monthly</a><a
                                    class="dropdown-item" href="#">Yearly</a></div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="card-header " v-if="headerCard">
                <div class="header-top">
                    <h5 class="f-w-600 m-0">{{ title }}<span class="f-14 font-primary f-w-500 ms-1">
                            <svg class="svg-fill me-1">
                                <use href="@/assets/svg/icon-sprite.svg#user-visitor"></use>
                            </svg>(+2.8)</span></h5>
                    <div class="card-header-right-icon">
                        <div class="dropdown icon-dropdown">
                            <button class="btn dropdown-toggle" id="visitorButton" type="button" data-bs-toggle="dropdown"
                                aria-expanded="false"><i class="icon-more-alt"></i></button>
                            <div class="dropdown-menu dropdown-menu-end" aria-labelledby="visitorButton"><a
                                    class="dropdown-item" href="#">Today</a><a class="dropdown-item" href="#">Tomorrow</a><a
                                    class="dropdown-item" href="#">Yesterday</a></div>
                        </div>
                    </div>
                </div>
            </div>

            <div class="card-body" :class="cardbodyClass">
                <slot />
            </div>
        </div>
    </div>
</template>
<script lang="ts" setup>
let props = defineProps({
    title: String,
    cardClass: String,
    colClass: String,
    cardbodyClass: String,
    cardhaderClass: String,
    headerTitle: String,
    dropdown: String,
    location: String,
    titleClass: String,
    meet: String,
    headerCard: String
})
</script>