import Editor from '@monaco-editor/react'
import { useState } from 'react'

function CodeEditor() {
  const [code, setCode] = useState(
`def two_sum(nums, target):
    # Write your solution here
    pass`
  )

  function handleRun() {
    console.log('Code:', code)
  }

  return (
    <section className="editor-panel">

      <div className="editor-header">
        <span>Python</span>

        <button onClick={handleRun}>
          Run
        </button>
      </div>

      <div className="editor">
        <Editor
          height="100%"
          defaultLanguage="python"
          value={code}
          onChange={(value) => setCode(value || '')}
          theme="vs-dark"
          options={{
            minimap: { enabled: false },
            fontSize: 14,
            padding: { top: 15 },
            automaticLayout: true,
          }}
        />
      </div>

      <div className="output">
        <h3>Output</h3>
        <p>Run your code to see the output.</p>
      </div>

    </section>
  )
}

export default CodeEditor