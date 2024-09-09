<script setup>
import { onMounted, ref, resolveDirective } from 'vue'
import { NInput, NSelect } from 'naive-ui'

import CommonPage from '@/components/page/CommonPage.vue'
import QueryBarItem from '@/components/query-bar/QueryBarItem.vue'
import CrudTable from '@/components/table/CrudTable.vue'

import { useCRUD } from '@/composables'
import api from '@/api'

defineOptions({ name: 'Операционные логи' })

const $table = ref(null)
const queryItems = ref({})

const {
  modalVisible,
  modalTitle,
  modalLoading,
  handleSave,
  modalForm,
  modalFormRef,
  handleEdit,
  handleDelete,
  handleAdd,
} = useCRUD({
  name: 'Операционные логи',
  initForm: {
    args: {
      ping_sleep: 1,
      ping_threshold: 500,
      agent_data_check_threshold: 2,
      agent_incoming_traffic_threshold: 30,
      before_start_clean_sleep: 2,
      before_stop_disposal_sleep: 20,
    },
  },
  doCreate: api.createHostMonitor,
  doUpdate: api.updateHostMonitor,
  doDelete: api.deleteHostMonitor,
  refresh: () => $table.value?.handleSearch(),
})

onMounted(() => {
  $table.value?.handleSearch()
})

function formatTimestamp(timestamp) {
  const date = new Date(timestamp)

  const pad = (num) => num.toString().padStart(2, '0')

  const year = date.getFullYear()
  const month = pad(date.getMonth() + 1) // Месяцы начинаются с 0, поэтому нужно прибавить 1
  const day = pad(date.getDate())
  const hours = pad(date.getHours())
  const minutes = pad(date.getMinutes())
  const seconds = pad(date.getSeconds())

  return `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`
}

// Получить время начала текущего дня в формате метки времени
function getStartOfDayTimestamp() {
  const now = new Date()
  now.setHours(0, 0, 0, 0) // Устанавливаем часы, минуты, секунды и миллисекунды в 0
  return now.getTime()
}

// Получить время конца текущего дня в формате метки времени
function getEndOfDayTimestamp() {
  const now = new Date()
  now.setHours(23, 59, 59, 999) // Устанавливаем часы в 23, минуты в 59, секунды в 59 и миллисекунды в 999
  return now.getTime()
}

// Пример использования
const startOfDayTimestamp = getStartOfDayTimestamp()
const endOfDayTimestamp = getEndOfDayTimestamp()

const datetimeRange = ref([startOfDayTimestamp, endOfDayTimestamp])
const handleDateRangeChange = (value) => {
  queryItems.value.start_time = formatTimestamp(value[0])
  queryItems.value.end_time = formatTimestamp(value[1])
}

const methodOptions = [
  {
    label: 'GET',
    value: 'GET',
  },
  {
    label: 'POST',
    value: 'POST',
  },
  {
    label: 'DELETE',
    value: 'DELETE',
  },
]

const columns = [
  {
    title: 'Имя пользователя',
    key: 'username',
    width: 'auto',
    align: 'center',
    ellipsis: { tooltip: true },
  },
  {
    title: 'Обзор интерфейса',
    key: 'summary',
    align: 'center',
    width: 'auto',
    ellipsis: { tooltip: true },
  },
  {
    title: 'Модуль функциональности',
    key: 'module',
    align: 'center',
    width: 'auto',
    ellipsis: { tooltip: true },
  },
  {
    title: 'Метод запроса',
    key: 'method',
    align: 'center',
    width: 'auto',
    ellipsis: { tooltip: true },
  },
  {
    title: 'Путь запроса',
    key: 'path',
    align: 'center',
    width: 'auto',
    ellipsis: { tooltip: true },
  },
  {
    title: 'Код состояния',
    key: 'status',
    align: 'center',
    width: 'auto',
    ellipsis: { tooltip: true },
  },
  {
    title: 'Время отклика (с)',
    key: 'response_time',
    align: 'center',
    width: 'auto',
    ellipsis: { tooltip: true },
  },
  {
    title: 'Время операции',
    key: 'created_at',
    align: 'center',
    width: 'auto',
    ellipsis: { tooltip: true },
  },
]
</script>

<template>
  <!-- Страница бизнес-логики -->
  <CommonPage>
    <!-- Таблица -->
    <CrudTable
      ref="$table"
      v-model:query-items="queryItems"
      :columns="columns"
      :get-data="api.getAuditLogList"
    >
      <template #queryBar>
        <QueryBarItem label="Имя пользователя" :label-width="70">
          <NInput
            v-model:value="queryItems.username"
            clearable
            type="text"
            placeholder="Введите имя пользователя"
            @keypress.enter="$table?.handleSearch()"
          />
        </QueryBarItem>
        <QueryBarItem label="Модуль функциональности" :label-width="70">
          <NInput
            v-model:value="queryItems.module"
            clearable
            type="text"
            placeholder="Введите модуль функциональности"
            @keypress.enter="$table?.handleSearch()"
          />
        </QueryBarItem>
        <QueryBarItem label="Обзор интерфейса" :label-width="70">
          <NInput
            v-model:value="queryItems.summary"
            clearable
            type="text"
            placeholder="Введите обзор интерфейса"
            @keypress.enter="$table?.handleSearch()"
          />
        </QueryBarItem>
        <QueryBarItem label="Метод запроса" :label-width="70">
          <NSelect
            v-model:value="modalForm.method"
            style="width: 150px"
            :options="methodOptions"
            clearable
            placeholder="Выберите метод запроса"
          />
        </QueryBarItem>
        <QueryBarItem label="API путь" :label-width="70">
          <NInput
            v-model:value="queryItems.path"
            clearable
            type="text"
            placeholder="Введите API путь"
            @keypress.enter="$table?.handleSearch()"
          />
        </QueryBarItem>
        <QueryBarItem label="Дата создания" :label-width="70">
          <NDatePicker
            v-model:value="datetimeRange"
            type="datetimerange"
            clearable
            placeholder="Выберите диапазон времени"
            @update:value="handleDateRangeChange"
          />
        </QueryBarItem>
      </template>
    </CrudTable>
  </CommonPage>
</template>
