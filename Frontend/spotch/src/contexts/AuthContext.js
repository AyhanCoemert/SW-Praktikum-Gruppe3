import React, {useContext, useState, useEffect } from 'react'
import {auth} from '../firebase'


//@author [Soumayyah Aboubakar](https://github.com/soumayyahaboubakar)


const AuthContext = React.createContext()

export function useAuth(){
    return useContext(AuthContext)
}

export function AuthProvider({children}) {
    const [currentUser, setCurrentUser] = useState()

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
      currentUser,
      registrierung
  }
    return(

        <AuthContext.Provider value={value}>
            {children}
        </AuthContext.Provider>
  )
}
