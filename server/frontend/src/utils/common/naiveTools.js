import { isNullOrUndef } from '@/utils'

export function setupMessage(NMessage) {
  let loadingMessage = null
  class Message {
    /**
     * Правила:
     * * Сообщение о загрузке (loading message) отображается только одно; новое сообщение заменит текущее сообщение о загрузке.
     * * Сообщение о загрузке не удаляется автоматически, если не будет заменено на не-загрузочное сообщение; не-загрузочные сообщения автоматически удаляются через 2 секунды.
     */

    removeMessage(message = loadingMessage, duration = 2000) {
      setTimeout(() => {
        if (message) {
          message.destroy()
          message = null
        }
      }, duration)
    }

    showMessage(type, content, option = {}) {
      if (loadingMessage && loadingMessage.type === 'loading') {
        // Если сообщение о загрузке уже существует, заменяем его новым сообщением
        loadingMessage.type = type
        loadingMessage.content = content

        if (type !== 'loading') {
          // Не-загрузочные сообщения должны автоматически удаляться
          this.removeMessage(loadingMessage, option.duration)
        }
      } else {
        // Если сообщение о загрузке не существует, создаем новое сообщение; если новое сообщение - это сообщение о загрузке, сохраняем его
        let message = NMessage[type](content, option)
        if (type === 'loading') {
          loadingMessage = message
        }
      }
    }

    loading(content) {
      this.showMessage('loading', content, { duration: 0 })
    }

    success(content, option = {}) {
      this.showMessage('success', content, option)
    }

    error(content, option = {}) {
      this.showMessage('error', content, option)
    }

    info(content, option = {}) {
      this.showMessage('info', content, option)
    }

    warning(content, option = {}) {
      this.showMessage('warning', content, option)
    }
  }

  return new Message()
}

export function setupDialog(NDialog) {
  NDialog.confirm = function (option = {}) {
    const showIcon = !isNullOrUndef(option.title)
    return NDialog[option.type || 'warning']({
      showIcon,
      positiveText: 'ОК', // Переведено
      negativeText: 'Отмена', // Переведено
      onPositiveClick: option.confirm,
      onNegativeClick: option.cancel,
      onMaskClick: option.cancel,
      ...option,
    })
  }

  return NDialog
}
