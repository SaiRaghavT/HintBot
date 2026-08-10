import { useState } from 'react'
import { sendMessage } from '../services/api'

function Chat() {
  const [message, setMessage] = useState('')
  const [messages, setMessages] = useState([])

  async function handleSend() {
    if (!message.trim()) return

    const userMessage = message

    setMessages((prev) => [
      ...prev,
      {
        role: 'user',
        content: userMessage,
      },
    ])

    setMessage('')

    try {
      const response = await sendMessage(userMessage)

      setMessages((prev) => [
        ...prev,
        {
          role: 'bot',
          content: response,
        },
      ])
    } catch (error) {
      console.error(error)

      setMessages((prev) => [
        ...prev,
        {
          role: 'bot',
          content: 'Sorry, something went wrong.',
        },
      ])
    }
  }

  return (
    <main className="chat">

      <div className="messages">

        {messages.map((msg, index) => (
          <div
            key={index}
            className={`message ${
              msg.role === 'user'
                ? 'user-message'
                : 'bot-message'
            }`}
          >

            {msg.role === 'bot' && (
              <div className="avatar">H</div>
            )}

            <div className="bubble">
              <p>{msg.content}</p>
            </div>

          </div>
        ))}

      </div>

      <div className="input-area">

        <input
          type="text"
          placeholder="Ask HintBot anything..."
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === 'Enter') {
              handleSend()
            }
          }}
        />

        <button onClick={handleSend}>
          Send
        </button>

      </div>

    </main>
  )
}

export default Chat