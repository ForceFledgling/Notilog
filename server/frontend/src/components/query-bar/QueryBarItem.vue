<template>
  <div flex items-center>
    <label
      v-if="!isNullOrWhitespace(label)"
      flex-grow
      flex-shrink-0
      :style="{ width: autoWidth ? 'auto' : labelWidth + 'px', 'margin-right': labelMarginRight + 'px' }"
    >
      {{ label }}
    </label>
    <div>
      <slot />
    </div>
  </div>
</template>

<script setup>
import { isNullOrWhitespace } from '@/utils'

defineProps({
  label: {
    type: String,
    default: '',
  },
  autoWidth: {
    type: Boolean,
    default: true,
  },
  labelWidth: {
    type: Number,
    default: 80,
  },
  // Отступ справа от label
  labelMarginRight: {
    type: Number,
    default: 10, // Значение по умолчанию для отступа
  },
  contentWidth: {
    type: Number,
    default: 220,
  },
})
</script>
