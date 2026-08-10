function ProblemPanel() {
  return (
    <section className="problem-panel">
      <h2>Two Sum</h2>

      <p>
        Given an array of integers and a target value,
        return the indices of two numbers that add up to
        the target.
      </p>

      <h3>Example</h3>

      <pre>
{`Input:
nums = [2, 7, 11, 15]
target = 9

Output:
[0, 1]`}
      </pre>

      <h3>Constraints</h3>

      <ul>
        <li>2 ≤ nums.length ≤ 10⁴</li>
        <li>-10⁹ ≤ nums[i] ≤ 10⁹</li>
        <li>Only one valid answer exists.</li>
      </ul>
    </section>
  )
}

export default ProblemPanel