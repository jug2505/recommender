<template>
  <div class="base-btn"> {{ msg }}</div>
</template>

<script>
export default {
  name: "HeaderButton",
  data() {
    return {
      msg: this.$attrs.msg
    }
  }
}
</script>

<style scoped>
.base-btn {
  display: grid;
  place-items: center;
  height: 50px;
  padding: 0 14px;
  border-radius: 3px;
  background-color: #343434;
  text-align: center;
  color: #ffffff;
  font-size: 18px;
  font-family: 'Roboto Condensed', sans-serif;
}
.base-btn:hover {
  background-color: #232323;
}
</style>