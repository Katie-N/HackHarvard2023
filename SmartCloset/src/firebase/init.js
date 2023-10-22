import { initializeApp } from "firebase/app";
import { firebaseConfig } from "./firebaseConfig.js"
import { getFirestore } from "firebase/firestore";

// init firebase
const firestoreApp = initializeApp(firebaseConfig);
// init services
const db = getFirestore(firestoreApp);

export { db }
