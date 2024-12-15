import React, { useState } from 'react';

function ChatInput({ onSend }) {
  const [query, setQuery] = useState('');
  const [codeSnippet, setCodeSnippet] = useState('');

  const handleSend = () => {
    onSend(query, codeSnippet);
    setQuery('');
    setCodeSnippet('');
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', marginTop: '10px' }}>
      <textarea
        rows={3}
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="Ask a question..."
        style={{ marginBottom: '5px' }}
      />
      <textarea
        rows={3}
        value={codeSnippet}
        onChange={(e) => setCodeSnippet(e.target.value)}
        placeholder="Optional: Paste Python code to run"
        style={{ marginBottom: '5px' }}
      />
      <button onClick={handleSend}>Send</button>
    </div>
  );
}

export default ChatInput;
