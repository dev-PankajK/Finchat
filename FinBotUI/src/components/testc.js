import React from 'react'
import { useState } from 'react';
import { fetchEventSource } from "@microsoft/fetch-event-source";

const Teste = () => {
    const [data, setData] = useState('Hello');
    const serverBaseURL = "http://localhost:8000"
    const fetchData = async () => {
        try {
          const response = await fetchEventSource(`${serverBaseURL}/openai_streaming`, {
            method: "POST",
            headers: {
              'Content-Type': 'application/json',
              Accept: "text/event-stream",
            },
            body: JSON.stringify({
              message: "Getting started"
            }),
            onopen(res) {
              if (res.ok && res.status === 200) {
                console.log("Connection made ", res);
              } else if (res.status >= 400 && res.status < 500 && res.status !== 429) {
                console.log("Client-side error ", res);
              }
            },
            onmessage(event) {
              setData((prevData) => prevData+event.data);
            },
            onclose() {
              console.log("Connection closed by the server");
            },
            onerror(err) {
              console.log("There was an error from server", err);
            },
          });
    
          if (response.ok && response.status === 200) {
            console.log("Connection made ", response);
          } else if (response.status >= 400 && response.status < 500 && response.status !== 429) {
            console.log("Client-side error ", response);
          }
        } catch (error) {
          console.log("There was an error from the server", error);
        }
      };
    
    const handleClick = () => {
        alert('Button clicked!');
        fetchData();

    };
    const handleOnchange = () => {
        console.log("Text Area changed");
    };
    // onChange={handleOnchange}
    return (<div>
        <textarea className="form-control" value={data} id='myBox' rows="10"></textarea>
        <input className="btn btn-primary" type="submit" onClick={handleClick} value="Submit" />
    </div>);
};


export default Teste;
