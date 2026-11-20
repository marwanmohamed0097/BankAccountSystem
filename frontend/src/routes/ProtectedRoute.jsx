import { Navigate } from "react-router-dom"
import { useAuth } from "../context/AuthContext"
import { useLanguage } from "../context/LanguageContext"

function ProtectedRoute({ children }) {
  const {
    token,
    loading
  } = useAuth()
  const { t } = useLanguage()

  if (loading) {
    return <p>{t("loading")}</p>
  }

  if (!token) {
    return <Navigate to="/login" replace />
  }

  return children
}

export default ProtectedRoute
