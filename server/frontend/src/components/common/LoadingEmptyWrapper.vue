<template>
  <div v-if="reloadFlag" class="relative">
    <slot></slot>
    <div v-show="showPlaceholder" class="absolute-lt h-full w-full" :class="placeholderClass">
      <div v-show="loading" class="absolute-center">
        <n-spin :show="true" :size="loadingSize" />
      </div>
      <div v-show="isEmpty" class="absolute-center">
        <div class="relative">
          <icon-custom-no-data :class="iconClass" />
          <p class="absolute-lb w-full text-center" :class="descClass">{{ emptyDesc }}</p>
        </div>
      </div>
      <div v-show="!network" class="absolute-center">
        <div
          class="relative"
          :class="{ 'cursor-pointer': showNetworkReload }"
          @click="handleReload"
        >
          <icon-custom-network-error :class="iconClass" />
          <p class="absolute-lb w-full text-center" :class="descClass">{{ networkErrorDesc }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, nextTick, watch, onUnmounted } from 'vue'

defineOptions({ name: 'LoadingEmptyWrapper' })

const NETWORK_ERROR_MSG = 'Похоже, что сеть немного подвела~'

const props = {
  loading: false,
  empty: false,
  loadingSize: 'medium',
  placeholderClass: 'bg-white dark:bg-dark transition-background-color duration-300 ease-in-out',
  emptyDesc: 'Нет данных',
  iconClass: 'text-320px text-primary',
  descClass: 'text-16px text-#666',
  showNetworkReload: false,
}

// Состояние сети
const network = ref(window.navigator.onLine)
const reloadFlag = ref(true)

// Данные пусты
const isEmpty = computed(() => props.empty && !props.loading && network.value)

const showPlaceholder = computed(() => props.loading || isEmpty.value || !network.value)

const networkErrorDesc = computed(() =>
  props.showNetworkReload ? `${NETWORK_ERROR_MSG}, Нажмите для повторной попытки` : NETWORK_ERROR_MSG,
)

function handleReload() {
  if (!props.showNetworkReload) return
  reloadFlag.value = false
  nextTick(() => {
    reloadFlag.value = true
  })
}

const stopHandle = watch(
  () => props.loading,
  (newValue) => {
    // По завершению загрузки проверить состояние сети
    if (!newValue) {
      network.value = window.navigator.onLine
    }
  },
)

onUnmounted(() => {
  stopHandle()
})
</script>

<style scoped></style>
