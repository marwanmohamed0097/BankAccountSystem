import {
  Navigate,
  Route,
  Routes
} from "react-router-dom"

import { useLanguage } from "./context/LanguageContext"
import Login from "./pages/Login"
import Register from "./pages/Register"
import Dashboard from "./pages/Dashboard"
import Accounts from "./pages/Accounts"
import ProtectedRoute from "./routes/ProtectedRoute"

function App() {
  const { language, setLanguage, t } = useLanguage()

  return (
    <>
      <div style={{ display: "flex", justifyContent: "flex-end", alignItems: "center", gap: "8px", padding: "12px" }}>
        <label htmlFor="language-select">{t("language")}</label>
        <select
          id="language-select"
          value={language}
          onChange={(event) => setLanguage(event.target.value)}
          aria-label={t("language")}
        >
          <option value="en">English</option>
          <option value="de">Deutsch</option>
          <option value="ar">العربية</option>
        </select>
      </div>

      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route
          path="/dashboard"
          element={
            <ProtectedRoute>
              <Dashboard />
            </ProtectedRoute>
          }
        />
        <Route
          path="/accounts"
          element={
            <ProtectedRoute>
              <Accounts />
            </ProtectedRoute>
          }
        />
        <Route path="/" element={<Navigate to="/dashboard" replace />} />
      </Routes>
    </>
  )
}

export default App
