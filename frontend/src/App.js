import React, { useState } from 'react';
import ChatBubble from './ChatBubble';
import ChatInput from './ChatInput';

function App() {
  const [messages, setMessages] = useState([
    { from: 'bot', text: 'Hello, I am MentorBot. How can I help you today?' }
  ]);

  const sendMessage = async (query, codeSnippet) => {
    const userMessage = { from: 'user', text: query };
    setMessages(prev => [...prev, userMessage]);

    const response = await fetch('http://localhost:8000/ask', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ query, code_snippet: codeSnippet })
    });
    const data = await response.json();
    const botMessage = { from: 'bot', text: data.answer };
    setMessages(prev => [...prev, botMessage]);
    if (data.code_result && data.code_result.trim() !== '') {
      const codeResultMessage = { from: 'bot', text: `Code Output:\n${data.code_result}` };
      setMessages(prev => [...prev, codeResultMessage]);
    }
  };

  const containerStyle = {
    display: 'flex',
    flexDirection: 'column',
    width: '60%',
    margin: 'auto',
    marginTop: '50px',
    border: '1px solid #ccc',
    padding: '20px'
  };

  const messagesContainerStyle = {
    display: 'flex',
    flexDirection: 'column'
  };

  return (
    <div style={containerStyle}>
      <h1>MentorBot</h1>
      <div style={messagesContainerStyle}>
        {messages.map((m, i) => <ChatBubble key={i} text={m.text} from={m.from} />)}
      </div>
      <ChatInput onSend={sendMessage} />
    </div>
  );
}

export default App;
