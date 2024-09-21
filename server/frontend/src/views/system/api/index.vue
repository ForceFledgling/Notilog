<script setup>
import { h, onMounted, ref, resolveDirective, withDirectives } from 'vue'
import { NButton, NForm, NFormItem, NInput, NPopconfirm } from 'naive-ui'
import CustomForm from '@/components/naive-ui-custom/CustomForm.vue'

import CommonPage from '@/components/page/CommonPage.vue'
import QueryBarItem from '@/components/query-bar/QueryBarItem.vue'
import CrudModal from '@/components/table/CrudModal.vue'
import CrudTable from '@/components/table/CrudTable.vue'
import TheIcon from '@/components/icon/TheIcon.vue'

import { renderIcon } from '@/utils'
import { useCRUD } from '@/composables'
import api from '@/api'

defineOptions({ name: 'Управление API' })

const $table = ref(null)
const queryItems = ref({})
const vPermission = resolveDirective('permission')

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
  name: 'API',
  initForm: {},
  doCreate: api.createApi,
  doUpdate: api.updateApi,
  doDelete: api.deleteApi,
  refresh: () => $table.value?.handleSearch(),
})

onMounted(() => {
  $table.value?.handleSearch()
})

async function handleRefreshApi() {
  await $dialog.confirm({
    title: 'Подтверждение',
    type: 'warning',
    content: 'Эта операция обновит маршруты на основе backend app.routes. Вы уверены, что хотите продолжить обновление API?',
    async confirm() {
      await api.refreshApi()
      $message.success('Обновление завершено')
      $table.value?.handleSearch()
    },
  })
}

const addAPIRules = {
  path: [
    {
      required: true,
      message: 'Пожалуйста, введите путь API',
      trigger: ['input', 'blur', 'change'],
    },
  ],
  method: [
    {
      required: true,
      message: 'Пожалуйста, введите метод запроса',
      trigger: ['input', 'blur', 'change'],
    },
  ],
  summary: [
    {
      required: true,
      message: 'Пожалуйста, введите описание API',
      trigger: ['input', 'blur', 'change'],
    },
  ],
  tags: [
    {
      required: true,
      message: 'Пожалуйста, введите теги',
      trigger: ['input', 'blur', 'change'],
    },
  ],
}

const columns = [
  {
    title: 'Путь API',
    key: 'path',
    width: 'auto',
    align: 'center',
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
    title: 'Описание API',
    key: 'summary',
    width: 'auto',
    align: 'center',
    ellipsis: { tooltip: true },
  },
  {
    title: 'Теги',
    key: 'tags',
    width: 'auto',
    align: 'center',
    ellipsis: { tooltip: true },
  },
  {
    title: 'Действия',
    key: 'actions',
    width: 'auto',
    align: 'center',
    fixed: 'right',
    render(row) {
      return [
        withDirectives(
          h(
            NButton,
            {
              size: 'small',
              type: 'primary',
              style: 'margin-right: 8px;',
              onClick: () => {
                handleEdit(row)
                modalForm.value.roles = row.roles.map((e) => (e = e.id))
              },
            },
            {
              default: () => 'Редактировать',
              icon: renderIcon('material-symbols:edit', { size: 16 }),
            }
          ),
          [[vPermission, 'post/api/v1/api/update']]
        ),
        h(
          NPopconfirm,
          {
            onPositiveClick: () => handleDelete({ api_id: row.id }, false),
            onNegativeClick: () => {},
          },
          {
            trigger: () =>
              withDirectives(
                h(
                  NButton,
                  {
                    size: 'small',
                    type: 'error',
                  },
                  {
                    default: () => 'Удалить',
                    icon: renderIcon('material-symbols:delete-outline', { size: 16 }),
                  }
                ),
                [[vPermission, 'delete/api/v1/api/delete']]
              ),
            default: () => h('div', {}, 'Вы уверены, что хотите удалить этот API?'),
          }
        ),
      ]
    },
  },
]
</script>

<template>
  <!-- Страница бизнес-логики -->
  <CommonPage show-footer title="Список API">
    <template #action>
      <div>
        <NButton
          v-permission="'post/api/v1/api/create'"
          class="float-right mr-15"
          type="primary"
          @click="handleAdd"
        >
          <TheIcon icon="material-symbols:add" :size="18" class="mr-5" />Создать API
        </NButton>
        <NButton
          v-permission="'post/api/v1/api/refresh'"
          class="float-right mr-15"
          type="warning"
          @click="handleRefreshApi"
        >
          <TheIcon icon="material-symbols:refresh" :size="18" class="mr-5" />Обновить API
        </NButton>
      </div>
    </template>
    <!-- Таблица -->
    <CrudTable
      ref="$table"
      v-model:query-items="queryItems"
      :columns="columns"
      :get-data="api.getApis"
    >
      <template #queryBar>
        <QueryBarItem label="Путь" :label-width="40">
          <NInput
            v-model:value="queryItems.path"
            clearable
            type="text"
            placeholder="Введите путь API"
            @keypress.enter="$table?.handleSearch()"
          />
        </QueryBarItem>
        <QueryBarItem label="Описание API" :label-width="70">
          <NInput
            v-model:value="queryItems.summary"
            clearable
            type="text"
            placeholder="Введите описание API"
            @keypress.enter="$table?.handleSearch()"
          />
        </QueryBarItem>
        <QueryBarItem label="Теги" :label-width="40">
          <NInput
            v-model:value="queryItems.tags"
            clearable
            type="text"
            placeholder="Введите теги"
            @keypress.enter="$table?.handleSearch()"
          />
        </QueryBarItem>
      </template>
    </CrudTable>

    <!-- Модальное окно для добавления/редактирования -->
    <CrudModal
      v-model:visible="modalVisible"
      :title="modalTitle"
      :loading="modalLoading"
      @save="handleSave"
    >
      <NForm
        ref="modalFormRef"
        label-placement="left"
        label-align="left"
        :label-width="80"
        :model="modalForm"
        :rules="addAPIRules"
      >
        <NFormItem label="Название API" path="path">
          <NInput v-model:value="modalForm.path" clearable placeholder="Введите путь API" />
        </NFormItem>
        <NFormItem label="Метод запроса" path="method">
          <NInput v-model:value="modalForm.method" clearable placeholder="Введите метод запроса" />
        </NFormItem>
        <NFormItem label="Описание API" path="summary">
          <NInput v-model:value="modalForm.summary" clearable placeholder="Введите описание API" />
        </NFormItem>
        <NFormItem label="Теги" path="tags">
          <NInput v-model:value="modalForm.tags" clearable placeholder="Введите теги" />
        </NFormItem>
      </NForm>
    </CrudModal>
  </CommonPage>
</template>
