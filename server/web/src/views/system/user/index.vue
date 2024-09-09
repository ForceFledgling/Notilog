<script setup>
import { h, onMounted, ref, resolveDirective, withDirectives } from 'vue'
import {
  NButton,
  NCheckbox,
  NCheckboxGroup,
  NForm,
  NFormItem,
  NImage,
  NInput,
  NSpace,
  NSwitch,
  NTag,
  NPopconfirm,
  NLayout,
  NLayoutSider,
  NLayoutContent,
  NTreeSelect,
} from 'naive-ui'

import CommonPage from '@/components/page/CommonPage.vue'
import QueryBarItem from '@/components/query-bar/QueryBarItem.vue'
import CrudModal from '@/components/table/CrudModal.vue'
import CrudTable from '@/components/table/CrudTable.vue'

import { formatDate, renderIcon } from '@/utils'
import { useCRUD } from '@/composables'
import api from '@/api'
import TheIcon from '@/components/icon/TheIcon.vue'
import { useUserStore } from '@/store'

defineOptions({ name: 'Упр пользователями' })

const $table = ref(null)
const queryItems = ref({})
const vPermission = resolveDirective('permission')

const {
  modalVisible,
  modalTitle,
  modalAction,
  modalLoading,
  handleSave,
  modalForm,
  modalFormRef,
  handleEdit,
  handleDelete,
  handleAdd,
} = useCRUD({
  name: 'Пользователь',
  initForm: {},
  doCreate: api.createUser,
  doUpdate: api.updateUser,
  doDelete: api.deleteUser,
  refresh: () => $table.value?.handleSearch(),
})

const roleOption = ref([])
const deptOption = ref([])

onMounted(() => {
  $table.value?.handleSearch()
  api.getRoleList({ page: 1, page_size: 9999 }).then((res) => (roleOption.value = res.data))
  api.getDepts().then((res) => (deptOption.value = res.data))
})

const columns = [
  {
    title: 'Имя',
    key: 'username',
    width: 60,
    align: 'center',
    ellipsis: { tooltip: true },
  },
  {
    title: 'Электронная почта',
    key: 'email',
    width: 60,
    align: 'center',
    ellipsis: { tooltip: true },
  },
  {
    title: 'Роль пользователя',
    key: 'role',
    width: 60,
    align: 'center',
    render(row) {
      const roles = row.roles ?? []
      const group = []
      for (let i = 0; i < roles.length; i++)
        group.push(
          h(NTag, { type: 'info', style: { margin: '2px 3px' } }, { default: () => roles[i].name })
        )
      return h('span', group)
    },
  },
  {
    title: 'Отдел',
    key: 'dept.name',
    align: 'center',
    width: 40,
    ellipsis: { tooltip: true },
  },
  {
    title: 'Суперпользователь',
    key: 'is_superuser',
    align: 'center',
    width: 40,
    render(row) {
      return h(
        NTag,
        { type: 'info', style: { margin: '2px 3px' } },
        { default: () => (row.is_superuser ? 'Да' : 'Нет') }
      )
    },
  },
  {
    title: 'Последний вход',
    key: 'last_login',
    align: 'center',
    width: 80,
    ellipsis: { tooltip: true },
    render(row) {
      return h(
        NButton,
        { size: 'small', type: 'text', ghost: true },
        {
          default: () => (row.last_login !== null ? formatDate(row.last_login) : null),
          icon: renderIcon('mdi:update', { size: 16 }),
        }
      )
    },
  },
  {
    title: 'Отключен',
    key: 'is_active',
    width: 50,
    align: 'center',
    render(row) {
      return h(NSwitch, {
        size: 'small',
        rubberBand: false,
        value: row.is_active,
        loading: !!row.publishing,
        checkedValue: false,
        uncheckedValue: true,
        onUpdateValue: () => handleUpdateDisable(row),
      })
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
              size: 'small',
              type: 'primary',
              style: 'margin-right: 8px;',
              onClick: () => {
                handleEdit(row)
                modalForm.value.dept_id = row.dept?.id
                modalForm.value.role_ids = row.roles.map((e) => (e = e.id))
                delete modalForm.value.dept
              },
            },
            {
              default: () => 'Редактировать',
              icon: renderIcon('material-symbols:edit', { size: 16 }),
            }
          ),
          [[vPermission, 'post/api/v1/user/update']]
        ),
        h(
          NPopconfirm,
          {
            onPositiveClick: () => handleDelete({ user_id: row.id }, false),
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
                [[vPermission, 'delete/api/v1/user/delete']]
              ),
            default: () => h('div', {}, 'Вы уверены, что хотите удалить этого пользователя?'),
          }
        ),
      ]
    },
  },
]

// Обновление состояния пользователя
async function handleUpdateDisable(row) {
  if (!row.id) return
  const userStore = useUserStore()
  if (userStore.userId === row.id) {
    $message.error('Невозможно отключить текущего пользователя!')
    return
  }
  row.publishing = true
  row.is_active = row.is_active === false ? true : false
  row.publishing = false
  const role_ids = []
  row.roles.forEach((e) => {
    role_ids.push(e.id)
  })
  row.role_ids = role_ids
  row.dept_id = row.dept?.id
  try {
    await api.updateUser(row)
    $message?.success(row.is_active ? 'Пользователь снова активен' : 'Пользователь отключен')
    $table.value?.handleSearch()
  } catch (err) {
    // В случае ошибки восстановление прежнего состояния
    row.is_active = row.is_active === false ? true : false
  } finally {
    row.publishing = false
  }
}

