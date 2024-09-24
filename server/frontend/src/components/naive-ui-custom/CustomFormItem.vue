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
const labelWidth = inject('labelWidth', ref('auto'))  // Ожидаем ref для динамического обновления
const baseMarginRight = inject('marginRight', ref('10px'))  // Ожидаем ref для динамического обновления

// Проверяем, является ли поле обязательным
const required = computed(() => props.rule.required)

// Устанавливаем отступы для обязательных и необязательных полей
const computedLabelStyle = computed(() => ({
  width: labelWidth.value,
  marginRight: required.value ? `calc(${baseMarginRight.value} - 4px)` : `calc(${baseMarginRight.value} + 4px)`, // Корректируем отступ для полей с и без символа "*"
}))
</script>

<style scoped>
.form-item-label {
  display: flex;
  align-items: center;
}

.required-asterisk {
  color: red;
  margin-left: 4px;
}

.not-required-asterisk {
  margin-right: 8px;
}
</style>
