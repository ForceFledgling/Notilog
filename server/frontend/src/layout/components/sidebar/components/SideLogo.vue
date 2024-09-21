<template>
  <router-link h-60 f-c-c to="/">
    <icon-custom-logo
      :class="{ 'invert-logo': isDark }"
      text-36
      color-primary
    ></icon-custom-logo>
    <h2
      v-show="!appStore.collapsed"
      ml-2
      mr-8
      max-w-150
      flex-shrink-0
      text-16
      font-bold
    >
      {{ title }}
    </h2>
  </router-link>
</template>

<script setup>
import { useAppStore } from '@/store'
import { useDark } from '@vueuse/core'

const title = import.meta.env.VITE_TITLE
const appStore = useAppStore()

// Получаем текущее состояние темы (тёмная или светлая)
const isDark = useDark()
</script>

<style scoped>
/* Стили инверсии для логотипа */
.invert-logo {
  filter: invert(100%);
  color: white;
}
</style>
