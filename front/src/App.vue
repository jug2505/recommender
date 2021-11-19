<template>
  <div>
    <recommender-home/>
  </div>
</template>

<script>
import RecommenderHome from './views/RecommenderHome.vue'
export default {
  components: { RecommenderHome },
  data() {
    return {
    }
  }
}
</script>

<style>
@import url('https://fonts.googleapis.com/css2?family=Ropa+Sans&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Roboto+Condensed&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Roboto&display=swap');
* {
  margin: 0;
  padding: 0;
}
body {
  background-color: #121212;
}
</style>