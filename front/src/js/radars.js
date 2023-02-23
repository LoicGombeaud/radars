import { reactive } from "vue"

const backUrl = "https://radars.loicgombeaud.com"

export const radars = reactive({
  all: await (async () => {
    const res = await fetch(`${backUrl}/radars`)
    return await res.json()
  })(),
})
