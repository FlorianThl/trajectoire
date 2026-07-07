import { Link } from "react-router-dom"

export function NotFound() {
  return (
    <div className="page" style={{ textAlign: "center", marginTop: "4rem" }}>
      <h1>404</h1>
      <p>Page introuvable</p>
      <Link to="/login" className="btn" style={{ display: "inline-block", marginTop: "1rem" }}>
        Retour a l'accueil
      </Link>
    </div>
  )
}
