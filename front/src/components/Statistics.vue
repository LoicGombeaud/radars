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
    radarId: String,
  },
  data() {
    return {
      showHistory: false,
    }
  },
}
</script>

<template>
  <div class="offcanvas-header">
    <h4 class="offcanvas-title" id="offcanvasLabel">TODO: Radar address</h4>
    <button type="button" class="btn-close text-reset" data-bs-dismiss="offcanvas" aria-label="Close"></button>
  </div>
  <div class="offcanvas-body">
    <div class="container-fluid">
      <div class="row">
        <div class="col">
          <RadarPhoto :radarId="radarId"/>
        </div>
        <div class="col">
          <DailySummary :radarId="radarId"/>
        </div>
        <div class="col">
          <DailyDetail :radarId="radarId"/>
        </div>
        <div class="col" v-if="showHistory">
          <History :radarId="radarId"/>
        </div>
      </div>
    </div>
  </div>
</template>
