<script>
import { statistics } from "../js/datastore.js"

export default {
  props: {
    radarId: String,
  },
  watch: {
    radarId() {
      this.hourlyStatistics = this.getHourlyStatistics()
    },
  },
  data() {
    return {
      hourlyStatistics: {},
    }
  },
  methods: {
    async getHourlyStatistics() {
      this.hourlyStatistics = await statistics.getHourlyStatistics(this.radarId)
    },
  }
}
</script>

<template>
  <h5>Détail d'hier</h5>
  <p>{{ hourlyStatistics }}</p>
</template>
