<script>
import Statistics from "./Statistics.vue"

export default {
  components: {
    Statistics,
  },
  data () {
    return {
      offcanvasBreakpoint: 500, //TODO adjust depending on graphs' width
      offcanvasPlacement: "",
      offcanvasClasses: {
        offcanvas: true,
        show: false,
      },
      activeRadar: "13H15",
    }
  },
  methods: {
    updateOffcanvasPlacement: function() {
      this.offcanvasPlacement = window.innerWidth < this.offcanvasBreakpoint ? "bottom" : "start"
    },
    updateOffcanvasClasses: function() {
      this.updateOffcanvasPlacement()
      var isShown = this.$el.querySelector("#offcanvas").classList.contains("show")
      this.offcanvasClasses = {
        offcanvas: true,
        show: isShown,
        "offcanvas-bottom": this.offcanvasPlacement == "bottom",
        "offcanvas-start": this.offcanvasPlacement == "start",
      }
    },
  },
  mounted() {
    addEventListener("resize", this.updateOffcanvasClasses)
    this.updateOffcanvasClasses()
  },
}
</script>

<template>
  <div class="container">
    <div class="row align-items-start">
      <div class="border col-md order-last">Column one</div>
      <div class="border col-md">Column two</div>
      <div class="border col-md">Column three</div>
    </div>
    <div class="row bg-light rounded-5">
      <div class="col">v<sub>moyenne</sub></div>
      <div class="col">v<sub>85%</sub></div>
      <div class="col">v<sub>maximum</sub></div>
    </div>
    <div class="row align-items-end">
      <div class="border col">Column one</div>
      <div class="border col">Column two</div>
      <div class="border col">Column three</div>
    </div>
    <button class="btn btn-primary" type="button" data-bs-toggle="offcanvas" data-bs-target="#offcanvas" aria-controls="offcanvas">Toggle offcanvas</button>

    <div :class="offcanvasClasses" tabindex="-1" id="offcanvas" aria-labelledby="offcanvasLabel">
      <div class="offcanvas-header">
        <h4 class="offcanvas-title" id="offcanvasLabel">TODO: Radar address</h4>
        <button type="button" class="btn-close text-reset" data-bs-dismiss="offcanvas" aria-label="Close"></button>
      </div>
      <div class="offcanvas-body">
        <Statistics :radarId="activeRadar" />
      </div>
    </div>
  </div>
</template>
