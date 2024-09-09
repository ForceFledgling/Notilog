<script setup>
import { h, onMounted, ref, resolveDirective, withDirectives } from 'vue'
import {
  NButton,
  NForm,
  NFormItem,
  NInput,
  NInputNumber,
  NPopconfirm,
  NSwitch,
  NTreeSelect,
} from 'naive-ui'

import CommonPage from '@/components/page/CommonPage.vue'
import CrudModal from '@/components/table/CrudModal.vue'
import CrudTable from '@/components/table/CrudTable.vue'
import IconPicker from '@/components/icon/IconPicker.vue'
import TheIcon from '@/components/icon/TheIcon.vue'

import { formatDate, renderIcon } from '@/utils'
import { useCRUD } from '@/composables'
import api from '@/api'

defineOptions({ name: 'Управление меню' })

const $table = ref(null)
const queryItems = ref({})
const vPermission = resolveDirective('permission')
const menuDisabled = ref(false)

// Инициализация содержимого формы
const initForm = {
  order: 1,
  keepalive: true,
}

const {
  modalVisible,
  modalTitle,
  modalLoading,
  handleAdd,
  handleDelete,
  handleEdit,
  handleSave,
  modalForm,
  modalFormRef,
} = useCRUD({
  name: 'Меню',
  initForm,
  doCreate: api.createMenu,
  doDelete: api.deleteMenu,
  doUpdate: api.updateMenu,
  refresh: () => $table.value?.handleSearch(),
})

onMounted(() => {
  $table.value?.handleSearch()
  getTreeSelect()
})

// Показать "Тип меню"
const showMenuType = ref(false)
const menuOptions = ref([])

const columns = [
  { title: 'ID', key: 'id', width: 50, ellipsis: { tooltip: true } },
  { title: 'Название меню', key: 'name', width: 80, ellipsis: { tooltip: true } },
  {
    title: 'Иконка',
    key: 'icon',
    width: 30,
    render(row) {
      return h(TheIcon, { icon: row.icon, size: 20 })
    },
  },
  { title: 'Сортировка', key: 'order', width: 30, ellipsis: { tooltip: true } },
  { title: 'Путь доступа', key: 'path', width: 60, ellipsis: { tooltip: true } },
  { title: 'Путь перенаправления', key: 'redirect', width: 60, ellipsis: { tooltip: true } },
  { title: 'Путь компонента', key: 'component', width: 60, ellipsis: { tooltip: true } },
  {
    title: 'KeepAlive',
    key: 'keepalive',
    width: 40,
    render(row) {
      return h(NSwitch, {
        size: 'small',
        rubberBand: false,
        value: row.keepalive,
        onUpdateValue: () => handleUpdateKeepalive(row),
      })
    },
  },
  {
    title: 'Скрыть',
    key: 'is_hidden',
    width: 40,
    render(row) {
      return h(NSwitch, {
        size: 'small',
        rubberBand: false,
        value: row.is_hidden,
        onUpdateValue: () => handleUpdateHidden(row),
      })
    },
  },
  {
    title: 'Дата создания',
    key: 'created_at',
    width: 70,
    render(row) {
      return h('span', formatDate(row.created_at))
    },
  },
  {
    title: 'Операции',
    key: 'actions',
    width: 80,
    align: 'center',
    fixed: 'right',
    render(row) {
      return [
        withDirectives(
          h(
            NButton,
            {
              size: 'tiny',
              quaternary: true,
              type: 'primary',
              style: `display: ${row.children ? '' : 'none'};`,
              onClick: () => {
                initForm.parent_id = row.id
                initForm.menu_type = 'menu'
                showMenuType.value = false
                menuDisabled.value = false
                handleAdd()
              },
            },
            { default: () => 'Подменю', icon: renderIcon('material-symbols:add', { size: 16 }) }
          ),
          [[vPermission, 'post/api/v1/menu/create']]
        ),
        withDirectives(
          h(
            NButton,
            {
              size: 'tiny',
              quaternary: true,
              type: 'info',
              onClick: () => {
                showMenuType.value = false
                handleEdit(row)
              },
            },
            {
              default: () => 'Редактировать',
              icon: renderIcon('material-symbols:edit-outline', { size: 16 }),
            }
          ),
          [[vPermission, 'post/api/v1/menu/update']]
        ),
        h(
          NPopconfirm,
          {
            onPositiveClick: () => handleDelete({ id: row.id }, false),
          },
          {
            trigger: () =>
              withDirectives(
                h(
                  NButton,
                  {
                    size: 'tiny',
                    quaternary: true,
                    type: 'error',
                    style: `display: ${row.children && row.children.length > 0 ? 'none' : ''};`, // Не разрешать удаление с подменю
                  },
                  {
                    default: () => 'Удалить',
                    icon: renderIcon('material-symbols:delete-outline', { size: 16 }),
                  }
                ),
                [[vPermission, 'delete/api/v1/menu/delete']]
              ),
            default: () => h('div', {}, 'Вы уверены, что хотите удалить это меню?'),
          }
        ),
      ]
    },
  },
]
// Изменить состояние keepalive
async function handleUpdateKeepalive(row) {
  if (!row.id) return
  row.publishing = true
  row.keepalive = row.keepalive === false ? true : false
  await api.updateMenu(row)
  row.publishing = false
  $message?.success(row.keepalive ? 'Включено' : 'Отключено')
}

