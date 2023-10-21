<template>
  <main>
    <!-- Grid of images -->
    <div id="recommendations">
      <div class="square" v-for="match in matches" @click="openMatch(match)">
        <img :src="match.img.src" :alt="match.img.alt">
      </div>
    </div>
  </main>
</template>

<style scoped>
  main {
    height: 100%;
  }

  #recommendations {
    display: grid;
    grid-template-columns: 1fr 1fr 1fr;
    grid-gap: 5px;
    margin: 1rem;
  }

  .square {
    width: 100%;
    height: 100%;
    aspect-ratio: 1;
    margin: 0;
    padding: 0;
  }

  .square > img {
    width: 100%;
    /* Forces the image to set the height equal to the width */
    aspect-ratio: 1;
    object-fit: cover;
    vertical-align: bottom;
  }
</style>

<script>
export default {
  computed: {
    matches: {
      get: function() {
        // get matches from firestore...

        // example data for now:
        return [
        {
          uid: 1,
          img: {
            src: "https://styleworthyblog.com/wp-content/uploads/2019/01/DSC_0814.jpg", // link to the match in google storage bucket
            alt: "outfit",
          },
        },
        {
          uid: 2,
          img: {
            src: "https://styleworthyblog.com/wp-content/uploads/2019/01/DSC_0814.jpg", // link to the match in google storage bucket
            alt: "outfit",
          },
        },
        {
          uid: 3,
          img: {
            src: "https://styleworthyblog.com/wp-content/uploads/2019/01/DSC_0814.jpg", // link to the match in google storage bucket
            alt: "outfit",
          },
        },
        {
          uid: 4,
          img: {
            src: "https://styleworthyblog.com/wp-content/uploads/2019/01/DSC_0814.jpg", // link to the match in google storage bucket
            alt: "outfit",
          },
        },
        {
          uid: 4,
          img: {
            src: "https://styleworthyblog.com/wp-content/uploads/2019/01/DSC_0814.jpg", // link to the match in google storage bucket
            alt: "outfit",
          },
        },
        {
          uid: 4,
          img: {
            src: "https://styleworthyblog.com/wp-content/uploads/2019/01/DSC_0814.jpg", // link to the match in google storage bucket
            alt: "outfit",
          },
        },
        {
          uid: 4,
          img: {
            src: "https://styleworthyblog.com/wp-content/uploads/2019/01/DSC_0814.jpg", // link to the match in google storage bucket
            alt: "outfit",
          },
        },
        ]
      },
    }
  },
  methods: {
    openMatch(selectedMatch) {
      console.log("open " + selectedMatch.uid);
    }
  },
}
</script>
