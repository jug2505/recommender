<template>
  <div>
    <div class="filmrow">
      <film-card
          v-for="movie in movies"
          cardImage="movie.card_image" title="movie.title" genre="movie.genre"/>
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
        has_other_pages: false,
        has_previous: false,
        has_next: false,
        previous_page_number: 1,
        next_page_number: 1,
        number: 1
      },
      genres: [],
      api_key: "",
      session_id: "",
      user_id: "",
      pages: []
    }
  },

  methods: {
    add_impression(user_id, event_type, content_id, session_id) {
      try {
        axios.post("http://localhost:8081/collect/log/", {
          params: {
            "event_type": event_type,
            "user_id": user_id,
            "content_id": content_id,
            "session_id": session_id
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

    async getPicture(movie_id) {
      let url = 'https://api.themoviedb.org/3/find/tt' + movie_id + '?external_source=imdb_id&api_key=' + this.api_key
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
