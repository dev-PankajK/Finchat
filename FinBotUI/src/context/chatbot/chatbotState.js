import ChatbotContext from './chatbotContext'
import { useState, useEffect } from 'react';
const ChatbotState = (props) => {
    const [userMessage, setUserMessage] = useState('');
    const [data, setData] = useState('');
    const [streaming, setStreaming] = useState(false)
    const [messages, setMessages] = useState([
        { type: 'incoming', content: 'Hi There! How can I help you' },
    ]);
    const chatStates = {
        userMessage,
        setUserMessage,
        data,
        setData,
        streaming,
        setStreaming,
        messages,
        setMessages,
      };
    return (
        <ChatbotContext.Provider value={chatStates}> 
            {props.children}
        </ChatbotContext.Provider>
    )
}

export default ChatbotState;