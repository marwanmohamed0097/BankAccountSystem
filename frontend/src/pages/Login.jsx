import { useState } from "react"
import { useNavigate } from "react-router-dom"
import { useAuth } from "../context/AuthContext"
import { useLanguage } from "../context/LanguageContext"

function Login() {
  const [username, setUsername] = useState("")
  const [password, setPassword] = useState("")
  const [error, setError] = useState("")
  const [loading, setLoading] = useState(false)

  const navigate = useNavigate()
  const { login } = useAuth()
  const { t } = useLanguage()

  async function handleSubmit(event) {
    event.preventDefault()

    setError("")
    setLoading(true)

    try {
      await login(username, password)
      navigate("/dashboard")
    } catch {
      setError(t("invalidCredentials"))
    } finally {
      setLoading(false)
    }
  }

  return (
    <div>
      <h1>{t("bankAccountSystem")}</h1>
      <h2>{t("login")}</h2>

      <form onSubmit={handleSubmit}>
        <div>
          <label>{t("username")}</label>

          <input
            type="text"
            value={username}
            onChange={(event) =>
              setUsername(event.target.value)
            }
            required
          />
        </div>

        <div>
          <label>{t("password")}</label>

          <input
            type="password"
            value={password}
            onChange={(event) =>
              setPassword(event.target.value)
            }
            required
          />
        </div>

        {error && <p>{error}</p>}

        <button
          type="submit"
          disabled={loading}
        >
          {loading ? t("loggingIn") : t("login")}
        </button>
      </form>
    </div>
  )
}

export default Login
