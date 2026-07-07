import { useEffect, useState } from "react"
import { useParams, Link } from "react-router-dom"
import { api, type CircuitRead, type EventRead } from "../services/api"

export function CircuitDetail() {
  const { id } = useParams<{ id: string }>()
  const [circuit, setCircuit] = useState<CircuitRead | null>(null)
  const [events, setEvents] = useState<EventRead[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    if (!id) return
    setLoading(true)
    Promise.all([
      api.circuits.get(id),
      api.circuits.events(id),
    ])
      .then(([c, e]) => {
        setCircuit(c)
        setEvents(e)
      })
      .finally(() => setLoading(false))
  }, [id])

  if (loading) return <div className="page"><p>Chargement...</p></div>
  if (!circuit) return <div className="page"><p>Circuit introuvable</p></div>

  const dateOpts: Intl.DateTimeFormatOptions = { day: "numeric", month: "long", year: "numeric" }

  return (
    <div className="page">
      <Link to="/circuits" className="back-link">{'<-'} Retour aux circuits</Link>

      <div className="page-header">
        <h1>{circuit.name}</h1>
        {circuit.website_url && (
          <a href={circuit.website_url} target="_blank" rel="noopener noreferrer" className="btn">
            Site web
          </a>
        )}
      </div>

      <div className="card">
        <div className="circuit-detail-grid">
          <div>
            <h3>Informations</h3>
            <p><strong>Ville :</strong> {circuit.city || "N/A"}</p>
            <p><strong>Pays :</strong> {circuit.country}</p>
            <p><strong>Longueur :</strong> {circuit.length_km ? `${circuit.length_km} km` : "N/A"}</p>
            <p><strong>Type :</strong> {circuit.layout_type === "permanent" ? "Permanent" : circuit.layout_type}</p>
            <p><strong>Degagements :</strong> {circuit.runoff_areas === "asphalte" ? "Asphalte" : circuit.runoff_areas === "graviers" ? "Graviers" : circuit.runoff_areas === "mixte" ? "Mixte" : "N/A"}</p>
            {circuit.description && <p><strong>Description :</strong> {circuit.description}</p>}
          </div>
          <div>
            <h3>Commodites</h3>
            <p>{circuit.has_electricity ? "OK Bornes electriques" : "-- Pas de borne electrique"}</p>
            <p>{circuit.has_compressor ? "OK Compresseur" : "-- Pas de compresseur"}</p>
            <p>{circuit.has_fuel_station ? "OK Station SP98" : "-- Pas de station"}</p>
          </div>
          <div>
            <h3>Restrictions</h3>
            {circuit.has_noise_restriction ? (
              <p>Limite sonore : <strong>{circuit.noise_limit_db} dB</strong></p>
            ) : (
              <p>Aucune restriction sonore</p>
            )}
            <p>
              Categories autorisees :{" "}
              {circuit.allowed_categories?.map((c) => c === "auto" ? "Auto" : c === "moto" ? "Moto" : c).join(", ")}
            </p>
          </div>
        </div>
      </div>

      <h2>Evenements ({events.length})</h2>
      {events.length === 0 ? (
        <p className="empty">Aucun evenement planifie pour ce circuit.</p>
      ) : (
        <div className="events-list">
          {events.map((e) => (
            <div key={e.id} className="card event-card">
              <div className="event-header">
                <h3>{e.organizer_name}</h3>
                {e.spots_available !== null && e.spots_available !== undefined && e.spots_available <= 5 && (
                  <span className="badge danger">Plus que {e.spots_available} places</span>
                )}
              </div>
              <p className="event-dates">
                {new Date(e.start_date).toLocaleDateString("fr-FR", dateOpts)}
                {e.start_date !== e.end_date && (
                  <> - {new Date(e.end_date).toLocaleDateString("fr-FR", dateOpts)}</>
                )}
              </p>
              <div className="event-tags">
                {e.has_debutant && <span className="tag">Debutant</span>}
                {e.has_intermediaire && <span className="tag">Intermediaire</span>}
                {e.has_confirme && <span className="tag">Confirme</span>}
                {e.price_base && <span className="tag price">{e.price_base.toFixed(0)} {'\u20AC'}</span>}
                {e.price_license && (
                  <span className="tag price">{e.price_license.toFixed(0)} {'\u20AC'} (licencie)</span>
                )}
              </div>
              {e.booking_url && (
                <a href={e.booking_url} target="_blank" rel="noopener noreferrer" className="btn" style={{ marginTop: "0.75rem" }}>
                  Reserver
                </a>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
