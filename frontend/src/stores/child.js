import { defineStore } from 'pinia'
import { childApi } from '@/api/child'

export const useChildStore = defineStore('child', {
  state: () => ({
    children: [],
    currentChild: null,
  }),

  getters: {
    childList: (state) => state.children,
    hasChildren: (state) => state.children.length > 0,
  },

  actions: {
    setCurrentChild(child) {
      this.currentChild = child
    },

    async fetchChildren(userId) {
      try {
        const children = await childApi.getChildList(userId)
        this.children = children
        if (children.length > 0 && !this.currentChild) {
          this.currentChild = children[0]
        }
        return children
      } catch (error) {
        throw error
      }
    },

    async addChild(childData) {
      try {
        const child = await childApi.createChild(childData)
        this.children.push(child)
        if (!this.currentChild) {
          this.currentChild = child
        }
        return child
      } catch (error) {
        throw error
      }
    },

    async updateChild(childId, data) {
      try {
        const child = await childApi.updateChild(childId, data)
        const index = this.children.findIndex((c) => c.id === childId)
        if (index !== -1) {
          this.children[index] = child
        }
        if (this.currentChild?.id === childId) {
          this.currentChild = child
        }
        return child
      } catch (error) {
        throw error
      }
    },

    async deleteChild(childId) {
      try {
        await childApi.deleteChild(childId)
        this.children = this.children.filter((c) => c.id !== childId)
        if (this.currentChild?.id === childId) {
          this.currentChild = this.children[0] || null
        }
      } catch (error) {
        throw error
      }
    },
  },
})
