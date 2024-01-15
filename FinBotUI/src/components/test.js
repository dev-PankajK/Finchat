import { useContext } from "react";
import ChatbotContext from "../context/chatbot/chatbotContext";
import React from 'react'

const Test = () => {
    const chatbotstates  = useContext(ChatbotContext)
  return (
    <div>
        <h1>Hello </h1>
       <p>{chatbotstates.streaming ? 'Streaming is ON' : 'Streaming is OFF'} setting</p>
    </div>
  )
}

export default Test;



