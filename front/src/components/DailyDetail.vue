<script>
import { statistics } from "../js/datastore.js"

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
  <h5>Détail d'hier</h5>
  <p>TODO graphique détaillé de {{ radarId }}</p>
  <p>{{ statistics.lazyLoad(radarId).hourly }}</p>
</template>
