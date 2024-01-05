import React from 'react'
import { useState, useEffect } from 'react';
import '../styles/chatbot.css';  
import { fetchEventSource } from "@microsoft/fetch-event-source";
const Chatbot = () => {
    const [userMessage, setUserMessage] = useState('');
    const [data, setData] = useState('');
    const [streaming, setStreaming] = useState(false)
    const [messages, setMessages] = useState([
        { type: 'incoming', content: 'Hi There! How can I help you' },
    ]);
    const serverBaseURL = "http://127.0.0.1:8000"
    const fetchData = async () => {
        try {
            const response = await fetchEventSource(`${serverBaseURL}/api/agent/openai_streaming`, {
                method: "POST",
                headers: {
                    'Content-Type': 'application/json',
                    Accept: "text/event-stream",
                },
                body: JSON.stringify({
                    message: userMessage
                }),
                onopen(res) {
                    if (res.ok && res.status === 200) {
                        console.log("Connection made ", res);
                        setStreaming(true)
                        setMessages((prevMessages) => [...prevMessages, { type: 'incoming', content: '' }])
                    } else if (res.status >= 400 && res.status < 500 && res.status !== 429) {
                        console.log("Client-side error ", res);
                    }
                },
                onmessage(event) {
                    setData((prevData) => prevData + event.data);
                },
                onclose() {
                    setStreaming(false)
                    console.log("Connection closed by the server");
                    setData((prevData) => {
                        setMessages((prevMessages) => {
                            prevMessages.pop();
                            return [...prevMessages, { type: 'incoming', content: prevData }]})
                        // setMessages((prevMessages) => [...prevMessages, { type: 'incoming', content: prevData }])
                        return prevData; // Return the value to update the state
                    });
                    console.log("Finishing Everythin.....");
                },
                onerror(err) {
                    console.log("There was an error from server", err);
                },
            });
        } catch (error) {
            console.log("There was an error from the server", error);
        }
    };
    useEffect(() => {
        console.log("Current Data Updated:", data);
        console.log(`streaming ${streaming}`);
        console.log("Messages:", messages);
    }, [data, messages]);

    const handleInputChange = (event) => {
        console.log(event.keyCode);
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
            // Fetch data from the backend
            await fetchData();
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