import React, { useContext } from 'react'
import { useEffect } from 'react';
import '../styles/chatbot.css';  
import ChatbotContext from '../context/chatbot/chatbotContext';
import fetchSse from '../utils/chatbot_utils';
const Chatbot = () => {
    const { userMessage, setUserMessage, data, setData, streaming, setStreaming, messages, setMessages } = useContext(ChatbotContext);
    const serverBaseURL = "http://127.0.0.1:8000"
    const sseEndpoint = `${serverBaseURL}/api/agent/run`
    useEffect(() => {
        console.log("Current Data Updated:", data);
        console.log(`streaming ${streaming}`);
        console.log("Messages:", messages);
    }, [data, messages]);

    const handleInputChange = (event) => {
        if (event.keyCode === 13) {
            // If Enter key is pressed, submit the message
            handleChat();
            setUserMessage('');
        };
    };
    const handleChat = async () => {
        const trimmedMessage = userMessage.trim();
        if (!trimmedMessage) return;
        console.log('User Message:', trimmedMessage);
        setMessages([...messages, { type: 'outgoing', content: trimmedMessage }]);
        //Fetch the data from backend and create the incoming li(streaming li)
        try {
            console.log(localStorage.access_token);
            // Fetch data from the backend
            const body = JSON.stringify({
                                query: userMessage,
                                access_token: localStorage.access_token
                            });
            await fetchSse(sseEndpoint,body,setData,setMessages,setStreaming);
            setData('');
            setUserMessage('');
        } catch (error) {
            console.log("Error fetching data:", error);
        }
    };
    return (
        <>
            <div className='show-chatbot'>
                <button className='chatbot-toggler'>
                    <span className='material-symbols-outlined'>mode_comment</span>
                    <span className='material-symbols-outlined'>close</span>
                </button>
                <div className="chatbot">
                    <header>
                        <span className='material-symbols-outlined'>close</span>
                        <h2>Sample Chatbot</h2>
                    </header>
                    <ul className="chatbox">
                        {messages.map((msg, index) => (
                            <li key={index} className={`chat ${msg.type}`}>
                                {msg.type === 'incoming' ? (
                                    <>
                                        <span className='material-symbols-outlined'>smart_toy</span>
                                        {index === messages.length - 1 && streaming ? (
                                            <p>{data}</p>
                                        ) : (
                                            <p>{msg.content}</p>
                                        )}
                                    </>
                                ) : <p>{msg.content}</p>}
                            </li>
                        ))}
                    </ul>
                    <div className='chat-input'>
                        <textarea placeholder='Enter a message..' value={userMessage} onKeyDown={handleInputChange} onChange={(e) => setUserMessage(e.target.value)} required></textarea>
                        <span id='send-btn' className='material-symbols-outlined' onClick={handleChat}>send</span>
                    </div>
                </div>
            </div>

        </>
    );
};

export default Chatbot;