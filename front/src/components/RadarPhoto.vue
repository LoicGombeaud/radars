<script>
export default {
  props: {
    radarId: String,
  },
  methods: {
    getRadarPhotoUrl() {
      return new URL(`../assets/img/${this.radarId}.webp`, import.meta.url).href
    },
  },
}
</script>

<template>
  <h5>Implantation</h5>
  <img :src="getRadarPhotoUrl(radarId)" class="img-fluid">
</template>
