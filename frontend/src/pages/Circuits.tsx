import { useEffect, useRef, useState } from "react"
import { Link, useNavigate } from "react-router-dom"
import maplibregl from "maplibre-gl"
import "maplibre-gl/dist/maplibre-gl.css"
import { api, type CircuitSearchResult } from "../services/api"

export function Circuits() {
  const navigate = useNavigate()
  const mapContainer = useRef<HTMLDivElement>(null)
  const map = useRef<maplibregl.Map | null>(null)
  const markers = useRef<maplibregl.Marker[]>([])

  const [circuits, setCircuits] = useState<CircuitSearchResult[]>([])
  const [loading, setLoading] = useState(true)
  const [radius, setRadius] = useState("300")
  const [noiseFilter, setNoiseFilter] = useState("")
  const [levelFilter, setLevelFilter] = useState("")

  useEffect(() => {
    if (!mapContainer.current || map.current) return
    map.current = new maplibregl.Map({
      container: mapContainer.current,
      style: "https://basemaps.cartocdn.com/gl/dark-matter-gl-style/style.json",
      center: [2.5, 46.8],
      zoom: 5.5,
    })
    map.current.addControl(new maplibregl.NavigationControl(), "top-left")

    return () => { map.current?.remove(); map.current = null; }
  }, [])

  async function load() {
    setLoading(true)
    try {
      const params: Record<string, string | number | undefined> = {}
      if (radius) params.radius_km = Number(radius)
      if (noiseFilter) params.vehicle_noise_db = Number(noiseFilter)
      if (levelFilter) params.level = levelFilter

      const list = await api.circuits.search(params)
      setCircuits(list)
      updateMap(list)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => { load() }, [])

  function updateMap(list: CircuitSearchResult[]) {
    if (!map.current) return
    markers.current.forEach((m) => m.remove())
    markers.current = []

    if (list.length === 0) return

    list.forEach((c, i) => {
      const el = document.createElement("div")
      el.className = "map-marker"
      el.innerHTML = `<span>${i + 1}</span>`
      el.addEventListener("click", () => navigate(`/circuits/${c.id}`))

      const marker = new maplibregl.Marker({ element: el })
        .setLngLat([c.lon || 2.5, c.lat || 46.8])
        .setPopup(
          new maplibregl.Popup({ offset: 25 }).setHTML(
            `<strong>${c.name}</strong><br/>${c.city || ""}<br/><a href="/circuits/${c.id}">Voir le circuit</a>`
          )
        )
        .addTo(map.current!)
      markers.current.push(marker)
    })
  }

  async function handleSearch(e: React.FormEvent) {
    e.preventDefault()
    await load()
  }

  return (
    <div className="page">
      <div className="page-header">
        <h1>Recherche de Circuits</h1>
      </div>

      <form onSubmit={handleSearch} className="card search-form">
        <div className="field-row">
          <label>
            Rayon (km)
            <input type="number" value={radius} onChange={(e) => setRadius(e.target.value)} placeholder="300" />
          </label>
          <label>
            Mon véhicule (dB)
            <input type="number" step="0.1" value={noiseFilter} onChange={(e) => setNoiseFilter(e.target.value)} placeholder="Ex: 102" />
          </label>
          <label>
            Niveau
            <select value={levelFilter} onChange={(e) => setLevelFilter(e.target.value)}>
              <option value="">Tous</option>
              <option value="debutant">Débutant</option>
              <option value="intermediaire">Intermédiaire</option>
              <option value="confirme">Confirmé</option>
            </select>
          </label>
        </div>
        <button type="submit" className="btn">Rechercher</button>
      </form>

      <div className="circuits-layout">
        <div className="circuits-list">
          {loading ? (
            <p className="empty">Chargement...</p>
          ) : circuits.length === 0 ? (
            <p className="empty">Aucun circuit trouvé. Ajustez vos filtres.</p>
          ) : (
            circuits.map((c) => (
              <Link to={`/circuits/${c.id}`} key={c.id} className="card circuit-card">
                <h3>{c.name}</h3>
                <p>{c.city || "Localisation non disponible"}</p>
                <div className="circuit-tags">
                  {c.length_km && <span className="tag">{c.length_km} km</span>}
                  {c.has_noise_restriction && c.noise_limit_db && (
                    <span className="tag noise">🔊 {c.noise_limit_db} dB max</span>
                  )}
                  {c.distance_km !== null && c.distance_km !== undefined && (
                    <span className="tag">{Math.round(c.distance_km)} km</span>
                  )}
                  <span className="tag">{c.events_count} événements</span>
                </div>
              </Link>
            ))
          )}
        </div>
        <div ref={mapContainer} className="map-container" />
      </div>
    </div>
  )
}
