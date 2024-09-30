import React, { useState } from 'react';

const API_URL = process.env.REACT_APP_API_URL || '';

function App() {
  const [podcastUrl, setPodcastUrl] = useState('');
  const [linkedInPost, setLinkedInPost] = useState('');
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLinkedInPost('');
    setError('');
    try {
      console.log('Sending request to:', `${API_URL}/api/generate-post`);
      const response = await fetch(`${API_URL}/api/generate-post`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ podcast_url: podcastUrl })
      });
      console.log('Response status:', response.status);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const data = await response.json();
      console.log('Received data:', data);
      setLinkedInPost(data.post);
    } catch (error) {
      console.error('Error details:', error);
      setError(`An error occurred: ${error.message}`);
    }
  };

  return (
    <div style={{ padding: '20px' }}>
      <h1>Podcast LinkedIn Post Generator</h1>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          value={podcastUrl}
          onChange={(e) => setPodcastUrl(e.target.value)}
          placeholder="Enter podcast URL"
          required
        />
        <button type="submit">Generate Post</button>
      </form>
      {linkedInPost && (
        <div>
          <h2>Generated LinkedIn Post:</h2>
          <p>{linkedInPost}</p>
        </div>
      )}
      {error && <p style={{color: 'red'}}>{error}</p>}
    </div>
  );
}

export default App;