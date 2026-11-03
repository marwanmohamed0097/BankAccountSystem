const API_URL = "http://127.0.0.1:8000"

export async function loginUser(username, password) {
  const response = await fetch(`${API_URL}/login`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      username,
      password
    })
  })

  if (!response.ok) {
    throw new Error("Invalid username or password")
  }

  return response.json()
}

export async function getCurrentUser(token) {
  const response = await fetch(`${API_URL}/me`, {
    headers: {
      Authorization: `Bearer ${token}`
    }
  })

  if (!response.ok) {
    throw new Error("Invalid session")
  }

  return response.json()
}
export async function getAccounts(token) {
  const response = await fetch(`${API_URL}/accounts`, {
    headers: {
      Authorization: `Bearer ${token}`
    }
  })

  if (!response.ok) {
    throw new Error("Could not load accounts")
  }

  return response.json()
}

export async function createAccount(
  token,
  accountNumber,
  initialBalance
) {
  const response = await fetch(`${API_URL}/accounts`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`
    },
    body: JSON.stringify({
      account_number: accountNumber,
      initial_balance: Number(initialBalance),
      customer_id: null
    })
  })

  if (!response.ok) {
    throw new Error("Could not create account")
  }

  return response.json()
}

export async function depositMoney(token, accountNumber, amount) {
  const response = await fetch(`${API_URL}/deposit`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`
    },
    body: JSON.stringify({
      account_number: accountNumber,
      amount: Number(amount)
    })
  })

  if (!response.ok) {
    throw new Error("Deposit failed")
  }

  return response.json()
}

export async function withdrawMoney(token, accountNumber, amount) {
  const response = await fetch(`${API_URL}/withdraw`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`
    },
    body: JSON.stringify({
      account_number: accountNumber,
      amount: Number(amount)
    })
  })

  if (!response.ok) {
    throw new Error("Withdraw failed")
  }

  return response.json()
}

export async function transferMoney(
  token,
  fromAccount,
  toAccount,
  amount
) {
  const response = await fetch(`${API_URL}/transfer`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`
    },
    body: JSON.stringify({
      from_account: fromAccount,
      to_account: toAccount,
      amount: Number(amount)
    })
  })

  if (!response.ok) {
    throw new Error("Transfer failed")
  }

  return response.json()
}

export async function getTransactions(token, accountNumber) {
  const response = await fetch(
    `${API_URL}/transactions/${accountNumber}`,
    {
      headers: {
        Authorization: `Bearer ${token}`
      }
    }
  )

  if (!response.ok) {
    throw new Error("Could not load transactions")
  }

  return response.json()
}
