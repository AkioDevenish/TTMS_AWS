<template>
    <div :class="colClass">
        <div class="card" :class="cardClass">
            <div :class="smallClass">
                <div class="card-header" :class="cardhaderClass" v-if="headerTitle">
                    <h5 v-if="titles" :class="titleClass">{{ title }}</h5>
                    <h4 v-else :class="titleClass"><i class="icofont icofont-library me-2" v-if="ico"></i>{{ title }}</h4>
                    <vue-feather v-if="icon" :type="type"></vue-feather>
                    <span v-if="text" v-html="props.desc" />
                    <p :class="preClass" v-if="pre" v-html="props.desc"></p>{{ descs }}
                </div>
                <div class="card-header" :class="cardhaderClass" v-if="headerTop">
                    <div class="header-top">
                        <h4>{{ title }}</h4>
                        <div class="card-header-right-icon" v-if="dropdown">
                            <div class="dropdown">
                                <button class="btn dropdown-toggle" id="dropdownMenuButton" type="button"
                                    data-bs-toggle="dropdown">Today</button>
                                <div class="dropdown-menu dropdown-menu-end" aria-labelledby="dropdownMenuButton"><a
                                        class="dropdown-item" href="#">Today</a><a class="dropdown-item"
                                        href="#">Tomorrow</a><a class="dropdown-item" href="#">Yesterday</a></div>
                            </div>
                        </div>
                    </div>
                </div>
                <slot v-if="table" />
                <div class="card-body" v-else :class="cardbodyClass">
                    <slot />
                </div>
                <slot name="light-box" />
                <div class="card-footer " v-if="footer" :class="footerclass">
                    <div class="table-responsive theme-scrollbar" v-if="grid">
                        <table class="w-100">
                            <tbody>
                                <tr>
                                    <th> Class</th>
                                    <th>Value of the class</th>
                                </tr>
                                <tr>
                                    <td><code>{{ content }}</code></td>
                                    <td>{{ startClass }}</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                    <h6 class="mb-0 " :class="footersClass">{{ footertitle }}</h6>
                    <button class="btn  m-r-15" v-if="btnclass" :class="btnclass" type="submit">Submit</button>
                    <button class="btn " v-if="lightclass" :class="lightclass" type="submit">Cancel</button>
                </div>
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
    grid: String,
    headerCard: String,
    chart: String,
    price: String,
    desc: String,
    total: String,
    charts: String,
    headerTop: String,
    smallClass: String,
    pre: String,
    preClass: String,
    titles: String,
    card: String,
    footer: String,
    btnclass: String,
    lightclass: String,
    table: String,
    text: String,
    descs: String,
    content: String,
    startClass: String,
    footerclass: String,
    icon: String,
    type: String,
    ico: String,
    footersClass: String,
    footertitle: String
})
</script>