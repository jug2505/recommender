<template>
  <div>
    <film-card cardImage="https://via.placeholder.com/315x140" title="title" genre="genre"/>
  </div>

</template>

<script>
import FilmCard from "../components/FilmCard";
export default {
  name: "FrontPage",
  components: {FilmCard},
  data () {
    return {
    }
  }
}
</script>

<style>
</style>
