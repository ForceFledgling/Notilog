<template>
  <QueryBar v-if="$slots.queryBar" mb-30 @search="handleSearch" @reset="handleReset">
    <slot name="queryBar" />
  </QueryBar>

  <n-data-table
    :remote="remote"
    :loading="loading"
    :columns="columns"
    :data="tableData"
    :scroll-x="scrollX"
    :row-key="(row) => row[rowKey]"
    :pagination="isPagination ? pagination : false"
    @update:checked-row-keys="onChecked"
    @update:page="onPageChange"
  />
</template>

<script setup>
const props = defineProps({
  /**
   * @remote true: постраничная навигация с сервера  false: постраничная навигация на клиенте
   */
  remote: {
    type: Boolean,
    default: true,
  },
  /**
   * @remote Нужна ли постраничная навигация
   */
  isPagination: {
    type: Boolean,
    default: true,
  },
  scrollX: {
    type: Number,
    default: 450,
  },
  rowKey: {
    type: String,
    default: 'id',
  },
  columns: {
    type: Array,
    required: true,
  },
  /** Параметры в queryBar */
  queryItems: {
    type: Object,
    default() {
      return {}
    },
  },
  /** Дополнительные параметры (опционально) */
  extraParams: {
    type: Object,
    default() {
      return {}
    },
  },
  /**
   * ! Определение параметров входных и выходных данных интерфейса
   * * Для режима постраничной навигации необходимо согласовать параметры запроса на постраничную навигацию
   *    @page_size Параметр постраничной навигации: сколько записей отображается на одной странице, по умолчанию 10
   *    @page   Параметр постраничной навигации: номер страницы, по умолчанию 1
   */
  getData: {
    type: Function,
    required: true,
  },
})

const emit = defineEmits(['update:queryItems', 'onChecked', 'onDataChange'])
const loading = ref(false)
const initQuery = { ...props.queryItems }
const tableData = ref([])
const pagination = reactive({
  page: 1,
  page_size: 10,
  pageSizes: [10, 20, 50, 100],
  showSizePicker: true,
  prefix({ itemCount }) {
    return `Всего ${itemCount} записей`
  },
  onChange: (page) => {
    pagination.page = page
  },
  onUpdatePageSize: (pageSize) => {
    pagination.page_size = pageSize
    pagination.page = 1
    handleQuery()
  },
})

async function handleQuery() {
  try {
    loading.value = true
    let paginationParams = {}
    // Если режим постраничной навигации не используется или используется клиентская постраничная навигация, параметры постраничной навигации не требуются
    if (props.isPagination && props.remote) {
      paginationParams = { page: pagination.page, page_size: pagination.page_size }
    }
    const { data, total } = await props.getData({
      ...props.queryItems,
      ...props.extraParams,
      ...paginationParams,
    })
    tableData.value = data
    pagination.itemCount = total || 0
  } catch (error) {
    tableData.value = []
    pagination.itemCount = 0
  } finally {
    emit('onDataChange', tableData.value)
    loading.value = false
  }
}
function handleSearch() {
  pagination.page = 1
  handleQuery()
}
async function handleReset() {
  const queryItems = { ...props.queryItems }
  for (const key in queryItems) {
    queryItems[key] = ''
  }
  emit('update:queryItems', { ...queryItems, ...initQuery })
  await nextTick()
  pagination.page = 1
  handleQuery()
}
function onPageChange(currentPage) {
  pagination.page = currentPage
  if (props.remote) {
    handleQuery()
  }
}
function onChecked(rowKeys) {
  if (props.columns.some((item) => item.type === 'selection')) {
    emit('onChecked', rowKeys)
  }
}

defineExpose({
  handleSearch,
  handleReset,
  tableData,
})
</script>
