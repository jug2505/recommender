<template>
  <router-link
    :to="{ name: 'Movie info', params: { id: id } }"
    style="text-decoration: none; color: inherit;">
  <div class="card">
    <img :src="card_image" :alt="'img: ' + title">
    <div class="info">
      <div class="top">
        <div class="name"> {{ title }}</div>
        <div class="genre"> {{ year }}</div>
      </div>
    </div>
  </div>
  </router-link>
</template>

<script>
export default {
  name: "FilmCard",
  props: {
    id: {
      type: String,
      default: ""
    },
    card_image: {
      type: String,
      default: ""
    },
    title: {
      type: String,
      default: ""
    },
    year: {
      type: Number,
      default: 0
    }
  },
  data() {
    return {

    }
  }
}
</script>

<style scoped>
.card {
  font-family: 'Roboto', serif;
  display: flex;
  flex-direction: column;
  width: 150px; /*185px*/
  height: 310px; /*350px*/
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
  font-size: small;
}

.genre {
  font-size: smaller;
}

</style>