<template>
  <div class="front-page">
    <div class="film-row">
        <film-card
            v-for="movie in movies"
            :id="movie.movie_id"
            :title="movie.title"
            :year="movie.year"
            :card_image="movie.card_image"
            :rating="parseInt(movie.rating)"
            v-bind:key="movie.movie_id"/>
    </div>
    
    <div v-if="pop_movies.length !== 0" class="row-title">
      Рекомендации на основе популярности
    </div>
    <div class="film-row">
      <film-card
          v-for="movie in pop_movies"
          :id="movie.movie_id"
          :title="movie.title"
          :year="movie.year"
          :card_image="movie.card_image"
          v-bind:key="movie.movie_id"/>
    </div>

    <div v-if="cf_movies.length !== 0" class="row-title">
      Рекомендации на основе коллаборативной фильтрации
    </div>
    <div class="film-row">
      <film-card
          v-for="movie in cf_movies"
          :id="movie.movie_id"
          :title="movie.title"
          :year="movie.year"
          :card_image="movie.card_image"
          v-bind:key="movie.movie_id"/>
    </div>

    <div v-if="svd_movies.length !== 0" class="row-title">
      Рекомендации на основе SVD
    </div>
    <div class="film-row">
      <film-card
          v-for="movie in svd_movies"
          :id="movie.movie_id"
          :title="movie.title"
          :year="movie.year"
          :card_image="movie.card_image"
          v-bind:key="movie.movie_id"/>
    </div>

    <div v-if="cont_movies.length !== 0" class="row-title">
      Рекомендации на основе описаний фильмов
    </div>
    <div class="film-row">
      <film-card
          v-for="movie in cont_movies"
          :id="movie.movie_id"
          :title="movie.title"
          :year="movie.year"
          :card_image="movie.card_image"
          v-bind:key="movie.movie_id"/>
    </div>

    <div v-if="knn_movies.length !== 0" class="row-title">
      Рекомендации KNN
    </div>
    <div class="film-row">
      <film-card
          v-for="movie in knn_movies"
          :id="movie.movie_id"
          :title="movie.title"
          :year="movie.year"
          :card_image="movie.card_image"
          v-bind:key="movie.movie_id"/>
    </div>

    <div v-if="hybrid_movies.length !== 0" class="row-title">
      Рекомендации гибридной рекомендательной системы
    </div>
    <div class="film-row">
      <film-card
          v-for="movie in hybrid_movies"
          :id="movie.movie_id"
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

let API_URL = 'http://localhost:8081'

export default {
  name: "FrontPage",
  components: {FilmCard},

  data () {
    return {
      movies: [],
      pop_movies: [],
      cf_movies: [],
      svd_movies: [],
      cont_movies: [],
      hybrid_movies: [],
      knn_movies: [],
      
      api_key: "",
    }
  },

  created() {
    this.getWatched()
    this.getPopRecs()
    this.getCFRecs()
    this.getSVDRecs()
    this.getContRecs()
    this.getHybridRecs()
    this.getKNNRecs()
  },
  methods: {

    getWatched(){
      axios
        .get(API_URL + "/rec/movie/user/" + store.state.user_id + "/")
        .then(
          (response) => {
            this.movies = response.data.data
            this.api_key = response.data.api_key
            this.getMoviePosters(this.movies)
          })
        .catch((error) => { console.log(error) })
    },

    getPopRecs(){
      axios
        .get(API_URL + "/rec/pop/user/" + store.state.user_id + "/")
        .then(
          (response) => {
            this.pop_movies = response.data.data
            this.getMoviePosters(this.pop_movies)
          })
        .catch((error) => { console.log(error) })
    },

    getCFRecs(){
      axios
        .get(API_URL + "/rec/cf/user/" + store.state.user_id + "/")
        .then(
          (response) => {
            response.data.data.forEach(element => {
              this.cf_movies.push({movie_id: element[0], prediction: element[1].prediction})
            });
            this.getMoviePosters(this.cf_movies)
          })
        .catch((error) => { console.log(error) })
    },

    getSVDRecs(){
      axios
        .get(API_URL + "/rec/svd/user/" + store.state.user_id + "/")
        .then(
          (response) => {
            response.data.data.forEach(element => {
              this.svd_movies.push({movie_id: element[0], prediction: element[1].prediction})
            });
            
            //this.svd_movies = response.data.data
            this.getMoviePosters(this.svd_movies)
          })
        .catch((error) => { console.log(error) })
    },

    getContRecs(){
      axios
        .get(API_URL + "/rec/content/user/" + store.state.user_id + "/")
        .then(
          (response) => {
            response.data.data.forEach(element => {
              this.cont_movies.push({movie_id: element[0], prediction: element[1].prediction})
            });
            
            this.getMoviePosters(this.cont_movies)
          })
        .catch((error) => { console.log(error) })
    },

    getHybridRecs(){
      axios
        .get(API_URL + "/rec/hybrid/user/" + store.state.user_id + "/")
        .then(
          (response) => {
            response.data.data.forEach(element => {
              this.hybrid_movies.push({movie_id: element[0], prediction: element[1]})
            });

            this.getMoviePosters(this.hybrid_movies)
          })
        .catch((error) => { console.log(error) })
    },

    getKNNRecs(){
      axios
        .get(API_URL + "/rec/knn/user/" + store.state.user_id + "/")
        .then(
          (response) => {
            response.data.data.forEach(element => {
              this.knn_movies.push({movie_id: element.movie_id, prediction: element.prediction})
            });
            
            this.getMoviePosters(this.knn_movies)
          })
        .catch((error) => { console.log(error) })
    },

    getMoviePosters(movies) {
      if (movies.length !== 0) {
        for (let i = 0; i < movies.length; i++) {
          axios
            .get(API_URL + "/rec/movie/" + movies[i].movie_id + "/")
            .then(
              (info_responce) => {
                movies[i].title = info_responce.data.title
                movies[i].year = info_responce.data.year

                axios
                  .get('https://api.themoviedb.org/3/find/tt' + movies[i].movie_id + '?external_source=imdb_id&api_key=' + this.api_key)
                  .then(
                    (image_responce) => {
                      let path = ""
                      if (image_responce.data.movie_results && image_responce.data.movie_results[0] && image_responce.data.movie_results[0].poster_path) {
                        path = "http://image.tmdb.org/t/p/w185/" + image_responce.data.movie_results[0].poster_path
                      }
                      movies[i].card_image = path
                  })
                  .catch((error) => { console.log(error) })
            })
            .catch((error) => { console.log(error) })
        }
      }
    }
  },
}
</script>

<style>
.front-page {
    width: 1024px;
    margin: 0 auto;
}
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
