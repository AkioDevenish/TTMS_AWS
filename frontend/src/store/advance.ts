import { defineStore } from 'pinia'
import { ref } from 'vue'
import { animationrating } from "@/core/data/advance"
export const useAdvanceStore = defineStore('advance', () => {

    let data = ref(animationrating)
    return {
        data
    }
})
