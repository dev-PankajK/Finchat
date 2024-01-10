import React, { useState } from 'react'
import axios from 'axios';
import Chatbot from './chatbot';

const Login = () => {
    const [isLoggedIn,setLoggedIn] = useState(false);
    const [credentials, setCredentials] = useState({username:"",password:""});
    const handleLogin = async (e) => {
        console.log("Logged in..");
        e.preventDefault();
        try {
            const response = await axios.post('http://localhost:8000/api/auth/login', credentials);
            console.log(response.data);
            setLoggedIn(true);
            localStorage.setItem('access_token',response.data.access_token)

        } catch (error) {
            console.error('Login failed:', error.message);
        }
    }
    if (isLoggedIn) {
        return <Chatbot />;
    }
    const formOnChange = (e)=>{
        setCredentials({...credentials,[e.target.name]:e.target.value})
    }

  return (
    <div className="container mt-5">
    <form>
        <div className="form-group">
            <label htmlFor="exampleInputEmail1">Email address</label>
            <input
                name='username'
                type="email"
                className="form-control"
                id="exampleInputEmail1"
                aria-describedby="emailHelp"
                placeholder="Enter email"
                value={credentials.username}
                onChange={formOnChange}
            />
            <small id="emailHelp" className="form-text text-muted">
                We'll never share your email with anyone else.
            </small>
        </div>
        <div className="form-group">
            <label htmlFor="exampleInputPassword1">Password</label>
            <input
            name='password'
                type="password"
                className="form-control"
                id="exampleInputPassword1"
                placeholder="Password"
                value={credentials.password}
                onChange={formOnChange}
            />
        </div>
        <div className="form-group form-check">
            <input
                type="checkbox"
                className="form-check-input"
                id="exampleCheck1"
            />
            <label className="form-check-label" htmlFor="exampleCheck1">
                Check me out
            </label>
        </div>
        <button
            type="submit"
            className="btn btn-primary"
            onClick={handleLogin}
        >
            Submit
        </button>
    </form>
</div>
  )
}

export default Login;
