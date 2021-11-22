<template>
  <div>
    <div class="filmrow">
        <film-card
            v-for="movie in movies"
            v-bind:title="movie.title"
            v-bind:genre="movie.year"
            :card_image="movie.card_image"
            v-bind:key="movie.movie_id"/>
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
        this.api_key = response.data.api_key
        this.session_id = response.data.session_id
        this.user_id = response.data.user_id
        this.pages = response.data.pages
      } catch (e) {
        alert(e)
      }
    },

    async getPicture(movie_id) {
      let url = 'https://api.themoviedb.org/3/find/tt' + movie_id + '?external_source=imdb_id&api_key=' + this.api_key
      const response = await axios.get(url)
      let path = ""
      if (response.data.movie_results && response.data.movie_results[0] && response.data.movie_results[0].poster_path) {
        path = "http://image.tmdb.org/t/p/w185/" + response.data.movie_results[0].poster_path
      }
      return path
    },

  },

  created() {
    this.fetchData().then(
        () => {
          this.movies.forEach(
              m => this.getPicture(m.movie_id).then(
                path => m.card_image = path
              ).then(() => {
                this.movies = this.movies.filter(m => m.card_image !== "")
              })
          )
        }
    )
  }
}
</script>

<style>
.filmrow {
  display: flex;
  flex-wrap: wrap;
}
</style>
