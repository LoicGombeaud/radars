<script>
import "leaflet/dist/leaflet.css"
import {
  LMap,
  LMarker,
  LTileLayer,
} from "@vue-leaflet/vue-leaflet"
import {
  Offcanvas,
} from "bootstrap"
import Statistics from "./Statistics.vue"
import { radars } from "../js/datastore.js"

export default {
  components: {
    LMap,
    LMarker,
    LTileLayer,
    Statistics,
  },
  data () {
    return {
      center: [44.84, -0.57],
      zoom: 13,
      minZoom: 13,
      maxZoom: 15,
      maxBounds: [
        [44.89, -0.65],
        [44.81, -0.53],
      ],
      offcanvasBreakpoint: 500, //TODO adjust depending on graphs' width
      offcanvasPlacement: "",
      offcanvasClasses: {
        offcanvas: true,
        show: false,
      },
      activeRadarId: "",
      radars: [],
    }
  },
  methods: {
    updateOffcanvasPlacement: function() {
      this.offcanvasPlacement = window.innerWidth < this.offcanvasBreakpoint ? "bottom" : "start"
    },
    updateOffcanvasClasses: function() {
      this.updateOffcanvasPlacement()
      var isShown = this.$refs.offcanvas.classList.contains("show")
      this.offcanvasClasses = {
        offcanvas: true,
        show: isShown,
        "offcanvas-bottom": this.offcanvasPlacement == "bottom",
        "offcanvas-start": this.offcanvasPlacement == "start",
      }
    },
    onClickMarker(event) {
      this.activeRadarId = event.target.options.radarId
      var myOffcanvasEl = document.getElementById("offcanvas")
      var offcanvas = Offcanvas.getOrCreateInstance(myOffcanvasEl)
      offcanvas.show()
    },
    async fetchRadars() {
      this.radars = await radars.getAll()
    }
  },
  mounted() {
    addEventListener("resize", this.updateOffcanvasClasses)
    this.updateOffcanvasClasses()
    this.fetchRadars()
  },
}
</script>

<template>
  <div class="container-fluid px-0" id="map-container">
    <l-map
      ref="map"
      v-model:zoom="zoom"
      :center="center"
      :minZoom="minZoom"
      :maxZoom="maxZoom"
      :maxBounds="maxBounds"
      :options="{
        zoomControl: false,
        attributionControl: false,
      }"
    >
      <l-tile-layer
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        layer-type="base"
        name="OpenStreetMap"
      ></l-tile-layer>
      <l-marker
        v-for="radar of radars"
        :lat-lng="[radar.latitude, radar.longitude]"
        :options="{radarId: radar.id}"
        @click="onClickMarker"
      ></l-marker>
    </l-map>
    <div
      :class="offcanvasClasses"
      tabindex="-1"
      id="offcanvas"
      ref="offcanvas"
      aria-labelledby="offcanvasLabel"
    >
      <Statistics :radar="radars.find((radar) => radar.id == activeRadarId)" />
    </div>
  </div>
</template>
