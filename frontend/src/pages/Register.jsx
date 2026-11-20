import { useState } from "react"
import { Link, useNavigate } from "react-router-dom"
import { useLanguage } from "../context/LanguageContext"

function Register() {
  const [username, setUsername] = useState("")
  const [password, setPassword] = useState("")
  const [message, setMessage] = useState("")

  const navigate = useNavigate()
  const { t } = useLanguage()

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
      setMessage(t("registrationFailed"))
    }
  }

  return (
    <div>
      <h1>{t("register")}</h1>

      <form onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder={t("username")}
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          required
        />

        <input
          type="password"
          placeholder={t("password")}
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />

        <button type="submit">
        {t("register")}
        </button>
      </form>

      {message && <p>{message}</p>}

      <Link to="/login">
        {t("backToLogin")}
      </Link>
    </div>
  )
}

export default Register
