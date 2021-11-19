<template>
  <div class="user">
    <i class="fas fa-user"></i>
  </div>
</template>

<script>
import '@fortawesome/fontawesome-free/js/all.min.js'
export default {
  name: "ProfileButton",
  data () {
    return {
    }
  }
}
</script>

<style scoped>
.user {
  background-color: #ffffff;
  width: 50px;
  height: 50px;
  display: grid;
  place-items: center;
  border-radius: 50%;
  font-size: 24px;
}

</style>