import { useEffect, useState } from "react"
import { useNavigate } from "react-router-dom"
import { useAuth } from "../context/AuthContext"
import { useLanguage } from "../context/LanguageContext"

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
  const { t } = useLanguage()
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
      setError(t("couldNotLoadAccounts"))
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

      setMessage(t("accountCreated"))

      await loadAccounts()
    } catch {
      setError(t("couldNotCreateAccount"))
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
      setMessage(t("depositSuccessful"))

      await loadAccounts()
    } catch {
      setError(t("depositFailed"))
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
      setMessage(t("withdrawalSuccessful"))

      await loadAccounts()
    } catch {
      setError(t("withdrawalFailed"))
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

      setMessage(t("transferSuccessful"))

      await loadAccounts()
    } catch {
      setError(t("transferFailed"))
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
      setError(t("couldNotLoadTransactions"))
    }
  }

  return (
    <div>
      <h1>{t("accounts")}</h1>

      <button onClick={() => navigate("/dashboard")}>
        {t("backToDashboard")}
      </button>

      <h2>{t("createAccount")}</h2>

      <form onSubmit={handleCreateAccount}>
        <div>
          <label>{t("accountNumber")}</label>

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
          <label>{t("initialBalance")}</label>

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
          {t("createAccount")}
        </button>
      </form>

      {error && <p>{error}</p>}
      {message && <p>{message}</p>}

      <h2>{t("myAccounts")}</h2>

      {loading ? (
        <p>{t("loading")}</p>
      ) : accounts.length === 0 ? (
        <p>{t("noAccounts")}</p>
      ) : (
        <>
          <ul>
            {accounts.map((account) => (
              <li key={account.account_number}>
                {account.account_number}
                {" - "}
                {t("balance", { amount: account.balance })}
              </li>
            ))}
          </ul>

          <h2>{t("bankOperations")}</h2>

          <div>
            <label>{t("selectAccount")}</label>

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
            <label>{t("amount")}</label>

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
            {t("deposit")}
          </button>

          <button
            type="button"
            onClick={handleWithdraw}
          >
            {t("withdraw")}
          </button>

          <h2>{t("transfer")}</h2>

          <form onSubmit={handleTransfer}>
            <div>
              <label>{t("from")}</label>

              <input
                value={selectedAccount}
                readOnly
              />
            </div>

            <div>
              <label>{t("toAccount")}</label>

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
              <label>{t("amount")}</label>

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
              {t("transfer")}
            </button>
          </form>

          <h2>{t("transactionHistory")}</h2>

          <button
            type="button"
            onClick={handleLoadTransactions}
          >
            {t("loadTransactions")}
          </button>

          {transactions.length === 0 ? (
            <p>{t("noTransactions")}</p>
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
