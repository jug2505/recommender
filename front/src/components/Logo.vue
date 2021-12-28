<template>
  <div class="logo">
    <span>{{modelValue}}</span>
  </div>
</template>

<script>
export default {
  name: "Logo",
  props: {
    modelValue: {
      type: String,
      default: "MovieRecs"
    }
  },
  data () {
    return {}
  }
}
</script>

<style scoped>
.logo {
  font-family: 'Ropa Sans', Arial, Helvetica, sans-serif;
  color: #ffffff;
  font-size: 36px;
}
</style>