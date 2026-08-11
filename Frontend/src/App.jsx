import { useEffect, useState } from 'react'

import ProblemPanel from './components/ProblemPanel'
import CodeEditor from './components/CodeEditor'
import ChatPanel from './components/ChatPanel'

import { getCurrentProblem } from './services/api'


function App() {

    const [problem, setProblem] = useState(null)
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState('')


    useEffect(() => {

        async function loadProblem() {

            try {

                const data = await getCurrentProblem()

                console.log('CURRENT PROBLEM:', data)

                setProblem(data)

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
                    <span className="brand-icon">💡</span>
                    <span>HintBot</span>
                </div>

                <div className="navbar-profile">
                    <span>R</span>
                </div>

            </nav>


            <div className="workspace">

                <ProblemPanel
                    problem={problem}
                />

                <CodeEditor
                    problem={problem}
                />

                <ChatPanel />

            </div>

        </div>

    )
}


export default App