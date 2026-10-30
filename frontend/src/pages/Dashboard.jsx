import { useNavigate } from "react-router-dom"
import { useAuth } from "../context/AuthContext"

function Dashboard() {
  const {
    user,
    logout
  } = useAuth()

  const navigate = useNavigate()

  function handleLogout() {
    logout()
    navigate("/login")
  }

  return (
    <div>
      <h1>Dashboard</h1>

      <h2>
        Welcome {user?.username}
      </h2>

      <p>
        Role: {user?.role}
      </p>

      <button onClick={handleLogout}>
        Logout
      </button>
    </div>
  )
}

export default Dashboard