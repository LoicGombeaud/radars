<script>
import { statistics } from "../js/statistics.js"

export default {
  props: {
    radarId: String,
  },
  data() {
    return {
      statistics,
    }
  },
}
</script>

<template>
  <h5>Résumé d'hier</h5>
  <p>TODO graphique résumé de {{ radarId }}</p>
  <p>{{ statistics.lazyLoad(radarId).daily}}</p>
</template>