let lastClickedNodeId = null

const nodeProps = ({ option }) => {
  return {
    onClick() {
      if (lastClickedNodeId === option.id) {
        $table.value?.handleSearch()
        lastClickedNodeId = null
      } else {
        api.getUserList({ dept_id: option.id }).then((res) => {
          $table.value.tableData = res.data
          lastClickedNodeId = option.id
        })
      }
    },
  }
}

const validateAddUser = {
  username: [
    {
      required: true,
      message: 'Пожалуйста, введите имя',
      trigger: ['input', 'blur'],
    },
  ],
  email: [
    {
      required: true,
      message: 'Пожалуйста, введите адрес электронной почты',
      trigger: ['input', 'change'],
    },
    {
      trigger: ['blur'],
      validator: (rule, value, callback) => {
        const re = /^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$/
        if (!re.test(modalForm.value.email)) {
          callback('Неверный формат электронной почты')
          return
        }
        callback()
      },
    },
  ],
  password: [
    {
      required: true,
      message: 'Пожалуйста, введите пароль',
      trigger: ['input', 'blur', 'change'],
    },
  ],
  confirmPassword: [
    {
      required: true,
      message: 'Пожалуйста, повторите пароль',
      trigger: ['input'],
    },
    {
      trigger: ['blur'],
      validator: (rule, value, callback) => {
        if (value !== modalForm.value.password) {
          callback('Пароли не совпадают')
          return
        }
        callback()
      },
    },
  ],
  roles: [
    {
      type: 'array',
      required: true,
      message: 'Пожалуйста, выберите хотя бы одну роль',
      trigger: ['blur', 'change'],
    },
  ],
}
</script>

<template>
  <NLayout has-sider wh-full>
    <NLayoutSider
      bordered
      content-style="padding: 24px;"
      :collapsed-width="0"
      :width="240"
      show-trigger="arrow-circle"
    >
      <h1>Список отделов</h1>
      <br />
      <NTree
        block-line
        :data="deptOption"
        key-field="id"
        label-field="name"
        default-expand-all
        :node-props="nodeProps"
      >
      </NTree>
    </NLayoutSider>
    <NLayoutContent>
      <CommonPage show-footer title="Список пользователей">
        <template #action>
          <NButton v-permission="'post/api/v1/user/create'" type="primary" @click="handleAdd">
            <TheIcon icon="material-symbols:add" :size="18" class="mr-5" />Создать пользователя
          </NButton>
        </template>
        <!-- Таблица -->
        <CrudTable
          ref="$table"
          v-model:query-items="queryItems"
          :columns="columns"
          :get-data="api.getUserList"
        >
          <template #queryBar>
            <QueryBarItem label="Имя" :label-width="40">
              <NInput
                v-model:value="queryItems.username"
                clearable
                type="text"
                placeholder="Введите имя пользователя"
                @keypress.enter="$table?.handleSearch()"
              />
            </QueryBarItem>
            <QueryBarItem label="Электронная почта" :label-width="40">
              <NInput
                v-model:value="queryItems.email"
                clearable
                type="text"
                placeholder="Введите адрес электронной почты"
                @keypress.enter="$table?.handleSearch()"
              />
            </QueryBarItem>
          </template>
        </CrudTable>

        <!-- Окно добавления/редактирования -->
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
            :rules="validateAddUser"
          >
            <NFormItem label="Имя пользователя" path="username">
              <NInput v-model:value="modalForm.username" clearable placeholder="Введите имя пользователя" />
            </NFormItem>
            <NFormItem label="Электронная почта" path="email">
              <NInput v-model:value="modalForm.email" clearable placeholder="Введите адрес электронной почты" />
            </NFormItem>
            <NFormItem v-if="modalAction === 'add'" label="Пароль" path="password">
              <NInput
                v-model:value="modalForm.password"
                show-password-on="mousedown"
                type="password"
                clearable
                placeholder="Введите пароль"
              />
            </NFormItem>
            <NFormItem v-if="modalAction === 'add'" label="Подтверждение пароля" path="confirmPassword">
              <NInput
                v-model:value="modalForm.confirmPassword"
                show-password-on="mousedown"
                type="password"
                clearable
                placeholder="Подтвердите пароль"
              />
            </NFormItem>
            <NFormItem label="Роли" path="role_ids">
              <NCheckboxGroup v-model:value="modalForm.role_ids">
                <NSpace item-style="display: flex;">
                  <NCheckbox
                    v-for="item in roleOption"
                    :key="item.id"
                    :value="item.id"
                    :label="item.name"
                  />
                </NSpace>
              </NCheckboxGroup>
            </NFormItem>
            <NFormItem label="Суперпользователь" path="is_superuser">
              <NSwitch
                v-model:value="modalForm.is_superuser"
                size="small"
                :checked-value="true"
                :unchecked-value="false"
              ></NSwitch>
            </NFormItem>
            <NFormItem label="Отключен" path="is_active">
              <NSwitch
                v-model:value="modalForm.is_active"
                :checked-value="false"
                :unchecked-value="true"
                :default-value="true"
              />
            </NFormItem>
            <NFormItem label="Отдел" path="dept_id">
              <NTreeSelect
                v-model:value="modalForm.dept_id"
                :options="deptOption"
                key-field="id"
                label-field="name"
                placeholder="Выберите отдел"
                clearable
                default-expand-all
              ></NTreeSelect>
            </NFormItem>
          </NForm>
        </CrudModal>
      </CommonPage>
    </NLayoutContent>
  </NLayout>
  <!-- Страница с бизнес-логикой -->
</template>
