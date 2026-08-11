function ProblemPanel({ problem }) {
    return (
        <section className="problem-panel">

            <div className="problem-top">
                <span>Problem {problem.frontend_id}</span>

                <span className="difficulty">
                    {problem.difficulty}
                </span>
            </div>

            <h2>{problem.title}</h2>

            <div className="topics">
                {problem.topics.map((topic, index) => (
                    <span key={index}>
                        {topic}
                    </span>
                ))}
            </div>

            <div className="problem-description">
                <p>{problem.description}</p>
            </div>

            <div className="examples">

                <h3>Examples</h3>

                {problem.examples.map((example, index) => (
                    <div className="example" key={index}>

                        <strong>
                            Example {example.example_num || index + 1}
                        </strong>

                        <p>
                            {example.example_text}
                        </p>

                    </div>
                ))}

            </div>

            <div className="constraints">

                <h3>Constraints</h3>

                <ul>
                    {problem.constraints.map((constraint, index) => (
                        <li key={index}>
                            {constraint}
                        </li>
                    ))}
                </ul>

            </div>

        </section>
    )
}

export default ProblemPanel