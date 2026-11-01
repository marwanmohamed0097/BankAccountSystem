import { useEffect, useState } from "react"
import { useNavigate } from "react-router-dom"
import { useAuth } from "../context/AuthContext"
import {
  createAccount,
  getAccounts
} from "../api/api"

function Accounts() {
  const { token } = useAuth()
  const navigate = useNavigate()

  const [accounts, setAccounts] = useState([])
  const [accountNumber, setAccountNumber] = useState("")
  const [initialBalance, setInitialBalance] = useState(0)
  const [error, setError] = useState("")
  const [loading, setLoading] = useState(true)

  async function loadAccounts() {
    try {
      setError("")

      const data = await getAccounts(token)

      setAccounts(data.accounts)
    } catch {
      setError("Could not load accounts.")
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    loadAccounts()
  }, [])

  async function handleCreateAccount(event) {
    event.preventDefault()

    try {
      setError("")

      await createAccount(
        token,
        accountNumber,
        initialBalance
      )

      setAccountNumber("")
      setInitialBalance(0)

      await loadAccounts()
    } catch {
      setError("Could not create account.")
    }
  }

  return (
    <div>
      <h1>Accounts</h1>

      <button onClick={() => navigate("/dashboard")}>
        Back to Dashboard
      </button>

      <h2>Create Account</h2>

      <form onSubmit={handleCreateAccount}>
        <div>
          <label>Account Number</label>

          <input
            type="text"
            value={accountNumber}
            onChange={(event) =>
              setAccountNumber(event.target.value)
            }
            required
          />
        </div>

        <div>
          <label>Initial Balance</label>

          <input
            type="number"
            min="0"
            step="0.01"
            value={initialBalance}
            onChange={(event) =>
              setInitialBalance(event.target.value)
            }
            required
          />
        </div>

        <button type="submit">
          Create Account
        </button>
      </form>

      {error && <p>{error}</p>}

      <h2>My Accounts</h2>

      {loading ? (
        <p>Loading...</p>
      ) : accounts.length === 0 ? (
        <p>No accounts found.</p>
      ) : (
        <ul>
          {accounts.map((account) => (
            <li key={account.account_number}>
              {account.account_number}
              {" - "}
              Balance: {account.balance}
            </li>
          ))}
        </ul>
      )}
    </div>
  )
}

export default Accounts
