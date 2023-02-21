<script>
import Map from "./components/Map.vue"
import Menu from "./components/Menu.vue"
import Statistics from "./components/Statistics.vue"

export default {
  components: {
    Map,
    Menu,
    Statistics,
  },
  data() {
    return {
    }
  },
}
</script>

<template>
  <Menu />
  <Map />
  <Statistics />
</template>
