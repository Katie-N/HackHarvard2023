import './assets/main.css'

import { createApp } from 'vue'
// import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'

import { initializeApp } from "firebase/app";
import { firebaseConfig } from "./firebaseConfig.js"
import { getFirestore } from "firebase/firestore";

// init firebase
const firestoreApp = initializeApp(firebaseConfig);
// init services
const db = getFirestore(firestoreApp);

const app = createApp(App)
// app.use(createPinia())
app.use(router)

app.mount('#app')
