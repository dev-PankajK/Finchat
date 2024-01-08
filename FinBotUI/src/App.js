import './App.css';
import Chatbot from './components/chatbot';
import ChatbotState from './context/chatbot/chatbotState';
function App() {
  return (
    <>
    <ChatbotState>
    <Chatbot />
    </ChatbotState>

    </>
  );
}

export default App;
