import React from 'react'
import Registrierung from './Components/Pages/Registrierung'
import { Container } from 'react-bootstrap'
import { AuthProvider } from './contexts/AuthContext'
import { BrowserRouter as Router, Switch, Route } from "react-router-dom"
import Login from './Components/Pages/Login'


function App() {
  return (

    
      <Container
       className="d-flex align-items-center justify-content-center"
        style = {{ minHeight:"100vh"}}
        >
          
        <div className="w-100" style={{maxWidth:'400px'}}>
          <Router>
          <AuthProvider>
            <Switch>
            <Route path="/login" component={Login} />
            <Route path="/registrierung" component={Registrierung} />
            </Switch>
          </AuthProvider>
          </Router>
           <Registrierung/>
        </div>
      </Container>
     
  )
}


export default App