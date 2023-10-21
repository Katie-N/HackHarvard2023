<script setup>
import { RouterLink, RouterView } from 'vue-router'
</script>

<template>
  <FooterNav />
  <RouterView />
</template>

<script>
import FooterNav from './components/FooterNav.vue'

export default {
  components: {
    FooterNav
  },
}
</script>

<style scoped>
header {
  max-height: 100vh;
}
</style>
