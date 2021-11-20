<template>
  <div class="card">
    <img :src="cardImage" :alt="'img: ' + title">
    <div class="info">
      <div class="top">
        <div class="name"> {{ title }}</div>
        <div class="genre"> {{ genre }}</div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "FilmCard",
  data() {
    return {
      cardImage: this.$attrs.cardImage,
      title: this.$attrs.title,
      genre: this.$attrs.genre,
    }
  }
}
</script>

<style scoped>
.card {
  font-family: 'Roboto', serif;
  display: flex;
  flex-direction: column;
  width: 315px;
  height: 200px;
  color: white;
  margin-right: 5px;
}

.info {
  display: flex;
  flex-direction: column;
  gap: 5px;
  padding: 7px;
  background-color: #202020;
  border-bottom-left-radius: 3px;
  border-bottom-right-radius: 3px;
}

.name {
  font-weight: 700;
}

.genre {
  font-size: smaller;
}

</style>