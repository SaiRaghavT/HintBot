import { useState } from 'react'
import ReactMarkdown from 'react-markdown'
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

            console.log("BACKEND RESPONSE:", response)
            console.log("TYPE:", typeof response)

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

                {messages.length === 0 && (
                    <div className="welcome">

                        <div className="welcome-icon">
                            💡
                        </div>

                        <h2>Hi, I'm HintBot</h2>

                        <p>
                            Stuck on a problem? Ask me for a hint.
                            I'll help you think through it instead of
                            giving you the answer straight away.
                        </p>

                        <div className="suggestions">
                            <button
                                onClick={() => setMessage('Help me with DSA')}
                            >
                                🧠 DSA
                            </button>

                            <button
                                onClick={() => setMessage('Help me with coding')}
                            >
                                💻 Coding
                            </button>

                            <button
                                onClick={() => setMessage('Explain this concept')}
                            >
                                📚 Concepts
                            </button>
                        </div>

                    </div>
                )}

                {messages.map((msg, index) => {
                    console.log(
                        'MSG:',
                        msg,
                        'CONTENT TYPE:',
                        typeof msg.content
                    )

                    return (
                        <div
                            key={index}
                            className={`message ${msg.role === 'user'
                                    ? 'user-message'
                                    : 'bot-message'
                                }`}
                        >

                            {msg.role === 'bot' && (
                                <div className="avatar">
                                    H
                                </div>
                            )}

                            <div className="bubble">
                                {msg.role === 'bot' ? (
                                    <ReactMarkdown>
                                        {String(msg.content)}
                                    </ReactMarkdown>
                                ) : (
                                    <p>{String(msg.content)}</p>
                                )}
                            </div>

                        </div>
                    )
                })}

            </div>

            <div className="input-area">

                <input
                    type="text"
                    placeholder="Ask HintBot for a hint..."
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