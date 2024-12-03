<template>
    <table class="table-wrapper table-responsive theme-scrollbar">
        <tbody>
            <tr>
                <td>
                    <table class="table-responsive" style="width: 100%;">
                        <tbody>
                            <tr
                                style="padding: 28px 0 5px; display: flex; justify-content: space-between; align-items: center;">
                                <td><img class="img-fluid for-light" src="@/assets/images/logo/logo.png" alt=""><img
                                        class="img-fluid for-dark" src="@/assets/images/logo/logo_light.png" alt=""></td>
                                <td>
                                    <ul
                                        style="list-style: none; display: flex; background: linear-gradient(291deg, #7A70BA 21.2%, #7A70BA 83.92%); padding: 31px 80px; border-bottom-left-radius: 100px; gap:28px;">
                                        <li>
                                            <svg class="stroke-icon"
                                                style="height:14px; width: 14px; fill:#fff; margin-right: 10px;">
                                                <use href="@/assets/svg/icon-sprite.svg#call"></use>
                                            </svg><span style="color: #FFFFFF;">(239) 555-0108</span>
                                        </li>
                                        <li
                                            style="border-left: 1px dashed rgba(255, 255, 255, 0.3); border-right: 1px dashed rgba(255, 255, 255, 0.3); padding: 0 22px;">
                                            <svg class="stroke-icon"
                                                style="height:16px; width: 16px; fill:#fff; margin-right: 10px;">
                                                <use href="@/assets/svg/icon-sprite.svg#email-box"></use>
                                            </svg><span style="color: #FFFFFF;">Mofi@themesforest.com</span>
                                        </li>
                                        <li>
                                            <svg class="stroke-icon"
                                                style="height:16px; width: 16px; fill:#fff; margin-right: 10px;">
                                                <use href="@/assets/svg/icon-sprite.svg#web"></use>
                                            </svg><span style="color: #FFFFFF;">Website: www.Mofithemes.com</span>
                                        </li>
                                    </ul>
                                </td>
                            </tr>
                            <tr style="display: flex; justify-content: space-between;">
                                <td> <span :style="item.style" v-for="(item, index) in data1" :key="index">{{ item.title
                                }}</span></td>
                                <td>
                                    <h4 style="font-size:42px; font-weight: 600;color: #7A70BA; margin:0 0 12px 0;">INVOICE
                                    </h4><span :style="item.style" v-for="(item, index) in data2" :key="index">
                                        {{ item.title }}</span>
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </td>
            </tr>
            <tr>
                <td>
                    <table class="table-responsive" style="width: 100%; border-spacing: 4px; margin-bottom: 20px;">
                        <tbody>
                            <tr>
                                <td style="background: rgba(122, 112, 186 , 0.1);padding: 15px 25px;"
                                    v-for="(items, index) in tables" :key="index">
                                    <p
                                        style="font-size:16px; font-weight:500; color:#7A70BA; opacity:0.8; margin:0;line-height: 2;">
                                        {{ items.title }}</p><span style="font-size: 16px; font-weight: 600;">{{ items.desc
                                        }}</span>
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </td>
            </tr>
            <tr>
                <td>
                    <table class="table-responsive" style="width: 100%; border-spacing:0;">
                        <thead>
                            <tr style="background: #7A70BA;">
                                <th :style="item.style" v-for="(item, index) in tableheader" :key="index">
                                    <span style="color: #fff; font-size: 16px; font-weight: 600;">{{ item.title }}</span>
                                </th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="(item, index) in tablesection" :key="index">
                                <td :style="item.style">
                                    <span :style="item.nostyle">{{ item.no }}</span>
                                </td>
                                <td :style="item.titleclass">
                                    <h4 :style="item.titlestyle">{{ item.title }}</h4><span
                                        :style="item.substyle">{{ item.subtitle }}</span>
                                </td>
                                <td :style="item.pricestyle">
                                    <span :style="item.priceclass">{{ item.price }}</span>
                                </td>
                                <td :style="item.qtystyle">
                                    <span :style="item.priceclass">{{ item.qty }}</span>
                                </td>
                                <td :style="item.totalstyle">
                                    <span :style="item.totalclass">{{ item.total }}</span>
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </td>
            </tr>
            <tr style="width: 100%; display: flex; justify-content: space-between; margin-top: 36px;">
                <td> <img src="@/assets/images/email-template/invoice-3/sign.png" alt="sign"><span
                        style="color: #7A70BA;display: block;font-size: 16px;font-weight: 600;">Laurine T.
                        Ebbert</span><span style=" display: block; font-size: 14px; padding-top: 5px;">( Designer )</span>
                </td>
                <td> <span style="display: flex; justify-content: end; gap: 15px;"><a
                            style="background: rgba(122, 112, 186, 1); color:rgba(255, 255, 255, 1);border-radius: 10px;padding: 18px 27px;font-size: 16px;font-weight: 600;outline: 0;border: 0; text-decoration: none;"
                            href="#!" onclick="window.print();">Print Invoice<i class="icon-arrow-right"
                                style="font-size:13px;font-weight:bold; margin-left: 10px;"></i></a><a
                            style="background: rgba(122, 112, 186, 0.1);color: rgba(122, 112, 186, 1);border-radius: 10px;padding: 18px 27px;font-size: 16px;font-weight: 600;outline: 0;border: 0; text-decoration: none;"
                            href="" download="">Download<i class="icon-arrow-right"
                                style="font-size:13px;font-weight:bold; margin-left: 10px;"></i></a></span></td>
            </tr>
        </tbody>
    </table>
</template>
<script lang="ts" setup>
import { data1, data2, tables, tableheader, tablesection } from "@/core/data/ecommerce"
</script>