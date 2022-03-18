<template>
  <div class="info">
    <div class="errors" v-if="errors">
      <div v-for="error in errors" :key="error.id" class="error">
        {{ error }}
      </div>
    </div>
    <div class="movie-content" v-if="errors.length == 0">
      <div class="left">
        <img :src="movie.poster_path" :alt="'img: ' + movie.title">
      </div>
      <div class="right">
        <div class="header">
          <div class="top"> 
            <div class="name"> {{ movie.title }}</div>
            <div class="stars" :style="{width: movie.rating / 5 * 45 + 'px'}">
              <i class="fas fa-star"></i>
              <i class="fas fa-star"></i>
              <i class="fas fa-star"></i>
              <i class="fas fa-star"></i>
              <i class="fas fa-star"></i>
            </div>
          </div>
          <div class="bottom">
            <div class="bl">
              <div class="genre" v-for="genre in movie.movie_genres" :key="genre.name"> {{ genre.name }}</div>
            </div>
          </div>
        </div>
        <div class="description">
          {{ movie.description }}
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

let API_URL = 'http://localhost:8081'

export default {
  name: "MovieInfo",
  
  data () {
      return {
        movie: {},
        errors: []
      }
  },
  
  created () {
    axios.get(API_URL + "/rec/movie/" + this.$route.params.id + "/")
      .then(response => {
        this.movie = response.data
        this.getPoster()
      })
      .catch(error => {
        if (error.response.status == 404) {
          this.errors.push('404: movie not found')
        }
    })
    },
    methods: {
      getPoster() {
        axios.get('https://api.themoviedb.org/3/find/tt' + this.$route.params.id + '?external_source=imdb_id&api_key=' + this.movie.api_key)
          .then(response => {
            if (response.data.movie_results && response.data.movie_results[0] && response.data.movie_results[0].poster_path) {
              this.movie.poster_path = "http://image.tmdb.org/t/p/w185/" + response.data.movie_results[0].poster_path
              this.movie.description = response.data.movie_results[0].overview
              this.movie.rating = response.data.movie_results[0].vote_average
              this.movie.title = response.data.movie_results[0].original_title
            }
             console.log(this.movie)
          })
          .catch(error => {
            if (error.response.status == 404) {
              this.errors.push('404: movie not found')
            }
          })
      }
    }
}
</script>

<style scoped>
* {
    font-family: 'Roboto', sans-serif;
}
.info {
  height: 68vh;
}
.errors {
  display: flex;
  justify-content: center;
}
.errors .error {
  padding: 10px;
  background-color: #a04e4e;
  border: 1px solid #d85f5f;
  border-radius: 3px;
}
.movie-content {
  width: 1024px;
  margin: 0 auto;
  display: flex;
  gap: 20px;
}
.movie-content .left {
  display: flex;
  flex-direction: column;
  gap: 10px;
}
.movie-content .right {
  display: flex;
  flex-direction: column;
  width: 100%;
  align-items: stretch;
}
.movie-content .right .header {
  padding-bottom: 10px;
  margin-bottom: 10px;
  border-bottom: 2px solid #545454;
}
.movie-content .right .header .top {
  display: flex;
  align-items: center;
  gap: 5px;
}
.movie-content .right .header .top .name {
  color: #ffffff;
  font-size: 36px;
  font-weight: 700;
}
.movie-content .right .header .top .stars {
  display: flex;
  color: #FFF511;
  overflow: hidden;
  width: 90px;
}
.movie-content .right .bottom {
  display: flex;
  align-items: center;
  gap: 5px;
}
.movie-content .right .bottom .bl {
  display: flex;
  align-items: center;
  gap: 5px;
}
.movie-content .right .bottom .bl .genre {
  color: #cacaca;
  font-size: smaller;
}
.movie-content .description {
  color: #ffffff;
}

</style>