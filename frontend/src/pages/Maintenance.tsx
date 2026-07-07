import { useEffect, useState } from "react"
import { useParams, Link } from "react-router-dom"
import { api, type MaintenanceLogRead, type VehicleRead } from "../services/api"

const CONSUMABLE_LABELS: Record<string, string> = {
  plaquettes: "Plaquettes de frein",
  disques: "Disques de frein",
  huile: "Huile moteur",
  liquide_frein: "Liquide de frein",
  pneus: "Pneumatiques",
}

const CONSUMABLE_OPTIONS = Object.keys(CONSUMABLE_LABELS)

export function Maintenance() {
  const { vehicleId } = useParams<{ vehicleId: string }>()
  const [vehicle, setVehicle] = useState<VehicleRead | null>(null)
  const [logs, setLogs] = useState<MaintenanceLogRead[]>([])
  const [loading, setLoading] = useState(true)

  const [showForm, setShowForm] = useState(false)
  const [form, setForm] = useState({ consumable: "plaquettes", max_laps: "100", alert_threshold: "80" })

  async function load() {
    if (!vehicleId) return
    setLoading(true)
    try {
      const [v, l] = await Promise.all([
        api.vehicles.get(vehicleId),
        api.maintenance.list(vehicleId),
      ])
      setVehicle(v)
      setLogs(l)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => { load() }, [vehicleId])

  function resetForm() {
    setForm({ consumable: "plaquettes", max_laps: "100", alert_threshold: "80" })
    setShowForm(false)
  }

  async function handleAdd() {
    if (!vehicleId) return
    try {
      await api.maintenance.create(vehicleId, {
        consumable: form.consumable,
        max_laps: Number(form.max_laps),
        alert_threshold: Number(form.alert_threshold),
      })
      resetForm()
      await load()
    } catch (err) {
      alert(err instanceof Error ? err.message : "Erreur lors de l'ajout")
    }
  }

  async function handleReset(logId: string) {
    if (!vehicleId) return
    try {
      await api.maintenance.update(vehicleId, logId, { current_laps: 0 })
      await load()
    } catch (err) {
      alert(err instanceof Error ? err.message : "Erreur")
    }
  }

  async function handleDelete(logId: string) {
    if (!vehicleId || !confirm("Supprimer ce suivi ?")) return
    try {
      await api.maintenance.delete(vehicleId, logId)
      await load()
    } catch (err) {
      alert(err instanceof Error ? err.message : "Erreur")
    }
  }

  if (loading) return <div className="page"><p>Chargement...</p></div>
  if (!vehicle) return <div className="page"><p>Vehicule introuvable</p></div>

  return (
    <div className="page">
      <Link to="/garage" className="back-link">{'<-'} Retour au garage</Link>
      <div className="page-header">
        <h1>Carnet d'entretien - {vehicle.brand} {vehicle.model}</h1>
        <button onClick={() => { resetForm(); setShowForm(true) }} className="btn">+ Ajouter un suivi</button>
      </div>

      {showForm && (
        <div className="card">
          <h2>Nouveau suivi</h2>
          <div className="field-row">
            <label>
              Consommable
              <select value={form.consumable} onChange={(e) => setForm((p) => ({ ...p, consumable: e.target.value }))}>
                {CONSUMABLE_OPTIONS.map((c) => (
                  <option key={c} value={c}>{CONSUMABLE_LABELS[c]}</option>
                ))}
              </select>
            </label>
            <label>
              Duree de vie (tours)
              <input type="number" value={form.max_laps} onChange={(e) => setForm((p) => ({ ...p, max_laps: e.target.value }))} />
            </label>
            <label>
              Seuil d'alerte (%)
              <input type="number" min={1} max={100} value={form.alert_threshold} onChange={(e) => setForm((p) => ({ ...p, alert_threshold: e.target.value }))} />
            </label>
          </div>
          <div className="btn-row">
            <button onClick={handleAdd} className="btn">Ajouter</button>
            <button onClick={resetForm} className="btn secondary">Annuler</button>
          </div>
        </div>
      )}

      {logs.length === 0 ? (
        <p className="empty">Aucun suivi d'usure pour ce vehicule.</p>
      ) : (
        <div className="maintenance-grid">
          {logs.map((log) => {
            const wear = log.wear_percent ?? 0
            const alerted = log.is_alerted ?? wear >= log.alert_threshold
            return (
              <div key={log.id} className={`card maintenance-card ${alerted ? "alerted" : ""}`}>
                <div className="maintenance-header">
                  <h3>{CONSUMABLE_LABELS[log.consumable] || log.consumable}</h3>
                  {alerted && <span className="badge danger">Alerte</span>}
                </div>
                <div className="wear-bar-container">
                  <div
                    className="wear-bar"
                    style={{
                      width: `${Math.min(wear, 100)}%`,
                      background: wear >= log.alert_threshold ? "#dc2626" : wear >= log.alert_threshold * 0.75 ? "#f59e0b" : "#2563eb",
                    }}
                  />
                </div>
                <p className="wear-text">{wear.toFixed(0)}% use - {log.current_laps}/{log.max_laps} tours</p>
                <p className="wear-threshold">Seuil d'alerte: {log.alert_threshold}%</p>
                <div className="btn-row">
                  <button onClick={() => handleReset(log.id)} className="btn small">Remettre a zero</button>
                  <button onClick={() => handleDelete(log.id)} className="btn danger small">Supprimer</button>
                </div>
              </div>
            )
          })}
        </div>
      )}
    </div>
  )
}
