import { useState } from 'react'
import './App.css'

function App() {
  const [message,setMessage] = useState("")

  const [reply,setReply] = useState("")
  async function sendMessage() {
    const response =  await fetch(
      "http://127.0.0.1:8000/chat",
      {
        method:'POST',
        headers : {
          'content-Type':'application/json'
        },
        body : JSON.stringify({
          message:message,
          thread_id : "user1"
        }
        )
      }
    )
    const data = await response.json()
    setReply(data.reply)
    
  }
  return (
    <div> 
      <h1>Zentra</h1>
      <input type= "text" placeholder='enter message' value={message}
       onChange={(e) => setMessage(e.target.value)} />
       <button onClick={sendMessage}>send</button>
       <p>{reply}</p>
    </div>
  )
}

export default App