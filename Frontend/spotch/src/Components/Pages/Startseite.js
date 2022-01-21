import React, { Component } from 'react';
import './App.css';
import './index.css';
import Registrierung from '.Components/Pages/Registrierung';
import SPO from './API/SPO'


class Homepage extends Component {

  render() {

    return (
      <div class="App-header">
		<Anmelden>Anmelden</Anmelden>
		<SPO>Dein online SPO</SPO>
      </div>
    );
  }
}

export default Homepage;


