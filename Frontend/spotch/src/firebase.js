import firebase from 'firebase/compat/app';
import "firebase/auth"

const app = firebase.initializeApp({
  apiKey: process.env.React_App_Firebase_Api_Key,
  authDomain: process.env.React_App_Firebase_AuthDomain ,
  projectId: process.env.React_App_Firebase_ProjectId ,
  storageBucket: process.env.React_App_Firebase_StorageBucket ,
  messagingSenderId: process.env.React_App_Firebase_MessagingSenderId ,
  appId:process.env.React_App_Firebase_AppId 
})


export const auth = app.auth
export default app