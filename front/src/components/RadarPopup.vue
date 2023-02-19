<script>
import {
  Tab,
  Tabs,
} from "vue3-tabs-component"
import "../assets/tabs-component.css"

import Plotly from 'plotly.js-dist'

export default {
  data() {
    return {
      hourlyStatistics: {},
      dailyStatistics: {},
    }
  },
  computed: {
    n_total() {
      return this.dailyStatistics.n_total
    },
    n_over_limit() {
      return this.dailyStatistics.n_30_to_40 +
             this.dailyStatistics.n_40_to_50 +
             this.dailyStatistics.n_50_to_60 +
             this.dailyStatistics.n_60_to_70 +
             this.dailyStatistics.n_over_70
    },
    p_over_limit() {
      return Math.round(100 * this.n_over_limit / this.n_total)
    },
    v_avg() {
      return Math.round(10 * this.dailyStatistics.v_avg) / 10
    },
  },
  components: {
    Tab,
    Tabs,
  },
  props: {
    radarId: String,
    radarAddress: String,
  },
  methods: {
    async fetchStatistics() {
      const resDaily = await fetch(`https://radars.loicgombeaud.com/statistics/daily/${this.radarId}/yesterday`)
      this.dailyStatistics = await resDaily.json()
      const resHourly = await fetch(`https://radars.loicgombeaud.com/statistics/hourly/${this.radarId}/yesterday`)
      this.hourlyStatistics = await resHourly.json()

      // Draw daily statistics pie chart
      Plotly.newPlot(
        this.$refs.daily,
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

      // Draw hourly statistics scatter chart
      Plotly.newPlot(
        this.$refs.hourly,
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
          height: 400,
          width: 400,
          yaxis: {
            rangemode: "tozero",
            ticksuffix: " km/h",
          },
          legend: {
            xanchor: "left",
            x: 0.1,
            yanchor: "bottom",
            y: -.7,
          },
        }
      )
    },
    getPhotoUrl(radarId) {
      return new URL(`../assets/img/${radarId}.webp`, import.meta.url).href
    },
  },
  mounted() {
    this.fetchStatistics()
  },
}
</script>

<template>
  <tabs :options="{ useUrlFragment: false }">
    <tab name="Résumé du jour (J - 1)">
      <h1>Radar : {{radarAddress}}</h1>
      {{n_total}} mesures effectuées, dont {{n_over_limit}} excès de vitesse ({{p_over_limit}}%)<br>
      Vitesse moyenne : {{v_avg}} km/h<br>
      Vitesse 85% : {{dailyStatistics.v_85p}} km/h<br>
      Vitesse maximum: {{dailyStatistics.v_max}} km/h
      <div ref="daily"></div>
    </tab>
    <tab name="Détail du jour (J - 1)">
      <h1>Radar : {{radarAddress}}</h1>
      <div ref="hourly"></div>
    </tab>
    <tab name="Photo">
      <h1>Radar : {{radarAddress}}</h1>
      <img
        :src="getPhotoUrl(radarId)"
        class="radar-photo"/>
    </tab>
    <tab name="Historique" :is-disabled="true">
    </tab>
  </tabs>
</template>
