<template>
  <main>
    <!-- Grid of images -->
    <div id="recommendations">
      <div class="square" v-for="match in matches" @click="openMatch(match)">
        <img :src="match.img.src">
      </div>
    </div>
    <!-- <div @click="getMatchesFromFirestore()">Click Me</div> -->
    <!-- <img src="https://storage.googleapis.com/smartcloset-ef535.appspot.com/inspo/c015b055009057c8e7875276adc787ab.jpg" /> -->
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
import { getDocs, collection } from 'firebase/firestore'
import { db } from '../firebase/init.js'

export default {
  // data() {
  //   return {
  //     matches: [],
  //   }
  // },
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
    // openMatch(selectedMatch) {
    //   console.log("open " + selectedMatch.uid);
    // },
    // async getMatchesFromFirestore() {
    //   // This retrieves all of the outfits the user is able to wear (all of the matches)
    //   const docsSnap = await getDocs(collection(db, "users/0000000000000000000/outfitsDEMO"))
    //
    //   docsSnap.forEach((doc) => {
    //     console.log("doc", doc.data()); // "doc1", "doc2" and "doc3"
    //     this.matches.push(doc.data());
    //   });
    //   console.log("in data: ", this.matches);
    //   console.log(this.matches[0].srcUrl);
    // },
  },
}
</script>
