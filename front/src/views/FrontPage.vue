<template>
  <div>
    <div class="filmrow">
      <film-card
          v-for="movie in movies"
          cardImage="movie.cardImage" title="movie.title" genre="movie.genre"/>
    </div>
  </div>

</template>

<script>
import FilmCard from "../components/FilmCard";
import axios from 'axios';

export default {
  name: "FrontPage",
  components: {FilmCard},

  data () {
    return {
      page: 1,
      movies: [],
      paginator: {
        hasOtherPages: false,
        hasPrevious: false,
        hasNext: false,
        previousPageNumber: 1,
        nextPageNumber: 1,
        number: 1
      },
      genres: [],
      apiKey: "",
      sessionId: "",
      userId: "",
      pages: []
    }
  },

  methods: {
    add_impression(userId, eventType, contentId, sessionId) {
      try {
        axios.post("http://localhost:8081/collect/log/", {
          params: {
            "event_type": eventType,
            "user_id": userId,
            "content_id": contentId,
            "session_id": sessionId
          }
        })
      } catch (e) {
        alert(e)
      }
    },

    async fetchData() {
      try {
        const response = await axios.get("http://localhost:8081/movies/", {
          params: {
            page: this.page
          }
        })
        this.paginator = response.data.paginator
        this.movies = response.data.movies
        this.genres = response.data.genres
        this.apiKey = response.data.api_key
        this.sessionId = response.data.session_id
        this.userId = response.data.user_id
        this.pages = response.data.pages
      } catch (e) {
        alert(e)
      }
    },

    async getPicture(movieId) {
      let url = 'https://api.themoviedb.org/3/find/tt' + movieId + '?external_source=imdb_id&api_key=' + this.apiKey
      const response = await axios.get(url)
      this.movies.forEach(m => m.cardImage = "http://image.tmdb.org/t/p/w500/" + response.data.movie_results[0].poster_path)
    }

  },

  mounted() {
    this.fetchData()
  }
}
</script>

<style>
.filmrow {
  display: flex;
}
</style>