// Изменить состояние скрытия
async function handleUpdateHidden(row) {
  if (!row.id) return
  row.publishing = true
  row.is_hidden = row.is_hidden === false ? true : false
  await api.updateMenu(row)
  row.publishing = false
  $message?.success(row.is_hidden ? 'Скрыто' : 'Отменено скрытие')
}

// Добавить меню (опционально каталог)
function handleClickAdd() {
  initForm.parent_id = 0
  initForm.menu_type = 'catalog'
  initForm.is_hidden = false
  initForm.order = 1
  initForm.keepalive = true
  showMenuType.value = true
  menuDisabled.value = true
  handleAdd()
}

async function getTreeSelect() {
  const { data } = await api.getMenus()
  const menu = { id: 0, name: 'Корневой каталог', children: [] }
  menu.children = data
  menuOptions.value = [menu]
}
</script>

<template>
  <!-- Страница бизнес-логики -->
  <CommonPage show-footer title="Список меню">
    <template #action>
      <NButton v-permission="'post/api/v1/menu/create'" type="primary" @click="handleClickAdd">
        <TheIcon icon="material-symbols:add" :size="18" class="mr-5" />Создать корневое меню
      </NButton>
    </template>

    <!-- Таблица -->
    <CrudTable
      ref="$table"
      v-model:query-items="queryItems"
      :is-pagination="false"
      :columns="columns"
      :get-data="api.getMenus"
      :single-line="true"
    >
    </CrudTable>

    <!-- Модальное окно для добавления/редактирования/просмотра -->
    <CrudModal
      v-model:visible="modalVisible"
      :title="modalTitle"
      :loading="modalLoading"
      @save="handleSave(getTreeSelect)"
    >
      <!-- Форма -->
      <NForm
        ref="modalFormRef"
        label-placement="left"
        label-align="left"
        :label-width="80"
        :model="modalForm"
      >
        <NFormItem label="Родительское меню" path="parent_id">
          <NTreeSelect
            v-model:value="modalForm.parent_id"
            key-field="id"
            label-field="name"
            :options="menuOptions"
            default-expand-all="true"
            :disabled="menuDisabled"
          />
        </NFormItem>
        <NFormItem
          label="Название меню"
          path="name"
          :rule="{
            required: true,
            message: 'Введите уникальное название меню',
            trigger: ['input', 'blur'],
          }"
        >
          <NInput v-model:value="modalForm.name" placeholder="Введите уникальное название меню" />
        </NFormItem>
        <NFormItem
          label="Путь доступа"
          path="path"
          :rule="{
            required: true,
            message: 'Введите путь доступа',
            trigger: ['blur'],
          }"
        >
          <NInput v-model:value="modalForm.path" placeholder="Введите путь доступа" />
        </NFormItem>
        <NFormItem v-if="modalForm.menu_type === 'menu'" label="Путь компонента" path="component">
          <NInput
            v-model:value="modalForm.component"
            placeholder="Введите путь компонента, например: /system/user"
          />
        </NFormItem>
        <NFormItem label="Путь перенаправления" path="redirect">
          <NInput
            v-model:value="modalForm.redirect"
            :disabled="modalForm.parent_id !== 0"
            :placeholder="
              modalForm.parent_id !== 0 ? 'Только для корневого меню можно установить путь перенаправления' : 'Введите путь перенаправления'
            "
          />
        </NFormItem>
        <NFormItem label="Иконка меню" path="icon">
          <IconPicker v-model:value="modalForm.icon" />
        </NFormItem>
        <NFormItem label="Порядок отображения" path="order">
          <NInputNumber v-model:value="modalForm.order" :min="1" />
        </NFormItem>
        <NFormItem label="Скрыто" path="is_hidden">
          <NSwitch v-model:value="modalForm.is_hidden" />
        </NFormItem>
        <NFormItem label="KeepAlive" path="keepalive">
          <NSwitch v-model:value="modalForm.keepalive" />
        </NFormItem>
      </NForm>
    </CrudModal>
  </CommonPage>
</template>
