<template>
  <div class="parent-pick">
  <div class="pick">

    <router-link :to="{ name: 'Front page' }">
      <header-button msg="Выбрать случайного пользователя с 10 оцененными фильмами" @click="changeId(10)"/>
    </router-link>

    <router-link :to="{ name: 'Front page' }">
      <header-button msg="Выбрать случайного пользователя с 50 оцененными фильмами" @click="changeId(50)"/>
    </router-link>


  </div>
  </div>
</template>
 
<script>
import store from '../store'
import axios from 'axios';
import HeaderButton from "../components/UI/HeaderButton";

let API_URL = 'http://localhost:8081'

export default {
  name: "UserPick",
  components: {HeaderButton},

   data () {
    return {
    }
  },
  methods: {
    changeId(num){
      axios
        .get(API_URL + "/rec/user/num/" + num + "/")
        .then( (response) => { store.state.user_id = response.data.user_id } )
        .catch( (error) => { console.log(error) })
    }
  }
}
</script>

<style scoped>
.parent-pick {
  display: flex;
  justify-content: center;
  flex-direction: row;
  align-items:flex-start;

  height: 68vh;
}
.pick {
  width: fit-content;
  display: flex;
  justify-content: center;
  flex-direction: column;
  /*align-items:center;*/
}
a {
  text-decoration: none;
}
</style>