<template>
  <div>
    <div class="film-row">
        <film-card
            v-for="movie in movies"
            :title="movie.title"
            :year="movie.year"
            :card_image="movie.card_image"
            v-bind:key="movie.movie_id"/>
    </div>

    <div class="film-row">
      <div class="pagination" v-if="paginator.has_other_pages">
        <button v-if="paginator.has_previous" @click="changePage(paginator.previous_page_number)">&laquo;</button>
        <span v-for="i in pages" :key="i">
          <button class="active" v-if="i === paginator.number">{{ i }}</button>
          <button v-else @click="changePage(i)">{{ i }}</button>
        </span>
        <button v-if="paginator.has_next" @click="changePage(paginator.next_page_number)">&raquo;</button>
      </div>
    </div>

    <div v-if="movies_ar.length !== 0" class="row-title">
      Рекомендации на основе ассоциативных правил
    </div>
    <div class="film-row">
      <film-card
          v-for="movie in movies_ar"
          :title="movie.title"
          :year="movie.year"
          :card_image="movie.card_image"
          v-bind:key="movie.movie_id"/>
    </div>

  </div>

</template>

<script>
import FilmCard from "../components/FilmCard";
import store from '../store'
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
      user_id: store.state.user_id,
      pages: [],

      movies_ar: []
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
        //this.user_id = response.data.user_id
        this.pages = response.data.pages
      } catch (e) {
        alert(e)
      }
    },

    async fetchAR() {
      try {
        const response = await axios.get("http://localhost:8081/rec/ar/" + this.user_id + '/') // Поменять на this.user_id
        this.movies_ar = response.data.data
        if (this.movies_ar.length !== 0) {
          for (let i = 0; i < this.movies_ar.length; i++) {
            const ar_response = await axios.get("http://localhost:8081/movies/movie/" + this.movies_ar[i].movie_id + '/')
            this.movies_ar[i].title = ar_response.data.title
            this.movies_ar[i].year = ar_response.data.year

            this.movies_ar[i].card_image = await this.getPicture(this.movies_ar[i].movie_id)
          }
        }
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

    updateMovies() {
      this.fetchData().then(
          () => {
            this.movies.forEach(
                m => this.getPicture(m.movie_id).then(
                    path => m.card_image = path
                ).then(() => {
                  this.movies = this.movies.filter(m => m.card_image !== "")
                })
            )
            this.fetchAR()
          }
      )
    },

    changePage(val) {
      this.page = val
      console.log(val)
      this.updateMovies()
    }

  },

  created() {
    this.updateMovies()
  }
}
</script>

<style>
.film-row {
  display: flex;
  flex-wrap: wrap;
}
.pagination {
  display: inline-block;
}
.pagination button {
  font-family: 'Roboto', serif;
  font-size: large;
  color: black;
  float: left;
  padding: 5px 12px;
  text-decoration: none;
}
.pagination button.active {
  background-color: #e3e331;
  color: black;
  border-radius: 5px;
}
.pagination button:hover:not(.active) {
  background-color: #ddd;
  border-radius: 5px;
}

.row-title {
  padding: 5px;
  color: #ffffff;
  font-size: 18px;
  font-family: 'Roboto Condensed', sans-serif;
}
</style>
