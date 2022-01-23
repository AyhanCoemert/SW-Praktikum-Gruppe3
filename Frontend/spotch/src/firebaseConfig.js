import { initializeApp } from "firebase/compat/app";
import { getAuth } from "firebase/compat/auth";

const firebaseConfig = {
    apiKey: process.env.React_App_Firebase_Api_Key,
    authDomain: process.env.React_App_Firebase_AuthDomain ,
    projectId: process.env.React_App_Firebase_ProjectId ,
    storageBucket: process.env.React_App_Firebase_StorageBucket ,
    messagingSenderId: process.env.React_App_Firebase_MessagingSenderId ,
    appId:process.env.React_App_Firebase_AppId 
  
};

const app = initializeApp(firebaseConfig);

export const auth = getAuth(app);