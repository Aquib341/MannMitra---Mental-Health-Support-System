// frontend/src/components/ChatInterface.js
import React, { useState, useRef, useEffect } from 'react';
import { apiService } from '../services/api';

const ChatInterface = ({ user }) => {
  const [messages, setMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [useVoice, setUseVoice] = useState(false);
  const messagesEndRef = useRef(null);
  const audioRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const sendMessage = async () => {
    if (!inputMessage.trim() || isLoading) return;

    const userMessage = inputMessage;
    setInputMessage('');
    setMessages(prev => [...prev, { type: 'user', content: userMessage }]);
    setIsLoading(true);

    try {
      const response = await apiService.sendMessage({
        user_id: user.uid,
        message: userMessage,
        voice_response: useVoice
      });

      setMessages(prev => [...prev, { 
        type: 'ai', 
        content: response.response,
        mood: response.mood
      }]);

      // Play audio if voice response is available
      if (useVoice && response.speech_data) {
        const audio = new Audio(`data:audio/mp3;base64,${response.speech_data}`);
        audio.play();
      }
    } catch (error) {
      console.error('Error sending message:', error);
      setMessages(prev => [...prev, { 
        type: 'ai', 
        content: 'Sorry, I encountered an error. Please try again.',
        isError: true
      }]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      sendMessage();
    }
  };

  return (
    <div className="chat-interface">
      <h2>Chat with MannMitra</h2>
      
      <div className="chat-messages">
        {messages.map((message, index) => (
          <div key={index} className={`message ${message.type} ${message.isError ? 'error' : ''}`}>
            <div className="message-content">
              {message.content}
              {message.mood && <span className="mood-badge">{message.mood}</span>}
            </div>
          </div>
        ))}
        {isLoading && (
          <div className="message ai">
            <div className="message-content typing">
              <span className="typing-dots">
                <span>.</span>
                <span>.</span>
                <span>.</span>
              </span>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      <div className="chat-input">
        <input
          type="text"
          value={inputMessage}
          onChange={(e) => setInputMessage(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder="Type your message..."
          disabled={isLoading}
        />
        <button onClick={sendMessage} disabled={isLoading || !inputMessage.trim()}>
          {isLoading ? 'Sending...' : 'Send'}
        </button>
        <label className="voice-toggle">
          <input
            type="checkbox"
            checked={useVoice}
            onChange={(e) => setUseVoice(e.target.checked)}
          />
          Voice Response
        </label>
      </div>

      <audio ref={audioRef} style={{ display: 'none' }} />
    </div>
  );
};

export default ChatInterface;