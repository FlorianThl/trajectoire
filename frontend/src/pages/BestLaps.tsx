import { useEffect, useState } from "react"
import { api, type LapRecordRead, type CircuitSearchResult, type VehicleRead, type LapProgressionStats } from "../services/api"
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid } from "recharts"

function parseLapTime(t: string): number {
  const parts = t.replace(",", ".").split(":").map(Number)
  if (parts.length === 3) return parts[0]*3600 + parts[1]*60 + parts[2]
  if (parts.length === 2) return parts[0]*60 + parts[1]
  return parts[0]
}

export function BestLaps() {
  const [laps, setLaps] = useState<LapRecordRead[]>([])
  const [circuits, setCircuits] = useState<CircuitSearchResult[]>([])
  const [vehicles, setVehicles] = useState<VehicleRead[]>([])
  const [progression, setProgression] = useState<LapProgressionStats[]>([])
  const [loading, setLoading] = useState(true)
  const [showForm, setShowForm] = useState(false)
  const [form, setForm] = useState({
    circuit_id: "",
    vehicle_id: "",
    lap_time: "",
    lap_number: "",
    total_laps_session: "",
    notes: "",
  })
  const [error, setError] = useState("")

  async function load() {
    setLoading(true)
    try {
      const [l, c, v, p] = await Promise.all([
        api.laps.list(),
        api.circuits.search({}),
        api.vehicles.list(),
        api.laps.progression(),
      ])
      setLaps(l)
      setCircuits(c)
      setVehicles(v)
      setProgression(p)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => { load() }, [])

  function resetForm() {
    setForm({ circuit_id: "", vehicle_id: "", lap_time: "", lap_number: "", total_laps_session: "", notes: "" })
    setShowForm(false)
    setError("")
  }

  function update(field: string, value: string) {
    setForm((prev) => ({ ...prev, [field]: value }))
  }

  async function handleSubmit() {
    setError("")
    if (!form.circuit_id || !form.lap_time) {
      setError("Circuit et temps au tour sont requis")
      return
    }
    try {
      await api.laps.create({
        circuit_id: form.circuit_id,
        vehicle_id: form.vehicle_id || null,
        lap_time: form.lap_time,
        lap_number: form.lap_number ? Number(form.lap_number) : null,
        total_laps_session: form.total_laps_session ? Number(form.total_laps_session) : null,
        notes: form.notes || null,
      })
      resetForm()
      await load()
    } catch (err) {
      setError(err instanceof Error ? err.message : "Erreur")
    }
  }

  async function handleDelete(id: string) {
    if (!confirm("Supprimer ce chrono ?")) return
    try {
      await api.laps.delete(id)
      await load()
    } catch (err) {
      alert(err instanceof Error ? err.message : "Erreur")
    }
  }

  const circuitName = (id: string) => circuits.find((c) => c.id === id)?.name || id.slice(0, 8)
  const vehicleName = (id: string | null) => {
    if (!id) return "-"
    const v = vehicles.find((v) => v.id === id)
    return v ? `${v.brand} ${v.model}` : id.slice(0, 8)
  }

  if (loading) return <div className="page"><p>Chargement...</p></div>

  const bestByCircuit = laps.reduce<Record<string, LapRecordRead>>((acc, lap) => {
    if (!acc[lap.circuit_id] || parseLapTime(lap.lap_time) < parseLapTime(acc[lap.circuit_id].lap_time)) {
      acc[lap.circuit_id] = lap
    }
    return acc
  }, {})

  return (
    <div className="page">
      <div className="page-header">
        <h1>Meilleurs tours</h1>
        <button onClick={() => { resetForm(); setShowForm(true) }} className="btn">+ Ajouter un chrono</button>
        <button onClick={api.laps.exportCsv} className="btn secondary">Exporter CSV</button>
      </div>

      {error && <p className="error">{error}</p>}

      {showForm && (
        <div className="card">
          <h2>Nouveau chrono</h2>
          <div className="field-row">
            <label>
              Circuit
              <select value={form.circuit_id} onChange={(e) => update("circuit_id", e.target.value)} required>
                <option value="">Selectionner...</option>
                {circuits.map((c) => <option key={c.id} value={c.id}>{c.name}</option>)}
              </select>
            </label>
            <label>
              Vehicule
              <select value={form.vehicle_id} onChange={(e) => update("vehicle_id", e.target.value)}>
                <option value="">-</option>
                {vehicles.map((v) => <option key={v.id} value={v.id}>{v.brand} {v.model}</option>)}
              </select>
            </label>
          </div>
          <div className="field-row">
            <label>
              Temps (ex: 1:18.200)
              <input value={form.lap_time} onChange={(e) => update("lap_time", e.target.value)} placeholder="1:18.200" required />
            </label>
            <label>
              N° tour
              <input type="number" value={form.lap_number} onChange={(e) => update("lap_number", e.target.value)} />
            </label>
            <label>
              Tours dans la session
              <input type="number" value={form.total_laps_session} onChange={(e) => update("total_laps_session", e.target.value)} />
            </label>
          </div>
          <label>
            Notes
            <input value={form.notes} onChange={(e) => update("notes", e.target.value)} placeholder="Conditions, sensations..." />
          </label>
          <div className="btn-row">
            <button onClick={handleSubmit} className="btn">Ajouter</button>
            <button onClick={resetForm} className="btn secondary">Annuler</button>
          </div>
        </div>
      )}

      {laps.length === 0 ? (
        <p className="empty">Aucun chrono enregistre. Ajoutez vos premiers tours !</p>
      ) : (
        <>
          <h2>Meilleurs chronos par circuit</h2>
          <div className="laps-grid">
            {Object.entries(bestByCircuit).map(([circuitId, lap]) => (
              <div key={circuitId} className="card lap-card best">
                <h3>{circuitName(circuitId)}</h3>
                <p className="lap-time">{lap.lap_time}</p>
                <p className="lap-vehicle">{vehicleName(lap.vehicle_id)}</p>
              </div>
            ))}
          </div>

          {progression.length > 0 && (
            <>
              <h2 style={{ marginTop: "2rem" }}>Progression par circuit</h2>
              <div className="progression-grid">
                {progression.map((p) => (
                  <div key={p.circuit_id} className="card">
                    <h3>{p.circuit_name}</h3>
                    <p>Meilleur temps : <strong>{p.best_lap}</strong></p>
                    <ResponsiveContainer width="100%" height={200}>
                      <LineChart data={p.laps}>
                        <CartesianGrid strokeDasharray="3 3" />
                        <XAxis dataKey="date" tick={{ fontSize: 11 }} />
                        <YAxis domain={["dataMin - 2", "dataMax + 2"]} tick={{ fontSize: 11 }} />
                        <Tooltip />
                        <Line type="monotone" dataKey="seconds" stroke="#e63946" dot={{ r: 4 }} />
                      </LineChart>
                    </ResponsiveContainer>
                  </div>
                ))}
              </div>
            </>
          )}

          <h2 style={{ marginTop: "2rem" }}>Tous les chronos</h2>
          <div className="laps-list">
            {laps.map((lap) => (
              <div key={lap.id} className="card lap-card">
                <div className="lap-header">
                  <h3>{circuitName(lap.circuit_id)}</h3>
                  <button onClick={() => handleDelete(lap.id)} className="btn danger small">Supprimer</button>
                </div>
                <p className="lap-time">{lap.lap_time}</p>
                <p>{vehicleName(lap.vehicle_id)}</p>
                {lap.total_laps_session && <p>{lap.total_laps_session} tours dans la session</p>}
                {lap.notes && <p className="lap-notes">{lap.notes}</p>}
                <p className="lap-date">{new Date(lap.created_at).toLocaleDateString("fr-FR")}</p>
              </div>
            ))}
          </div>
        </>
      )}
    </div>
  )
}
