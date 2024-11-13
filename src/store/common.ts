import { defineStore } from 'pinia'
import { ref } from 'vue'
import { computed } from 'vue'
import { simple, flush, multiples, multipledata, iconaccodion, collapse } from "@/core/data/uikits"
import { quik, intell, selling, users } from "@/core/data/faq"
import { news, cancals, shippeds } from "@/core/data/ecommerce"
import { featured } from "@/core/data/dashboards"
import { sent, inbox, starred, draft, trash, work, support } from "@/core/data/letter-box"
export const useCommonStore = defineStore('Common', () => {

    let data = ref(simple)
    let flushes = ref(flush)
    let multiple = ref(multiples)
    let multi = ref(multipledata)
    let icons = ref(iconaccodion)
    let quiks = ref(quik)
    let int = ref(intell)
    let sell = ref(selling)
    let user = ref(users)
    let newitem = ref(news)
    let cancal = ref(cancals)
    let shipped = ref(shippeds)
    let featureds = ref(featured)
    let sents = ref(sent)
    let inboxs = ref(inbox)
    let starr = ref(starred)
    let items = ref(draft)
    let deletes = ref(trash)
    let works = ref(work)
    let supported = ref(support)

    return {
        data,
        flushes,
        multiple,
        multi,
        icons,
        quiks,
        int,
        sell,
        user,
        newitem,
        cancal,
        shipped,
        featureds,
        sents,
        inboxs,
        starr,
        items,
        deletes,
        works,
        supported,
    }
})
