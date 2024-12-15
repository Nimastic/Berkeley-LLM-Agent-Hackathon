import React from 'react';

function ChatBubble({ text, from }) {
  const bubbleStyle = {
    maxWidth: '60%',
    padding: '10px',
    borderRadius: '10px',
    margin: '5px 0',
    backgroundColor: from === 'user' ? '#DCF8C6' : '#FFF',
    alignSelf: from === 'user' ? 'flex-end' : 'flex-start',
    border: '1px solid #ccc'
  };
  return <div style={bubbleStyle}>{text}</div>;
}

export default ChatBubble;
