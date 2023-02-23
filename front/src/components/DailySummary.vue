<script>
import { statistics } from "../js/datastore.js"

export default {
  props: {
    radarId: String,
  },
  watch: {
    radarId() {
      this.dailyStatistics = this.getDailyStatistics()
    },
  },
  data() {
    return {
      dailyStatistics: {},
    }
  },
  methods: {
    async getDailyStatistics() {
      this.dailyStatistics = await statistics.getDailyStatistics(this.radarId)
    },
  }
}
</script>

<template>
  <h5>Résumé d'hier</h5>
  <p>{{ dailyStatistics }}</p>
</template>
