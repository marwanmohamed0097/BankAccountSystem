import {
  createContext,
  useContext,
  useEffect,
  useState
} from "react"

import {
  getCurrentUser,
  loginUser
} from "../api/api"

const AuthContext = createContext()

export function AuthProvider({ children }) {
  const [token, setToken] = useState(
    localStorage.getItem("token")
  )

  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    async function loadUser() {
      if (!token) {
        setLoading(false)
        return
      }

      try {
        const currentUser = await getCurrentUser(token)
        setUser(currentUser)
      } catch {
        localStorage.removeItem("token")
        setToken(null)
        setUser(null)
      } finally {
        setLoading(false)
      }
    }

    loadUser()
  }, [token])

  async function login(username, password) {
    const data = await loginUser(
      username,
      password
    )

    localStorage.setItem(
      "token",
      data.access_token
    )

    setToken(data.access_token)

    const currentUser = await getCurrentUser(
      data.access_token
    )

    setUser(currentUser)
  }

  function logout() {
    localStorage.removeItem("token")
    setToken(null)
    setUser(null)
  }

  return (
    <AuthContext.Provider
      value={{
        token,
        user,
        loading,
        login,
        logout
      }}
    >
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  return useContext(AuthContext)
}