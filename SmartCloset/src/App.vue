<script setup>
import { RouterLink, RouterView } from 'vue-router'
</script>

<template>
  <header>
    <div class="wrapper">
      <nav>
        <RouterLink to="/">Home</RouterLink>
        <RouterLink to="/about">About</RouterLink>
      </nav>
    </div>
  </header>

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
