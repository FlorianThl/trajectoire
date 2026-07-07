import { Link } from "react-router-dom"

export function NotFound() {
  return (
    <div className="page" style={{ textAlign: "center", marginTop: "4rem" }}>
      <div style={{ fontSize: "5rem", fontWeight: 800, background: "linear-gradient(135deg, var(--primary), #4dabf7)", WebkitBackgroundClip: "text", WebkitTextFillColor: "transparent", lineHeight: 1.2 }}>404</div>
      <p style={{ fontSize: "1.1rem", color: "var(--text-secondary)", marginTop: "0.5rem" }}>Cette page n'existe pas ou a été déplacée.</p>
      <div style={{ marginTop: "2rem", display: "flex", gap: "0.75rem", justifyContent: "center" }}>
        <Link to="/" className="btn">Accueil</Link>
        <Link to="/circuits" className="btn secondary">Explorer les circuits</Link>
      </div>
    </div>
  )
}
