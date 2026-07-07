import { useEffect, useState } from "react"
import { Link } from "react-router-dom"
import { api, type CircuitSearchResult } from "../services/api"

const FEATURED_SLUGS = ["paul-ricard", "spa-francorchamps", "carole", "lohéac"]

export function Home() {
  const [circuits, setCircuits] = useState<CircuitSearchResult[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    api.circuits.search({})
      .then((list) => {
        const featured = list.filter((c) => FEATURED_SLUGS.includes(c.slug))
        setCircuits(featured.length > 0 ? featured : list.slice(0, 4))
      })
      .finally(() => setLoading(false))
  }, [])

  return (
    <div className="home">
      {/* Hero */}
      <section className="hero">
        <div className="hero-bg" />
        <div className="hero-content">
          <h1>Votre trajectoire commence ici</h1>
          <p>La plateforme qui centralise les trackdays et vous aide à choisir le circuit idéal pour votre véhicule.</p>
          <div className="hero-actions">
            <Link to="/register" className="btn btn-hero">Commencer</Link>
            <Link to="/circuits" className="btn btn-hero-secondary">Explorer les circuits</Link>
          </div>
        </div>
      </section>

      {/* Stats */}
      <section className="home-section">
        <div className="stats-row">
          <div className="stat-badge">🏁 15+ circuits référencés</div>
          <div className="stat-badge">📅 50+ événements par an</div>
          <div className="stat-badge">🔊 Filtrage sonore intelligent</div>
          <div className="stat-badge">📊 CV Mécanique inclus</div>
        </div>
      </section>

      {/* How it works */}
      <section className="home-section">
        <h2>Comment ça marche ?</h2>
        <div className="steps-grid">
          <div className="step-card">
            <span className="step-number">1</span>
            <h3>Créez votre profil</h3>
            <p>Inscrivez-vous et renseignez votre licence pour des tarifs dédiés.</p>
          </div>
          <div className="step-card">
            <span className="step-number">2</span>
            <h3>Ajoutez vos véhicules</h3>
            <p>Configurez votre garage virtuel avec les caractéristiques réelles (dB, pneus, freins).</p>
          </div>
          <div className="step-card">
            <span className="step-number">3</span>
            <h3>Trouvez votre circuit</h3>
            <p>Filtrez par bruit, distance et niveau. Le moteur écarte automatiquement les circuits incompatibles.</p>
          </div>
          <div className="step-card">
            <span className="step-number">4</span>
            <h3>Piste & Statistiques</h3>
            <p>Enregistrez vos chronos, suivez votre progression et l'usure de vos consommables.</p>
          </div>
        </div>
      </section>

      {/* Featured circuits */}
      <section className="home-section">
        <div className="section-header">
          <h2>Circuits populaires</h2>
          <Link to="/circuits" className="btn secondary">Voir tout</Link>
        </div>
        {loading ? (
          <p className="empty">Chargement...</p>
        ) : (
          <div className="featured-circuits">
            {circuits.map((c) => (
              <Link to={`/circuits/${c.id}`} key={c.id} className="card featured-card">
                <div className="featured-card-header">
                  <h3>{c.name}</h3>
                  <span className="tag">{c.length_km ? `${c.length_km} km` : "—"}</span>
                </div>
                <p>{c.city || "Localisation non disponible"}</p>
                <div className="featured-card-tags">
                  {c.has_noise_restriction && c.noise_limit_db && (
                    <span className="tag noise">🔊 {c.noise_limit_db} dB max</span>
                  )}
                  <span className="tag">{c.events_count} événements</span>
                  {c.allowed_categories?.map((cat) => (
                    <span key={cat} className="tag">{cat === "auto" ? "🚗 Auto" : "🏍️ Moto"}</span>
                  ))}
                </div>
              </Link>
            ))}
          </div>
        )}
      </section>

      {/* CTA */}
      <section className="home-section cta-section">
        <div className="cta-card">
          <h2>Prêt à prendre la piste ?</h2>
          <p>Rejoignez la communauté Trajectoire et ne manquez plus aucun trackday.</p>
          <Link to="/register" className="btn btn-hero">Créer mon compte</Link>
        </div>
      </section>
    </div>
  )
}
