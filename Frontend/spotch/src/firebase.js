import firebase from 'firebase/compat/app';
import 'firebase/compat/auth';

//@author [Soumayyah Aboubakar](https://github.com/soumayyahaboubakar)

const app = firebase.initializeApp({
  apiKey: process.env.REACT_APP_FIREBASE_API_KEY,
  authDomain: process.env.REACT_APP_FIREBASE_AUTHDOMAIN ,
  projectId: process.env.REACT_APP_FIREBASE_PROJECTID ,
  storageBucket: process.env.REACT_APP_FIREBASE_STORAGEBUCKET ,
  messagingSenderId: process.env.REACT_APP_FIREBASE_MESSAGINGSENDERID ,
  appId: process.env.REACT_APP_FIREBASE_APPID
})


export const auth = app.auth()
export default app 
 







/* import { initializeApp } from "firebase/compat/app";
import { getAuth } from "firebase/auth";

const firebaseConfig = {
    apiKey: process.env.React_App_Firebase_Api_Key,
    authDomain: process.env.React_App_Firebase_AuthDomain ,
    projectId: process.env.React_App_Firebase_ProjectId ,
    storageBucket: process.env.React_App_Firebase_StorageBucket ,
    messagingSenderId: process.env.React_App_Firebase_MessagingSenderId ,
    appId:process.env.React_App_Firebase_AppId 
  
};

const app = initializeApp(firebaseConfig);

export const auth = getAuth(app); */