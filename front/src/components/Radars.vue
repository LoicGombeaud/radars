<script>
import {
  LMarker,
  LPopup,
} from "@vue-leaflet/vue-leaflet"
import RadarPopup from "./RadarPopup.vue"

export default {
  data() {
    return {
      radars: [],
      popupOptions: {
        maxWidth: 10000,
      },
    }
  },
  components: {
    LMarker,
    LPopup,
    RadarPopup,
  },
  methods: {
    async fetchRadars() {
      //TODO parametrize?
      const res = await fetch("https://radars.loicgombeaud.com/radars")
      this.radars = await res.json()
    },
  },
  mounted() {
    this.fetchRadars()
  },
}
</script>

<template>
  <l-marker v-for="radar of radars" :lat-lng="[radar.latitude, radar.longitude]">
    <l-popup :options="popupOptions">
      <RadarPopup 
        :radarId="radar.id"
        :radarAddress="radar.address"
      />
    </l-popup>
  </l-marker>
</template>
