import React, { useState } from 'react';

function TextForm() {
  const [inputText, setInputText] = useState('');
  const [generatedPost, setGeneratedPost] = useState('');
  const [error, setError] = useState('');

  const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setGeneratedPost('');

    try {
      const response = await fetch(`${API_URL}/api/generate-post`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text: inputText }),  // Adjust to match backend expectations
      });

      if (!response.ok) {
        const errorMsg = await response.text();
        throw new Error(errorMsg || 'An error occurred');
      }

      const result = await response.text();
      setGeneratedPost(result);
    } catch (error) {
      console.error('Error:', error.message, error);
      setError(error.message);
    }
  };

  return (
    <div>
      <form onSubmit={handleSubmit}>
        <textarea
          value={inputText}
          onChange={(e) => setInputText(e.target.value)}
          placeholder="Enter your text here"
          rows="4"
          required
        />
        <button type="submit">Generate Post</button>
      </form>
      {error && <p style={{ color: 'red' }}>{error}</p>}
      {generatedPost && (
        <div>
          <h2>Generated Post:</h2>
          <textarea
            value={generatedPost}
            readOnly
            rows="10"
          />
        </div>
      )}
    </div>
  );
}

export default TextForm;