import React, { useState } from 'react';

function App() {
  const [podcastUrl, setPodcastUrl] = useState('');
  const [linkedInPost, setLinkedInPost] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch('/api/generate-post', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ podcast_url: podcastUrl })
      });
      const data = await response.json();
      setLinkedInPost(data.post);
    } catch (error) {
      console.error('Error:', error);
      setLinkedInPost('An error occurred while generating the post.');
    }
  };

  return (
    <div>
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
    </div>
  );
}

export default App;