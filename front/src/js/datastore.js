import { reactive } from "vue"

const backUrl = "https://radars.loicgombeaud.com"

export const radars = reactive({
  all: await (async () => {
    const res = await fetch(`${backUrl}/radars`)
    return await res.json()
  })(),
})

export const statistics = reactive({
  "13H12": {
    daily: "daily stats",
    hourly: "hourly stats",
  },
  lazyLoad(radarId) {
    if (!this[radarId]) {
      this[radarId] = {
        daily: `lazy-loaded daily stats for ${radarId}`,
        hourly: `lazy-loaded hourly stats for ${radarId}`,
      }
    }
    return this[radarId]
  },
})
