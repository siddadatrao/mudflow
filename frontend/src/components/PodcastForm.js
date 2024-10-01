import React, { useState } from 'react';
import './PodcastForm.css';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000'; // Fallback to localhost if env variable is not set

function TextForm() {
  const [inputText, setInputText] = useState('');
  const [generatedPost, setGeneratedPost] = useState('');
  const [loading, setLoading] = useState(false); // Loading state

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);  // Set loading state to true

    try {
      const response = await fetch(`${API_URL}/api/generate-post`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text: inputText }),
      });

      const result = await response.json();
      setGeneratedPost(result.generated_post);
    } catch (err) {
      console.error('Error:', err);
    } finally {
      setLoading(false);  // Reset loading state
    }
  };

  return (
    <div className="podcast-form-container">
      <div className="card">
        <h2 className="form-title">🎙️ Medical Context Linkedin Posts</h2>
        <form onSubmit={handleSubmit} className="form">
          <textarea
            className="input"
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
            placeholder="Enter podcast details..."
            rows="6"
            required
          />
          {!loading && ( // Conditionally render the button only when not loading
            <button
              type="submit"
              className="button"
            >
              📝 Generate Post
            </button>
          )}
        </form>
        {loading && <span className="loader"></span>} {/* Show loader when loading */}
        {generatedPost && (
          <div className="output">
            <h3 className="output-title">Generated LinkedIn Post:</h3>
            <div className="post-preview">{generatedPost}</div>
          </div>
        )}
      </div>
    </div>
  );
}

export default TextForm;