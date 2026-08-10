import ProblemPanel from './components/ProblemPanel'
import CodeEditor from './components/CodeEditor'
import ChatPanel from './components/ChatPanel'

function App() {
  return (

    <div className="app">

      <nav className="navbar">

        <div className="navbar-brand">
          <span className="brand-icon">💡</span>
          <span>HintBot</span>
        </div>

        <div className="navbar-profile">
          <span>R</span>
        </div>

      </nav>

      <div className="workspace">
        <ProblemPanel />
        <CodeEditor />
        <ChatPanel />
      </div>

    </div>

  )
}

export default App