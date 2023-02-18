<script>
import "leaflet/dist/leaflet.css"
import {
  LMap,
  LTileLayer,
} from "@vue-leaflet/vue-leaflet"
import Radars from "./components/Radars.vue"

export default {
  components: {
    LMap,
    LTileLayer,
    Radars,
  },
  data() {
    return {
      zoom: 13,
      center: [44.84, -0.57],
    }
  },
}
</script>

<template>
  <div style="height:100vh; width:100vw">
    <l-map ref="map" v-model:zoom="zoom" :center="center">
      <l-tile-layer
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        layer-type="base"
        name="OpenStreetMap"
      ></l-tile-layer>
      <Radars />
    </l-map>
  </div>
</template>
