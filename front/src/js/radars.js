import { reactive } from "vue"

const backUrl = "https://radars.loicgombeaud.com"

export const radars = reactive({
  all: [],
  async getAll() {
    if (!this["all"] || this["all"].length == 0) {
      const res = await fetch(`${backUrl}/radars`)
      this["all"] = await res.json()
    }
    console.log(this["all"])
    return this.all
  },
})
