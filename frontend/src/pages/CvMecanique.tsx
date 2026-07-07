import { useEffect, useState } from "react"
import { api, type VehicleStats } from "../services/api"

export function CvMecanique() {
  const [stats, setStats] = useState<VehicleStats[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    api.vehicleStats().then(setStats).finally(() => setLoading(false))
  }, [])

  if (loading) return <div className="page"><p>Chargement...</p></div>

  const totalKm = stats.reduce((s, v) => s + v.total_track_km, 0)
  const totalLaps = stats.reduce((s, v) => s + v.total_laps, 0)
  const totalRecords = stats.reduce((s, v) => s + v.lap_records_count, 0)

  return (
    <div className="page">
      <div className="page-header">
        <h1>CV Mecanique</h1>
      </div>

      <div className="stats-summary">
        <div className="card stat-card">
          <h3>{stats.length}</h3>
          <p>Vehicules</p>
        </div>
        <div className="card stat-card">
          <h3>{totalLaps.toLocaleString("fr-FR")}</h3>
          <p>Tours total</p>
        </div>
        <div className="card stat-card">
          <h3>{totalKm.toFixed(1)} km</h3>
          <p>Kilometrage piste</p>
        </div>
        <div className="card stat-card">
          <h3>{totalRecords}</h3>
          <p>Chronos enregistres</p>
        </div>
      </div>

      {stats.length === 0 ? (
        <p className="empty">Ajoutez des vehicules dans votre garage pour voir leurs statistiques.</p>
      ) : (
        <div className="vehicle-stats-grid">
          {stats.map((v) => (
            <div key={v.id} className="card">
              <h3>{v.brand} {v.model}</h3>
              <div className="stat-row">
                <span>Tours</span>
                <strong>{v.total_laps.toLocaleString("fr-FR")}</strong>
              </div>
              <div className="stat-row">
                <span>Km piste</span>
                <strong>{v.total_track_km.toFixed(1)} km</strong>
              </div>
              <div className="stat-row">
                <span>Chronos</span>
                <strong>{v.lap_records_count}</strong>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
