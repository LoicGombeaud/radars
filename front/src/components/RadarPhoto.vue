<script>
export default {
  props: {
    radarId: String,
  },
  methods: {
    getRadarPhotoUrl() {
      //TODO get actual URL (obviously)
      return "https://images.unsplash.com/photo-1595433707802-6b2626ef1c91?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxleHBsb3JlLWZlZWR8MXx8fGVufDB8fHx8&w=1000&q=80"
    },
  },
}
</script>

<template>
  <h5>Implantation</h5>
  <img :src="getRadarPhotoUrl(radarId)" class="img-fluid">
</template>
