import React, { useState } from 'react';

function QueryForm() {
  const [query, setQuery] = useState('');
  const [response, setResponse] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setResponse('');
    setLoading(true);
    try {
      const res = await fetch('https://<web-browser-query-agent.onrender.com>/query', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query }),
      });

      const data = await res.json();
      setResponse(data.answer || 'No result found.');
    } catch (err) {
      setResponse('❌ Error fetching data. Please try again later.');
    }
    setLoading(false);
  };

  return (
    <div>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Enter your query..."
        />
        <button type="submit" disabled={loading}>
          {loading ? 'Searching...' : 'Submit'}
        </button>
      </form>
      {response && <pre>{response}</pre>}
    </div>
  );
}

export default QueryForm;
