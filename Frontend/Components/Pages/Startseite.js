import React, { Component } from 'react';
import './App.css';
import './index.css';
import './logo.svg';
import Anmelden from './components/Registrierung';
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


