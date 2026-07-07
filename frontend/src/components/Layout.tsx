import { Link, Outlet, useNavigate } from "react-router-dom"
import { useAuth } from "../contexts/AuthContext"

export function Layout() {
  const { user, logout } = useAuth()
  const navigate = useNavigate()

  function handleLogout() {
    logout()
    navigate("/")
  }

  return (
    <div className="layout">
      <nav className="navbar">
        <Link to="/" className="logo">Trajectoire</Link>
        <div className="nav-links">
          <Link to="/circuits">Circuits</Link>
          {user ? (
            <>
              <Link to="/garage">Garage</Link>
              <Link to="/profil">Profil</Link>
              <Link to="/meilleurs-tours">Chronos</Link>
              <Link to="/cv-mecanique">CV Meca</Link>
              <button onClick={handleLogout} className="btn-link">Déconnexion</button>
            </>
          ) : (
            <>
              <Link to="/login">Connexion</Link>
              <Link to="/register" className="btn small" style={{ marginLeft: "0.5rem" }}>Inscription</Link>
            </>
          )}
        </div>
      </nav>
      <main className="content">
        <Outlet />
      </main>
    </div>
  )
}
