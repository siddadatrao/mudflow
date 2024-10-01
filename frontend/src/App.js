import React from 'react';
import './App.css';
import PodcastForm from './components/PodcastForm';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <h1>Podcast to LinkedIn Post Generator</h1>
      </header>
      <main>
        <PodcastForm />
      </main>
    </div>
  );
}

export default App;