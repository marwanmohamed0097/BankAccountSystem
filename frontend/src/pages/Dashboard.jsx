import { useNavigate } from "react-router-dom"
import { useAuth } from "../context/AuthContext"
import { useLanguage } from "../context/LanguageContext"

function Dashboard() {
  const {
    user,
    logout
  } = useAuth()

  const navigate = useNavigate()
  const { t } = useLanguage()

  function handleLogout() {
    logout()
    navigate("/login")
  }

  return (
    <div>
      <h1>{t("dashboard")}</h1>

      <h2>
        {t("welcome", { username: user?.username })}
      </h2>

      <p>
        {t("role", { role: user?.role })}
      </p>

      <button onClick={() => navigate("/accounts")}>
        {t("myAccounts")}
      </button>

      <button onClick={handleLogout}>
        {t("logout")}
      </button>
    </div>
  )
}

export default Dashboard
