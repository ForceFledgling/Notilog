<!-- CustomForm.vue -->
<template>
  <n-form ref="formRef" :model="model" :rules="rules" v-bind="attrs">
    <slot />
  </n-form>
</template>

<script setup>
import { ref, onMounted, provide } from 'vue'
import { NForm } from 'naive-ui'

const props = defineProps({
  model: {
    type: Object,
    required: true,
  },
  rules: {
    type: Object,
    default: () => ({}),
  },
  labelMarginRight: {
    type: String,
    default: '10px',
  },
})

const attrs = useAttrs()

const formRef = ref(null)
const labelWidth = ref('auto')
const marginRight = ref('auto')

function calculateLabelStyles() {
  const formElement = formRef.value?.$el
  if (formElement) {
    const labels = formElement.querySelectorAll('.n-form-item-label')
    let maxWidth = 0

    labels.forEach(labelElement => {
      const labelTextWidth = labelElement.querySelector('.n-form-item-label__text').offsetWidth
      // Не учитываем ширину символа required
      if (labelTextWidth > maxWidth) {
        maxWidth = labelTextWidth
      }
    })

    labelWidth.value = `${maxWidth}px`
    marginRight.value = `${parseInt(props.labelMarginRight, 10)}px`
  }
}

onMounted(() => {
  calculateLabelStyles()
})

provide('labelWidth', labelWidth.value)
provide('marginRight', marginRight.value)
</script>
