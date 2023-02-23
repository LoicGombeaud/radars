import { reactive } from "vue"

const backUrl = "https://radars.loicgombeaud.com"

export const radars = reactive({
  all: await (async () => {
    const res = await fetch(`${backUrl}/radars`)
    return await res.json()
  })(),
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
