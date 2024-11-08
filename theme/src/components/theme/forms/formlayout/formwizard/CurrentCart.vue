<template>
    <div class="col-xl-4">
        <div class="shipping-info">
            <h5>Current Cart </h5>
            <div class="overflow-auto theme-scrollbar">
                <table class="table table-striped">
                    <thead>
                        <tr>
                            <th scope="col">Product</th>
                            <th scope="col">Product Detail </th>
                            <th scope="col">Price </th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="(item, index) in currentcart" :key="index">
                            <td> <img :src="getImages(item.img)" alt="t-shirt"></td>
                            <td>
                                <div>
                                    <h6>{{ item.title }}</h6><span>{{ item.multipl }}</span>
                                </div>
                            </td>
                            <td>
                                <p>{{ item.price }}</p>
                            </td>
                        </tr>
                    </tbody>
                    <tfoot>
                        <tr>
                            <td>Sub Total :</td>
                            <td colspan="2">$1284.00 </td>
                        </tr>
                        <tr>
                            <td>Discount :</td>
                            <td colspan="2">$20.00</td>
                        </tr>
                        <tr>
                            <td>Shipping Charge :</td>
                            <td colspan="2">$100.78</td>
                        </tr>
                        <tr>
                            <td>Tax :</td>
                            <td colspan="2">$205.34</td>
                        </tr>
                        <tr>
                            <td>Total (USD) :</td>
                            <td colspan="2">$1569.7</td>
                        </tr>
                    </tfoot>
                </table>
            </div>
        </div>
    </div>
</template>
<script lang="ts" setup>
import { currentcart } from "@/core/data/forms"
import { getImages } from "@/composables/common/getImages"
</script>