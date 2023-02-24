<script>
import RadarPhoto from "./RadarPhoto.vue"
import DailyDetail from "./DailyDetail.vue"
import DailySummary from "./DailySummary.vue"
import History from "./History.vue"

export default {
  components: {
    RadarPhoto,
    DailyDetail,
    DailySummary,
    History,
  },
  props: {
    radar: {
      type: Object,
      default: {},
    },
  },
  data() {
    return {
      showHistory: false,
    }
  },
}
</script>

<template>
  <div class="offcanvas-header bg-dark text-white">
    <h4 class="offcanvas-title" id="offcanvasLabel">{{ radar.address }}</h4>
    <button type="button" class="btn-close text-reset btn-close-white" data-bs-dismiss="offcanvas" aria-label="Close"></button>
  </div>
  <div class="offcanvas-body">
    <div class="container-fluid">
      <div class="row">
        <RadarPhoto :radarId="radar.id"/>
      </div>
      <div class="row">
        <DailySummary :radarId="radar.id"/>
      </div>
      <div class="row">
        <DailyDetail :radarId="radar.id"/>
      </div>
      <!--
      <div class="col" v-if="showHistory">
        <History :radarId="radar.id"/>
      </div>
      -->
    </div>
  </div>
</template>
