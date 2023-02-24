<script>
import Plotly from "plotly.js-dist-min"
import { statistics } from "../js/datastore.js"

export default {
  props: {
    radarId: String,
  },
  watch: {
    radarId() {
      this.hourlyStatistics = this.getHourlyStatistics()
    },
    hourlyStatistics() {
      if (this.hourlyStatistics instanceof Array) {
        this.drawPlot()
      }
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
    drawPlot() {
      Plotly.newPlot(
        this.$refs.detailPlot,
        [
          {
            type: "scatter",
            name: "Vitesse maximum",
            x: this.hourlyStatistics.map(stat => new Date(stat.datetime).getHours() + "h"),
            y: this.hourlyStatistics.map(stat => stat.v_max),
            marker: {
              color: "red",
            },
          },
          {
            type: "scatter",
            name: "Vitesse 85%",
            x: this.hourlyStatistics.map(stat => new Date(stat.datetime).getHours() + "h"),
            y: this.hourlyStatistics.map(stat => stat.v_85p),
            marker: {
              color: "gray",
            },
          },
          {
            type: "scatter",
            name: "Vitesse moyenne",
            x: this.hourlyStatistics.map(stat => new Date(stat.datetime).getHours() + "h"),
            y: this.hourlyStatistics.map(stat => stat.v_avg),
            marker: {
              color: "black",
            },
          },
          {
            type: "scatter",
            name: "Vitesse limite autorisée",
            x: this.hourlyStatistics.map(stat => new Date(stat.datetime).getHours() + "h"),
            y: this.hourlyStatistics.map(stat => 30),
            marker: {
              color: "green",
            },
          },
        ],
        {
          xaxis: {
            fixedrange: true,
          },
          yaxis: {
            rangemode: "tozero",
            ticksuffix: " km/h",
            fixedrange: true,
          },
          legend: {
            xanchor: "left",
            x: 0.1,
            yanchor: "bottom",
            y: -.7,
          },
        },
        {
          responsive: true,
        },
      )
    }
  }
}
</script>

<template>
  <p class="h3 mb-4">Vitesses calculées, heure par heure</p>
  <p>Pour chaque créneau d'une heure, on affiche ici :</p>
  <p>- la vitesse maximum mesurée sur ce créneau</p>
  <p>- la vitesse 85% (cf. <router-link to="/explications">Explications</router-link>)</p>
  <p>- la vitesse moyenne</p>
  <div ref="detailPlot" id="detailPlot"></div>
</template>
