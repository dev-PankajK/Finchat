import './App.css';
import Chatbot from './components/chatbot';
import Login from './components/Login';
import ChatbotState from './context/chatbot/chatbotState';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';

const App = () => {
  return (
    <ChatbotState>
      <Router>
          <Routes>
              <Route path="/" element={<Login />} />
              {/* Add other routes as needed */}
          </Routes>
      </Router>
      </ChatbotState>
  );
};

export default App;
// function App() {
//   return (
//     <>
//       <ChatbotState>
//         <Router>
//           <Routes>

//             <Route path="/" element={Login} />
//             {/* <Chatbot /> */}

//           </Routes>
//         </Router>
//         {/* <h1>Hello</h1> */}
//       </ChatbotState>
//     </>
//   );
// }

// export default App;
