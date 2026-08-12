import { useState } from 'react'
import ReactMarkdown from 'react-markdown'

import { sendMessage } from '../services/api'


function ChatPanel({
  sessionId,
  problem,
  code,
  output,
  executionError
}) {

  const [message, setMessage] = useState('')
  const [messages, setMessages] = useState([])
  const [isSending, setIsSending] = useState(false)

  // Backend is the source of truth
  const [hintsUsed, setHintsUsed] = useState(0)
  const [maxHints, setMaxHints] = useState(4)


  async function handleSend() {

    // Don't send empty messages
    if (!message.trim()) return

    // Don't allow requests after all hints are used
    if (hintsUsed >= maxHints) return


    const userMessage = message


    // Show user's message immediately
    setMessages((prev) => [
      ...prev,
      {
        role: 'user',
        content: userMessage,
      },
    ])


    setMessage('')
    setIsSending(true)


    try {

      console.log('CHAT CONTEXT:', {
        sessionId,
        problemId: problem?.frontend_id,
        code,
        output,
        executionError,
      })


      const response = await sendMessage({

        sessionId: sessionId,

        problemId: problem?.frontend_id,

        message: userMessage,

        code: code,

        executionOutput: output,

        executionError: executionError,

      })


      console.log('CHAT RESPONSE:', response)


      // Backend controls the hint count
      setHintsUsed(response.hints_used)
      setMaxHints(response.max_hints)


      // Add only the AI response
      setMessages((prev) => [
        ...prev,
        {
          role: 'bot',
          content: response.response,
        },
      ])


    } catch (error) {

      console.error('CHAT ERROR:', error)


      setMessages((prev) => [
        ...prev,
        {
          role: 'bot',
          content: 'Sorry, something went wrong.',
        },
      ])


    } finally {

      setIsSending(false)

    }

  }


  const hintsExhausted = hintsUsed >= maxHints


  return (

    <section className="chat-panel">


      {/* =========================
          HEADER
      ========================= */}

      <div className="chat-header">

        <h2>
          💡 HintBot
        </h2>

        <span>
          ● Online
        </span>

      </div>


      {/* =========================
          HINT INFORMATION
      ========================= */}

      <div className="hint-info">

        <div className="hint-counter">

          <span>
            Hints used
          </span>

          <strong>
            {hintsUsed} / {maxHints}
          </strong>

        </div>


        <p>
          HintBot helps you solve the problem
          without giving away the solution.
        </p>


        <ul>

          <li>
            Hints become more specific as you ask.
          </li>

          <li>
            Each message uses one hint.
          </li>

          <li>
            HintBot guides you without giving the solution.
          </li>

        </ul>

      </div>


      {/* =========================
          MESSAGES
      ========================= */}

      <div className="chat-content">


        {messages.length === 0 && (

          <div className="welcome">

            <div className="welcome-icon">
              💡
            </div>


            <h2>
              Need a hint?
            </h2>


            <p>
              Ask HintBot when you're stuck.
              Hints become progressively more
              specific as you ask.
            </p>

          </div>

        )}


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

                <p>
                  {String(msg.content)}
                </p>

              )}

            </div>

          </div>

        ))}


        {isSending && (

          <div className="message bot-message">

            <div className="avatar">
              H
            </div>


            <div className="bubble">
              Thinking...
            </div>

          </div>

        )}


      </div>


      {/* =========================
          INPUT
      ========================= */}

      <div className="chat-input">


        <input

          type="text"

          placeholder={
            hintsExhausted
              ? 'No hints remaining'
              : 'Ask HintBot for a hint...'
          }

          value={message}

          disabled={
            isSending || hintsExhausted
          }

          onChange={(e) => {
            setMessage(e.target.value)
          }}

          onKeyDown={(e) => {

            if (
              e.key === 'Enter' &&
              !isSending &&
              !hintsExhausted
            ) {
              handleSend()
            }

          }}

        />


        <button

          onClick={handleSend}

          disabled={
            isSending || hintsExhausted
          }

        >

          {isSending
            ? '...'
            : hintsExhausted
              ? 'No Hints'
              : 'Send'
          }

        </button>


      </div>


    </section>

  )
}


export default ChatPanel