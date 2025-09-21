// frontend/src/components/AnonymousChat.js
import React, { useState, useEffect, useRef } from 'react';
import { apiService } from '../services/api';
// In each component file, make sure you have the import at the top:
import './AnonymousChat.css';

const AnonymousChat = ({ user }) => {
  const [messages, setMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState('');
  const [roomId, setRoomId] = useState('');
  const [isConnected, setIsConnected] = useState(false);
  const ws = useRef(null);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const joinChat = async () => {
    try {
      const response = await apiService.joinChat(user.uid);
      setRoomId(response.room_id);
      connectWebSocket(response.room_id);
    } catch (error) {
      console.error('Error joining chat:', error);
    }
  };

  const connectWebSocket = (roomId) => {
    ws.current = new WebSocket(`ws://localhost:8000/ws/chat/${roomId}`);
    
    ws.current.onopen = () => {
      setIsConnected(true);
      console.log('Connected to chat room');
    };
    
    ws.current.onmessage = (event) => {
      const data = JSON.parse(event.data);
      setMessages(prev => [...prev, data]);
    };
    
    ws.current.onclose = () => {
      setIsConnected(false);
      console.log('Disconnected from chat room');
    };
  };

  const sendMessage = () => {
    if (!inputMessage.trim() || !isConnected) return;

    const messageData = {
      user_id: user.uid,
      message: inputMessage,
      timestamp: new Date().toISOString()
    };

    ws.current.send(JSON.stringify(messageData));
    setInputMessage('');
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      sendMessage();
    }
  };

  return (
    <div className="anonymous-chat">
      <h2>Anonymous Community Chat</h2>
      
      {!roomId ? (
        <div className="join-chat">
          <p>Join a supportive community chat room</p>
          <button onClick={joinChat} className="btn btn-primary">
            Join Chat Room
          </button>
        </div>
      ) : (
        <div className="chat-room">
          <div className="chat-status">
            Status: {isConnected ? 'Connected' : 'Disconnected'}
            {roomId && <span className="room-id">Room: {roomId}</span>}
          </div>
          
          <div className="chat-messages">
            {messages.map((message, index) => (
              <div key={index} className="chat-message">
                <span className="user">Anonymous:</span>
                <span className="content">{message.message}</span>
                <span className="time">
                  {new Date(message.timestamp).toLocaleTimeString()}
                </span>
              </div>
            ))}
            <div ref={messagesEndRef} />
          </div>

          <div className="chat-input">
            <input
              type="text"
              value={inputMessage}
              onChange={(e) => setInputMessage(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Type your message..."
              disabled={!isConnected}
            />
            <button 
              onClick={sendMessage} 
              disabled={!isConnected || !inputMessage.trim()}
            >
              Send
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default AnonymousChat;