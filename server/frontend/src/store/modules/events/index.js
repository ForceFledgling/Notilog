// server/frontend/src/store/modules/event/index.js

import { defineStore } from 'pinia'
import api from '@/api'

export const useEventStore = defineStore('event', {
  state() {
    return {
      events: [],       // Список событий
      currentEvent: {}, // Текущая выбранная информация о событии
      totalEvents: 0,   // Общее количество событий
    }
  },
  getters: {
    eventList() {
      return this.events
    },
    eventCount() {
      return this.totalEvents
    },
    eventDetails() {
      return this.currentEvent
    },
  },
  actions: {
    // Получение списка всех событий
    async fetchEvents(params = {}) {
      try {
        const res = await api.getEventList(params) // Используем getEventList
        this.events = res.data.items // Пример структуры ответа: { items: [], total: number }
        this.totalEvents = res.data.total
        return res.data
      } catch (error) {
        console.error('Error fetching events:', error)
        return error
      }
    },

    // Получение информации о конкретном событии
    async fetchEventById(id) {
      try {
        const res = await api.getEventById({ id }) // Используем getEventById
        this.currentEvent = res.data
        return res.data
      } catch (error) {
        console.error('Error fetching event by ID:', error)
        return error
      }
    },

    // Сброс информации о событиях
    resetEvents() {
      this.events = []
      this.totalEvents = 0
      this.currentEvent = {}
    },
  },
})
