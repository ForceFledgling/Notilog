<script setup>
import { ref, onMounted, h } from 'vue'
import { NButton, NForm, NFormItem, NInput, NTabPane, NTabs, NDataTable, NPagination } from 'naive-ui'
import { useI18n } from 'vue-i18n'
import CommonPage from '@/components/page/CommonPage.vue'
import { useEventStore } from '@/store'
import api from '@/api'

const { t } = useI18n()
const eventStore = useEventStore()
const isLoading = ref(false)
const events = ref([])
const totalEvents = ref(0)
const page = ref(1)
const pageSize = ref(10)

async function loadEvents() {
  console.log("Loading events...")
  isLoading.value = true
  try {
    const response = await api.getEventList({ page: page.value, pageSize: pageSize.value })
    console.log("API Response:", response) // Посмотреть ответ от API
    events.value = response.data // Изменено на response.data
    totalEvents.value = response.total // Изменено на response.total
  } catch (error) {
    console.error(error)
  } finally {
    isLoading.value = false
  }
}


// Загрузка данных при монтировании компонента
onMounted(() => {
  loadEvents()
})

// Удаление события
async function deleteEvent(eventId) {
  isLoading.value = true
  try {
    await api.deleteEvent({ id: eventId })
    loadEvents()
    // Здесь предполагается, что у вас есть доступ к $message
    $message.success(t('common.text.delete_success'))
  } catch (error) {
    console.error(error)
  } finally {
    isLoading.value = false
  }
}

const columns = [
  {
    title: t('views.events.label_event_message'),
    key: 'message', // Используйте правильный ключ, чтобы отобразить данные события
  },
  {
    title: t('views.events.label_event_date'),
    key: 'created_at', // Используйте правильный ключ для даты
  },
  {
    title: t('views.events.label_actions'),
    key: 'actions',
    render(row) {
      return h(
        NButton,
        {
          type: 'error',
          onClick: () => deleteEvent(row.id),
        },
        { default: () => t('common.buttons.delete') }
      )
    },
  },
]


</script>

<template>
  <CommonPage :show-header="false">
    <NTabs type="line" animated>
      <NTabPane name="events-list" :tab="$t('views.events.label_events_list')">
        <div class="m-30">
          <NDataTable
            :loading="isLoading"
            :columns="columns"
            :data="events"
            :pagination="false"
            class="mb-20"
          />
          <NPagination
            v-model:page="page"
            v-model:page-size="pageSize"
            :page-count="Math.ceil(totalEvents / pageSize)"
            show-size-picker
            :page-sizes="[10, 50, 100]"
            @update:page="loadEvents"
            @update:page-size="loadEvents"
          />
        </div>
      </NTabPane>
      <NTabPane name="create-event" :tab="$t('views.events.label_create_event')">
        <div class="m-30 flex items-center">
          <NForm
            label-placement="left"
            label-align="left"
            label-width="100"
            class="w-400"
          >
            <NFormItem :label="$t('views.events.label_event_message')" path="event_name">
              <NInput type="text" :placeholder="$t('views.events.placeholder_event_name')" />
            </NFormItem>
            <NFormItem :label="$t('views.events.label_event_date')" path="event_date">
              <NInput
                type="date"
                placeholder=""
              />
            </NFormItem>
            <NButton type="primary">
              {{ $t('common.buttons.create') }}
            </NButton>
          </NForm>
        </div>
      </NTabPane>
    </NTabs>
  </CommonPage>
</template>

<style scoped>
.m-30 {
  margin: 30px;
}
.w-400 {
  width: 400px;
}
.w-500 {
  width: 500px;
}
.mb-20 {
  margin-bottom: 20px;
}
</style>
