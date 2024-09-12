import React from 'react';
import './App.css'; 
import CountryCard from './components/CountryCard';
import logo from './logo.png'; 
import data from './countriesData.json'; 

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
      </header>
      <div className="cards-container">
        {data.map((country, index) => (
          <CountryCard key={index} country={country} />
        ))}
      </div>
    </div>
  );
}

export default App;
