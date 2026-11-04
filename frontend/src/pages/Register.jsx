import { useState } from "react"
import { Link, useNavigate } from "react-router-dom"

function Register() {
  const [username, setUsername] = useState("")
  const [password, setPassword] = useState("")
  const [message, setMessage] = useState("")

  const navigate = useNavigate()

  async function handleSubmit(event) {
    event.preventDefault()

    const response = await fetch(
      "http://127.0.0.1:8000/register",
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          username,
          password
        })
      }
    )

    if (response.ok) {
      navigate("/login")
    } else {
      setMessage("Registration failed.")
    }
  }

  return (
    <div>
      <h1>Register</h1>

      <form onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          required
        />

        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />

        <button type="submit">
          Register
        </button>
      </form>

      {message && <p>{message}</p>}

      <Link to="/login">
        Back to Login
      </Link>
    </div>
  )
}

export default Register
