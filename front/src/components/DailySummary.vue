<script>
import Plotly from "plotly.js-dist-min"
import { statistics } from "../js/datastore.js"

export default {
  props: {
    radarId: String,
  },
  watch: {
    radarId() {
      this.dailyStatistics = this.getDailyStatistics()
    },
    dailyStatistics() {
      if (this.dailyStatistics) {
        this.drawPlot()
      }
      else {
        this.dailyStatistics = {}
      }
    }
  },
  data() {
    return {
      dailyStatistics: {},
    }
  },
  computed: {
    n_over_30() {
      return this.dailyStatistics.n_30_to_40 +
             this.dailyStatistics.n_40_to_50 +
             this.dailyStatistics.n_50_to_60 +
             this.dailyStatistics.n_60_to_70 +
             this.dailyStatistics.n_over_70
    },
    p_over_30() {
      return Math.round(100 * this.n_over_30 / this.dailyStatistics.n_total * 10) / 10
    },
    n_over_50() {
      return this.dailyStatistics.n_50_to_60 +
             this.dailyStatistics.n_60_to_70 +
             this.dailyStatistics.n_over_70
    },
    p_over_50() {
      return Math.round(100 * this.n_over_50 / this.dailyStatistics.n_total * 10) / 10
    },
  },
  methods: {
    async getDailyStatistics() {
      this.dailyStatistics = await statistics.getDailyStatistics(this.radarId)
    },
    drawPlot() {
      Plotly.newPlot(
        this.$refs.summaryPlot,
        [{
          type: "pie",
          values: [
            this.dailyStatistics.n_0_to_30,
            this.dailyStatistics.n_30_to_40,
            this.dailyStatistics.n_40_to_50,
            this.dailyStatistics.n_50_to_60 + this.dailyStatistics.n_60_to_70 + this.dailyStatistics.n_over_70,
          ],
          labels: [
            "0 - 30 km/h",
            "31 - 40 km/h",
            "41 - 50 km/h",
            "> 50 km/h",
          ],
          marker: {
            colors: [
              "#92E000",
              "#F58B00",
              "#DE3700",
              "#000000",
            ]
          },
          textinfo: "label+value",
          insidetextorientation: "horizontal",
          sort: false,
          direction: "clockwise",
          showlegend: false,
        }],
        {},
        {
          responsive: true,
        },
      )
    }
  }
}
</script>

<template>
  <p class="h3 mb-4">Répartition par tranche de vitesse</p>
  <p>Sur {{ dailyStatistics.n_total }} mesures effectuées :</p>
  <p>- {{ n_over_30 }} excès de vitesse, soit {{ p_over_30 }}%</p>
  <p>- {{ n_over_50 }} grands excès de vitesse (>50 km/h), soit {{ p_over_50 }}%</p>
  <div ref="summaryPlot" id="summaryPlot"></div>
</template>
