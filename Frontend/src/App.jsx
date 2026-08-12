import { useEffect, useState } from 'react'

import ProblemPanel from './components/ProblemPanel'
import CodeEditor from './components/CodeEditor'
import ChatPanel from './components/ChatPanel'

import { getCurrentProblem } from './services/api'


function App() {

  // New session every time the page is refreshed
  const [sessionId] = useState(() => crypto.randomUUID())

  console.log('SESSION ID:', sessionId)

  const [problem, setProblem] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  const [code, setCode] = useState('')
  const [output, setOutput] = useState('')
  const [executionError, setExecutionError] = useState(null)


  useEffect(() => {

    async function loadProblem() {

      try {

        const data = await getCurrentProblem()

        console.log('CURRENT PROBLEM:', data)

        setProblem(data)

        // Load starter code from backend
        setCode(data.starter_code || '')

      } catch (error) {

        console.error(error)

        setError('Failed to load problem.')

      } finally {

        setLoading(false)

      }
    }

    loadProblem()

  }, [])


  if (loading) {
    return <div>Loading problem...</div>
  }


  if (error) {
    return <div>{error}</div>
  }


  return (

    <div className="app">

      <nav className="navbar">

        <div className="navbar-brand">

          <span className="brand-icon">
            💡
          </span>

          <span>
            HintBot
          </span>

        </div>


        <div className="navbar-profile">

          <span>
            R
          </span>

        </div>

      </nav>


      <div className="workspace">

        <ProblemPanel
          problem={problem}
        />


        <CodeEditor
          code={code}
          setCode={setCode}
          output={output}
          setOutput={setOutput}
          setExecutionError={setExecutionError}
        />


        <ChatPanel
          sessionId={sessionId}
          problem={problem}
          code={code}
          output={output}
          executionError={executionError}
        />

      </div>

    </div>

  )
}


export default App