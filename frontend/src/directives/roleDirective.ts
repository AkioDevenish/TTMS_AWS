import { DirectiveBinding } from 'vue'
import { useAuth } from '@/composables/useAuth'

export const vRole = {
  mounted(el: HTMLElement, binding: DirectiveBinding) {
    const { hasRequiredRole } = useAuth()
    
    if (!hasRequiredRole(binding.value)) {
      el.style.display = 'none'
    }
  },
  updated(el: HTMLElement, binding: DirectiveBinding) {
    const { hasRequiredRole } = useAuth()
    
    if (!hasRequiredRole(binding.value)) {
      el.style.display = 'none'
    } else {
      el.style.display = ''
    }
  }
} 