<script setup>
/** Пользовательская иконка */
const props = defineProps({
  /** Имя иконки (имя файла в папке assets/svg) */
  icon: {
    type: String,
    required: true,
  },
  size: {
    type: Number,
    default: 14,
  },
  color: {
    type: String,
    default: undefined,
  },
})
</script>

<template>
  <TheIcon type="custom" v-bind="props" />
</template>
