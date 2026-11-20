import {
  createContext,
  useContext,
  useEffect,
  useMemo,
  useState
} from "react"

const LanguageContext = createContext(null)

const messages = {
  en: {
    language: "Language", bankAccountSystem: "Bank Account System",
    login: "Login", register: "Register", username: "Username", password: "Password",
    invalidCredentials: "Username or password is incorrect.", loggingIn: "Logging in...",
    registrationFailed: "Registration failed.", backToLogin: "Back to Login",
    dashboard: "Dashboard", welcome: "Welcome {username}", role: "Role: {role}",
    myAccounts: "My Accounts", logout: "Logout", accounts: "Accounts",
    backToDashboard: "Back to Dashboard", createAccount: "Create Account",
    accountNumber: "Account Number", initialBalance: "Initial Balance",
    accountCreated: "Account created successfully.", couldNotCreateAccount: "Could not create account.",
    couldNotLoadAccounts: "Could not load accounts.", loading: "Loading...",
    noAccounts: "No accounts found.", bankOperations: "Bank Operations",
    selectAccount: "Select Account", amount: "Amount", deposit: "Deposit",
    depositSuccessful: "Deposit successful.", depositFailed: "Deposit failed.",
    withdraw: "Withdraw", withdrawalSuccessful: "Withdrawal successful.",
    withdrawalFailed: "Withdrawal failed.", balance: "Balance: {amount}",
    transfer: "Transfer", from: "From", toAccount: "To Account",
    transferSuccessful: "Transfer successful.", transferFailed: "Transfer failed.",
    transactionHistory: "Transaction History", loadTransactions: "Load Transactions",
    filterTransactions: "Filter by type", allTypes: "All types",
    noTransactions: "No transactions loaded.",
    noMatchingTransactions: "No transactions match this type.",
    couldNotLoadTransactions: "Could not load transactions."
  },
  de: {
    language: "Sprache", bankAccountSystem: "Bankkontensystem", login: "Anmelden",
    register: "Registrieren", username: "Benutzername", password: "Passwort",
    invalidCredentials: "Benutzername oder Passwort ist falsch.", loggingIn: "Anmeldung läuft...",
    registrationFailed: "Registrierung fehlgeschlagen.", backToLogin: "Zurück zur Anmeldung",
    dashboard: "Übersicht", welcome: "Willkommen {username}", role: "Rolle: {role}",
    myAccounts: "Meine Konten", logout: "Abmelden", accounts: "Konten",
    backToDashboard: "Zurück zur Übersicht", createAccount: "Konto erstellen",
    accountNumber: "Kontonummer", initialBalance: "Anfangsguthaben",
    accountCreated: "Konto erfolgreich erstellt.", couldNotCreateAccount: "Konto konnte nicht erstellt werden.",
    couldNotLoadAccounts: "Konten konnten nicht geladen werden.", loading: "Wird geladen...",
    noAccounts: "Keine Konten gefunden.", bankOperations: "Bankgeschäfte",
    selectAccount: "Konto auswählen", amount: "Betrag", deposit: "Einzahlen",
    depositSuccessful: "Einzahlung erfolgreich.", depositFailed: "Einzahlung fehlgeschlagen.",
    withdraw: "Abheben", withdrawalSuccessful: "Auszahlung erfolgreich.",
    withdrawalFailed: "Auszahlung fehlgeschlagen.", balance: "Kontostand: {amount}",
    transfer: "Überweisung", from: "Von", toAccount: "Empfängerkonto",
    transferSuccessful: "Überweisung erfolgreich.", transferFailed: "Überweisung fehlgeschlagen.",
    transactionHistory: "Transaktionsverlauf", loadTransactions: "Transaktionen laden",
    filterTransactions: "Nach Typ filtern", allTypes: "Alle Typen",
    noTransactions: "Keine Transaktionen geladen.",
    noMatchingTransactions: "Keine Transaktionen dieses Typs.",
    couldNotLoadTransactions: "Transaktionen konnten nicht geladen werden."
  },
  ar: {
    language: "اللغة", bankAccountSystem: "نظام الحسابات البنكية", login: "تسجيل الدخول",
    register: "إنشاء حساب", username: "اسم المستخدم", password: "كلمة المرور",
    invalidCredentials: "اسم المستخدم أو كلمة المرور غير صحيحة.", loggingIn: "جاري تسجيل الدخول...",
    registrationFailed: "فشل إنشاء الحساب.", backToLogin: "العودة لتسجيل الدخول",
    dashboard: "لوحة التحكم", welcome: "أهلًا {username}", role: "الصلاحية: {role}",
    myAccounts: "حساباتي", logout: "تسجيل الخروج", accounts: "الحسابات",
    backToDashboard: "العودة للوحة التحكم", createAccount: "إنشاء حساب بنكي",
    accountNumber: "رقم الحساب", initialBalance: "الرصيد المبدئي",
    accountCreated: "تم إنشاء الحساب بنجاح.", couldNotCreateAccount: "تعذر إنشاء الحساب.",
    couldNotLoadAccounts: "تعذر تحميل الحسابات.", loading: "جاري التحميل...",
    noAccounts: "لم يتم العثور على حسابات.", bankOperations: "العمليات البنكية",
    selectAccount: "اختار حسابًا", amount: "المبلغ", deposit: "إيداع",
    depositSuccessful: "تم الإيداع بنجاح.", depositFailed: "فشلت عملية الإيداع.",
    withdraw: "سحب", withdrawalSuccessful: "تم السحب بنجاح.",
    withdrawalFailed: "فشلت عملية السحب.", balance: "الرصيد: {amount}",
    transfer: "تحويل", from: "من حساب", toAccount: "إلى حساب",
    transferSuccessful: "تم التحويل بنجاح.", transferFailed: "فشلت عملية التحويل.",
    transactionHistory: "سجل المعاملات", loadTransactions: "عرض المعاملات",
    filterTransactions: "تصفية حسب النوع", allTypes: "كل الأنواع",
    noTransactions: "لا توجد معاملات معروضة.",
    noMatchingTransactions: "مفيش معاملات من النوع ده.",
    couldNotLoadTransactions: "تعذر تحميل المعاملات."
  }
}

export function LanguageProvider({ children }) {
  const [language, setLanguage] = useState(() => {
    const saved = localStorage.getItem("bankLanguage")
    return messages[saved] ? saved : "en"
  })

  useEffect(() => {
    localStorage.setItem("bankLanguage", language)
    document.documentElement.lang = language
    document.documentElement.dir = language === "ar" ? "rtl" : "ltr"
  }, [language])

  const value = useMemo(() => ({
    language,
    setLanguage,
    t: (key, values = {}) => {
      let text = messages[language][key] ?? messages.en[key] ?? key
      for (const [name, replacement] of Object.entries(values)) {
        text = text.replace(`{${name}}`, String(replacement ?? ""))
      }
      return text
    }
  }), [language])

  return <LanguageContext.Provider value={value}>{children}</LanguageContext.Provider>
}

export function useLanguage() {
  return useContext(LanguageContext)
}
