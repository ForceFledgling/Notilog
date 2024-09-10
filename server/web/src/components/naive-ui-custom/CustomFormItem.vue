<!-- CustomFormItem.vue -->
<template>
  <n-form-item
    v-bind="attrs"
    :label-style="computedLabelStyle"
    :label-props="labelProps"
  >
    <template #label>
      <span :class="['form-item-label', { 'not-required-asterisk': !required }]">
        {{ props.label }}
        <span v-if="required" class="required-asterisk">*</span>
      </span>
    </template>
    <slot />
  </n-form-item>
</template>

<script setup>
import { computed, inject, defineProps, useAttrs } from 'vue'

const props = defineProps({
  rule: {
    type: Object,
    default: () => ({}),
  },
  label: {
    type: String,
    default: '',
  },
})

const attrs = useAttrs()

// Получаем вычисленную ширину и отступ из `CustomForm`
const labelWidth = inject('labelWidth', 'auto')
const baseMarginRight = inject('marginRight', '10px')

// Проверяем, является ли поле обязательным
const required = computed(() => props.rule.required)

// Устанавливаем отступы для обязательных и необязательных полей
const computedLabelStyle = computed(() => ({
  width: labelWidth,
  marginRight: required.value ? `calc(${baseMarginRight} - 4px)` : `calc(${baseMarginRight} + 4px)`, // Корректируем отступ для полей с и без символа "*"
}))
</script>

<style scoped>
.form-item-label {
  display: flex;
  align-items: center;
}

.required-asterisk {
  color: red; /* Цвет звездочки, можно изменить по необходимости */
  margin-left: 4px; /* Отступ между меткой и звездочкой */
}

.not-required-asterisk {
  margin-right: 8px; /* Отступ для меток без символа "*" на 4 пикселя больше */
}
</style>
