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
</template>
