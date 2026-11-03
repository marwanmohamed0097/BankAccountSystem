import { useEffect, useState } from "react"
import { useNavigate } from "react-router-dom"
import { useAuth } from "../context/AuthContext"

import {
  createAccount,
  depositMoney,
  getAccounts,
  getTransactions,
  transferMoney,
  withdrawMoney
} from "../api/api"

function Accounts() {
  const { token } = useAuth()
  const navigate = useNavigate()

  const [accounts, setAccounts] = useState([])
  const [transactions, setTransactions] = useState([])

  const [accountNumber, setAccountNumber] = useState("")
  const [initialBalance, setInitialBalance] = useState(0)

  const [selectedAccount, setSelectedAccount] = useState("")
  const [amount, setAmount] = useState("")

  const [toAccount, setToAccount] = useState("")
  const [transferAmount, setTransferAmount] = useState("")

  const [error, setError] = useState("")
  const [message, setMessage] = useState("")
  const [loading, setLoading] = useState(true)

  async function loadAccounts() {
    try {
      setError("")

      const data = await getAccounts(token)

      setAccounts(data.accounts)

      if (
        !selectedAccount &&
        data.accounts.length > 0
      ) {
        setSelectedAccount(
          data.accounts[0].account_number
        )
      }
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
      setMessage("")

      await createAccount(
        token,
        accountNumber,
        initialBalance
      )

      setAccountNumber("")
      setInitialBalance(0)

      setMessage("Account created successfully.")

      await loadAccounts()
    } catch {
      setError("Could not create account.")
    }
  }

  async function handleDeposit() {
    try {
      setError("")
      setMessage("")

      await depositMoney(
        token,
        selectedAccount,
        amount
      )

      setAmount("")
      setMessage("Deposit successful.")

      await loadAccounts()
    } catch {
      setError("Deposit failed.")
    }
  }

  async function handleWithdraw() {
    try {
      setError("")
      setMessage("")

      await withdrawMoney(
        token,
        selectedAccount,
        amount
      )

      setAmount("")
      setMessage("Withdrawal successful.")

      await loadAccounts()
    } catch {
      setError("Withdrawal failed.")
    }
  }

  async function handleTransfer(event) {
    event.preventDefault()

    try {
      setError("")
      setMessage("")

      await transferMoney(
        token,
        selectedAccount,
        toAccount,
        transferAmount
      )

      setToAccount("")
      setTransferAmount("")

      setMessage("Transfer successful.")

      await loadAccounts()
    } catch {
      setError("Transfer failed.")
    }
  }

  async function handleLoadTransactions() {
    try {
      setError("")
      setMessage("")

      const data = await getTransactions(
        token,
        selectedAccount
      )

      setTransactions(data.transactions)
    } catch {
      setError("Could not load transactions.")
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
      {message && <p>{message}</p>}

      <h2>My Accounts</h2>

      {loading ? (
        <p>Loading...</p>
      ) : accounts.length === 0 ? (
        <p>No accounts found.</p>
      ) : (
        <>
          <ul>
            {accounts.map((account) => (
              <li key={account.account_number}>
                {account.account_number}
                {" - "}
                Balance: {account.balance}
              </li>
            ))}
          </ul>

          <h2>Bank Operations</h2>

          <div>
            <label>Select Account</label>

            <select
              value={selectedAccount}
              onChange={(event) =>
                setSelectedAccount(
                  event.target.value
                )
              }
            >
              {accounts.map((account) => (
                <option
                  key={account.account_number}
                  value={account.account_number}
                >
                  {account.account_number}
                </option>
              ))}
            </select>
          </div>

          <div>
            <label>Amount</label>

            <input
              type="number"
              min="0.01"
              step="0.01"
              value={amount}
              onChange={(event) =>
                setAmount(event.target.value)
              }
            />
          </div>

          <button
            type="button"
            onClick={handleDeposit}
          >
            Deposit
          </button>

          <button
            type="button"
            onClick={handleWithdraw}
          >
            Withdraw
          </button>

          <h2>Transfer</h2>

          <form onSubmit={handleTransfer}>
            <div>
              <label>From</label>

              <input
                value={selectedAccount}
                readOnly
              />
            </div>

            <div>
              <label>To Account</label>

              <input
                type="text"
                value={toAccount}
                onChange={(event) =>
                  setToAccount(event.target.value)
                }
                required
              />
            </div>

            <div>
              <label>Amount</label>

              <input
                type="number"
                min="0.01"
                step="0.01"
                value={transferAmount}
                onChange={(event) =>
                  setTransferAmount(
                    event.target.value
                  )
                }
                required
              />
            </div>

            <button type="submit">
              Transfer
            </button>
          </form>

          <h2>Transaction History</h2>

          <button
            type="button"
            onClick={handleLoadTransactions}
          >
            Load Transactions
          </button>

          {transactions.length === 0 ? (
            <p>No transactions loaded.</p>
          ) : (
            <ul>
              {transactions.map(
                (transaction, index) => (
                  <li key={index}>
                    {transaction.type}
                    {" - "}
                    {transaction.amount}
                  </li>
                )
              )}
            </ul>
          )}
        </>
      )}
    </div>
  )
}

export default Accounts
