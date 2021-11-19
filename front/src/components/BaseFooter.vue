<template>
  <div class="footer">
    <div class="stats">
      <div class="numbers">
        <p> {{ uniqueItemsCount }}</p>
        <p> {{ userCount }}</p>
        <p> {{ ratingCount }}</p>
      </div>
      <div class="words">
        <p>уникальных фильмов</p>
        <p>уникальных пользователей</p>
        <p>рейтингов</p>
      </div>
    </div>
    <div class="media">
      <a href="https://twitter.com/mvtweetings"><i class="fab fa-twitter"></i></a>
      <a href="https://github.com/jug2505/recommender"><i class="fab fa-github"></i></a>
    </div>
    <div class="extra">
      Условия пользования
    </div>
  </div>
</template>

<script>
import '../../node_modules/@fortawesome/fontawesome-free/js/all.min.js'

export default {
  name: "BaseFooter",

  data() {
    return {
      uniqueItemsCount: "38k", // get dynamically later
      userCount: "72k",
      ratingCount: "921k",
    }
  },
}
</script>

<style scoped>
.footer {
  font-family: 'Roboto Condensed', serif;
  font-size: 18px;
  color: #cacaca;
  margin-top: auto;
  background-color: #232323;
  border-top: 2px solid #545454;
  padding: 70px 0;
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  gap: 10px;
  place-items: center;
}
.stats {
  display: grid;
  grid-template-columns: 1fr 2fr;
  gap: 5px;
  line-height: 1.5rem;
}
.numbers {
  text-align: end;
  color: #ffffff;
  font-weight: 700;
}
.media {
  display: flex;
  font-size: 26px;
  gap: 10px;
  color: inherit;
}
a:visited {
  color: inherit;
}
</style>