import React from 'react';
import { Container } from 'react-bootstrap';
import Registrierung from './Components/Pages/Registrierung';
import { AuthProvider } from './contexts/AuthContext';


function App() {
  return (

    <AuthProvider>
      <Container className="d-flex align-items-center justify-content-center"
        style = {{ minHeight:"100vh"}}>
        <div className="w-100" style={{maxWidth:'400px'}}>
         <Registrierung/>
        </div>
      </Container>
    </AuthProvider> 
  )
}


export default App