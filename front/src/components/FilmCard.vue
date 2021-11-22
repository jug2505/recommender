<template>
  <div class="card">
    <img :src="card_image" :alt="'img: ' + title">
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
  props: {
    card_image: {
      type: String,
      default: ""
    }
  },
  data() {
    return {
      title: this.$attrs.title,
      genre: this.$attrs.genre,
      //card_image: this.$attrs.card_image,
    }
  }
}
</script>

<style scoped>
.card {
  font-family: 'Roboto', serif;
  display: flex;
  flex-direction: column;
  width: 185px; /*315*/
  height: 350px; /*200*/
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