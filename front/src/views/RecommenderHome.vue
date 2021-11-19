<template>
  <div class="recommender-home">
    <base-header/>
    <div class="body">
      <router-view/>
    </div>
    <base-footer/>
  </div>
</template>

<script>
import BaseHeader from '../components/BaseHeader.vue'
import BaseFooter from '../components/BaseFooter.vue'

export default {
  name: "RecommenderHome",
  components: { BaseFooter, BaseHeader },
  data () {
    return {
    }
  }
}
</script>

<style scoped>
.recommender-home {
  background-color: #343434;
  display: flex;
  flex-direction: column;
  height: 100vh;
}
.body {
  padding: 10px;
}
</style>