import { reactive } from "vue"

const backUrl = "https://radars.loicgombeaud.com"

export const radars = reactive({
  all: [],
  async getAll() {
    if (this.all.length != 0) {
      return this.all
    }
    const res = await fetch(`${backUrl}/radars`)
    const data = await res.json()
    this.all = data
    return data
  },
})

export const statistics = reactive({
  daily: {},
  hourly: {},
  async getDailyStatistics(radarId) {
    if (radarId && !this.daily[radarId]) {
      const res = await fetch(`${backUrl}/statistics/daily/${radarId}/yesterday`)
      const data = await res.json()
      this.daily[radarId] = data
      return data
    }
  },
  async getHourlyStatistics(radarId) {
    if (radarId && !this.hourly[radarId]) {
      const res = await fetch(`${backUrl}/statistics/hourly/${radarId}/yesterday`)
      const data = await res.json()
      this.hourly[radarId] = data
      return data
    }
  },
})
