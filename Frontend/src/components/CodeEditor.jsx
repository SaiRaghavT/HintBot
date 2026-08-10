import Editor from '@monaco-editor/react'
import { useState } from 'react'
import { runCode } from '../services/api'

function CodeEditor() {
    const [code, setCode] = useState(
        `def two_sum(nums, target):
    # Write your solution here
    pass`
    )

    const [output, setOutput] = useState('')
    const [isRunning, setIsRunning] = useState(false)

    async function handleRun() {
        console.log("RUN CLICKED")
        console.log("CODE:", code)

        setIsRunning(true)
        setOutput('Running...')

        try {
            console.log("Sending request to /api/run...")

            const result = await runCode(code)

            console.log("BACKEND RESULT:", result)

            if (result.error) {
                setOutput(result.error)
            } else {
                setOutput(result.output || 'No output')
            }
        } catch (error) {
            console.error("RUN ERROR:", error)
            setOutput(error.message)
        }
        finally {
            setIsRunning(false)
        }
    }

    return (
        <section className="editor-panel">

            <div className="editor-header">
                <span>Python</span>

                <button
                    onClick={handleRun}
                    disabled={isRunning}
                >
                    {isRunning ? 'Running...' : 'Run'}
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
                        padding: {
                            top: 15,
                        },
                        automaticLayout: true,
                    }}
                />
            </div>

            <div className="output">
                <h3>Output</h3>

                <pre>{output}</pre>
            </div>

        </section>
    )
}

export default CodeEditor