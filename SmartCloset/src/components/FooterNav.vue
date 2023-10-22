<template>
  <main>
    <div id="navbar">
      <router-link to="/user"><img src="../assets/user.png" /></router-link>
      <router-link to="/inspo"><img src="../assets/idea.png" /></router-link>
      <router-link to="/upload"><img src="../assets/plus.png" /></router-link>
      <router-link to="/closet"><img src="../assets/clothes-hanger.png" /></router-link>
    </div>
  </main>
</template>

<style scoped>
  #navbar {
    display: grid;
    grid-template-columns: 1fr 1fr 1fr 1fr;
    width: 100%;
    position: fixed;
    bottom: 0;
    padding: 0;
    background-color: #faf9f2;
  }

  #navbar > * {
    width: 100%;
    padding: 1rem;
  }

  img {
    max-width: 100%;
    max-height: 100%;
  }

  main {

  }
</style>
