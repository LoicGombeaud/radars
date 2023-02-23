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
      this.drawPlot()
    }
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
        {
          height: 400,
          width: 400,
        }
      );
    }
  }
}
</script>

<template>
  <h5>Résumé d'hier</h5>
  <div ref="summaryPlot" id="summaryPlot"></div>
</template>
