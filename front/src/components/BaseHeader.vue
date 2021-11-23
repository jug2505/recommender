<template>
  <div class="nav">
    <div class="left">
      <router-link :to="{ name: 'Front page' }">
        <logo/>
      </router-link>
      <router-link :to="{ name: 'About' }">
        <header-button msg="О проекте"/>
      </router-link>
      <search-bar/>
    </div>
    <div class="right">
      <user-button
      :user_id="user_id"
      />
      <profile-button/>
    </div>
  </div>
</template>

<script>
import HeaderButton from "./UI/HeaderButton";
import SearchBar from "./UI/SearchBar";
import ProfileButton from "./UI/ProfileButton";
import Logo from "./Logo";
import UserButton from "./UI/UserButton";
import axios from "axios";

export default {
  name: "BaseHeader",
  components: {HeaderButton, SearchBar, ProfileButton, Logo, UserButton},
  data () {
    return {
      user_id: ""
    }
  },
  methods: {
    async fetchData(){
      try {
        const response = await axios.get("http://localhost:8081/movies/userinfo/")
        this.user_id = response.data.user_id
      } catch (e) {
        alert(e)
      }
    }
  },
  mounted() {
    this.fetchData()
  }
}
</script>

<style scoped>
.nav {
  background-color: #434343;
  padding: 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 2px solid #545454;
}
.left, .right {
  display: flex;
  align-items: center;
  gap: 20px;
}
a {
  text-decoration: none;
}

</style>