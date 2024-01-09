import { fetchEventSource } from "@microsoft/fetch-event-source";


/**
 * This fetchSse is only uses for openai streaming task to use it for another task user need to modify it
 * Fetch data using Server-Sent Events (SSE).
 * @param {string} endpoint - The API endpoint URL.
 * @param {object} body - The request body as an object.
 * @param {function} setData - The function to update data in the component's state.
 * @param {function} setMessages - The function to update messages in the component's state.
 * @param {function} setStreaming - The function to update the streaming state in the component's state.
 * @returns {Promise<void>} - A promise that resolves with no value upon successful execution.
 */

const fetchSse = async (endpoint,body,setData,setMessages,setStreaming) => {
    setMessages((prevMessages) => [...prevMessages, { type: 'incoming', content: '' }])
    try {
        await fetchEventSource(endpoint, {
            method: "POST",
            headers: {
                'Content-Type': 'application/json',
                Accept: "text/event-stream",
            },
            body: body,
            onopen(res) {
                if (res.ok && res.status === 200) {
                    console.log("Connection made ", res);
                    setStreaming(true)
                    // setMessages((prevMessages) => [...prevMessages, { type: 'incoming', content: '' }])
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
                    return prevData;
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

export default fetchSse;