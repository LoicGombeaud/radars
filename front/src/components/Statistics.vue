<script>
import DailyDetail from "./DailyDetail.vue"
import DailySummary from "./DailySummary.vue"
import History from "./History.vue"
import RadarPhoto from "./RadarPhoto.vue"

export default {
  components: {
    DailyDetail,
    DailySummary,
    History,
    RadarPhoto,
  },
  data() {
    return {
    }
  },
}
</script>

<template>
  <div id="statistics">
    <RadarPhoto />
    <DailyDetail />
    <DailySummary />
    <History />
  </div>
</template>
