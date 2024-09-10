<template>
  <n-modal
    v-model:show="show"
    :style="{ width }"
    preset="card"
    :title="title"
    size="huge"
    :bordered="false"
    :mask-closable="false"
  >
    <div style="padding: 20px; max-height: 80vh; overflow-y: auto;">
      <slot />
    </div>
    <template v-if="showFooter" #footer>
      <footer flex justify-end style="padding: 15px 20px;">
        <slot name="footer">
          <n-button @click="show = false">Отмена</n-button>
          <n-button :loading="loading" ml-20 type="primary" @click="emit('save')">Сохранить</n-button>
        </slot>
      </footer>
    </template>
  </n-modal>
</template>

<script setup>
const props = defineProps({
  width: {
    type: String,
    default: '800px', // Увеличена ширина до 800px
  },
  title: {
    type: String,
    default: '',
  },
  showFooter: {
    type: Boolean,
    default: true,
  },
  visible: {
    type: Boolean,
    required: true,
  },
  loading: {
    type: Boolean,
    default: false,
  },
})

const emit = defineEmits(['update:visible', 'onSave'])
const show = computed({
  get() {
    return props.visible
  },
  set(v) {
    emit('update:visible', v)
  },
})
</script>
