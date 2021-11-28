<template>
  <div class="user-button">
    <button class="text">id: {{user_id}}</button>
  </div>
</template>

<script>
export default {
  name: "UserButton",
  props: {
    user_id : {
      type: String,
      default: ""
    }
  }
}
</script>

<style scoped>
.text {
  font-family: 'Roboto Condensed', sans-serif;
  padding: 12px;
  font-size: 18px;
  border-radius: 3px;
  border: 2px solid #70c56f;
  background-color: #8feb8d;
  color: #343434;
  cursor: pointer;
}
.text:hover {
  background-color: #70c56f;
}

</style>