import { createContext, useContext, useEffect, useState, type ReactNode } from "react"
import { api, type UserRead } from "../services/api"

interface AuthContextType {
  user: UserRead | null
  loading: boolean
  login: (email: string, password: string) => Promise<void>
  register: (data: Parameters<typeof api.auth.register>[0]) => Promise<void>
  logout: () => void
}

const AuthContext = createContext<AuthContextType | null>(null)

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<UserRead | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    if (localStorage.getItem("token")) {
      api.auth.me()
        .then(setUser)
        .catch(() => localStorage.removeItem("token"))
        .finally(() => setLoading(false))
    } else {
      setLoading(false)
    }
  }, [])

  async function login(email: string, password: string) {
    const res = await api.auth.login({ email, password })
    localStorage.setItem("token", res.access_token)
    const me = await api.auth.me()
    setUser(me)
  }

  async function register(data: Parameters<typeof api.auth.register>[0]) {
    await api.auth.register(data)
  }

  function logout() {
    localStorage.removeItem("token")
    setUser(null)
  }

  return (
    <AuthContext.Provider value={{ user, loading, login, register, logout }}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  const ctx = useContext(AuthContext)
  if (!ctx) throw new Error("useAuth must be used within AuthProvider")
  return ctx
}
