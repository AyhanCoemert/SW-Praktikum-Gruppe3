import React, {useContext, useState, useEffect } from 'react';
import {auth} from '../firebase'

const AuthContext = React.createContext()

export function useAuth(){
    return useContext(AuthContext)
}

export function AuthProvider({children}) {
    const [CurrentUser, setCurrentUser] = useState()

    function registrierung (email, passwort){
       return auth.createUserWithEmailAndPassword(email, passwort)
        
    }

    useEffect(() => {
     const unsubscribe =  auth.onAuthStateChanged(user => {
            setCurrentUser(user)
    
        })
        return unsubscribe
    }, [])

    

    const value = {
      CurrentUser,
      registrierung
  }
    return(

        <AuthContext.Provider value={value}>
            {children}
        </AuthContext.Provider>
  )
}
