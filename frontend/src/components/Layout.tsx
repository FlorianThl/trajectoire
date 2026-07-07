import { Link, Outlet, useNavigate } from "react-router-dom"
import { useAuth } from "../contexts/AuthContext"

export function Layout() {
  const { user, logout } = useAuth()
  const navigate = useNavigate()

  function handleLogout() {
    logout()
    navigate("/login")
  }

  return (
    <div className="layout">
      <nav className="navbar">
        <Link to="/" className="logo">Trajectoire</Link>
        {user && (
          <div className="nav-links">
            <Link to="/profil">Profil</Link>
            <Link to="/garage">Garage</Link>
            <Link to="/circuits">Circuits</Link>
            <Link to="/meilleurs-tours">Mes chronos</Link>
            <button onClick={handleLogout} className="btn-link">Deconnexion</button>
          </div>
        )}
      </nav>
      <main className="content">
        <Outlet />
      </main>
    </div>
  )
}
