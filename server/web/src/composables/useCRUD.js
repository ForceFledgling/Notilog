import { isNullOrWhitespace } from '@/utils'

const ACTIONS = {
  view: 'Просмотр',
  edit: 'Редактировать',
  add: 'Добавить',
}

export default function ({ name, initForm = {}, doCreate, doDelete, doUpdate, refresh }) {
  const modalVisible = ref(false)
  const modalAction = ref('')
  const modalTitle = computed(() => ACTIONS[modalAction.value] + name)
  const modalLoading = ref(false)
  const modalFormRef = ref(null)
  const modalForm = ref({ ...initForm })

  /** Добавить */
  function handleAdd() {
    modalAction.value = 'add'
    modalVisible.value = true
    modalForm.value = { ...initForm }
  }

  /** Редактировать */
  function handleEdit(row) {
    modalAction.value = 'edit'
    modalVisible.value = true
    modalForm.value = { ...row }
  }

  /** Просмотр */
  function handleView(row) {
    modalAction.value = 'view'
    modalVisible.value = true
    modalForm.value = { ...row }
  }

  /** Сохранить */
  function handleSave(...callbacks) {
    if (!['edit', 'add'].includes(modalAction.value)) {
      modalVisible.value = false
      return
    }
    modalFormRef.value?.validate(async (err) => {
      if (err) return
      const actions = {
        add: {
          api: () => doCreate(modalForm.value),
          cb: () => {
            callbacks.forEach((callback) => callback && callback())
          },
          msg: () => $message.success('Добавление успешно'),
        },
        edit: {
          api: () => doUpdate(modalForm.value),
          cb: () => {
            callbacks.forEach((callback) => callback && callback())
          },
          msg: () => $message.success('Редактирование успешно'),
        },
      }
      const action = actions[modalAction.value]

      try {
        modalLoading.value = true
        const data = await action.api()
        action.cb()
        action.msg()
        modalLoading.value = modalVisible.value = false
        data && refresh(data)
      } catch (error) {
        modalLoading.value = false
      }
    })
  }

  /** Удалить */
  async function handleDelete(params = {}) {
    if (isNullOrWhitespace(params)) return
    try {
      modalLoading.value = true
      const data = await doDelete(params)
      $message.success('Удаление успешно')
      modalLoading.value = false
      refresh(data)
    } catch (error) {
      modalLoading.value = false
    }
  }

  return {
    modalVisible,
    modalAction,
    modalTitle,
    modalLoading,
    handleAdd,
    handleDelete,
    handleEdit,
    handleView,
    handleSave,
    modalForm,
    modalFormRef,
  }
}
