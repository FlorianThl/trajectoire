import { useEffect, useState } from "react"
import { Link } from "react-router-dom"
import { api, type VehicleRead } from "../services/api"

export function Garage() {
  const [vehicles, setVehicles] = useState<VehicleRead[]>([])
  const [showForm, setShowForm] = useState(false)
  const [editingId, setEditingId] = useState<string | null>(null)
  const [form, setForm] = useState({
    vehicle_type: "auto", brand: "", model: "", year: 2020,
    tires: "road", brakes: "stock", noise_level_db: "",
  })

  function resetForm() {
    setForm({ vehicle_type: "auto", brand: "", model: "", year: 2020, tires: "road", brakes: "stock", noise_level_db: "" })
    setEditingId(null)
    setShowForm(false)
  }

  function update(field: string, value: string) {
    setForm((prev) => ({ ...prev, [field]: value }))
  }

  async function load() {
    const list = await api.vehicles.list()
    setVehicles(list)
  }

  useEffect(() => { load() }, [])

  async function handleSubmit() {
    if (!form.brand || !form.model) {
      alert("Veuillez renseigner la marque et le modele")
      return
    }
    try {
      const payload = {
        ...form,
        year: Number(form.year),
        noise_level_db: form.noise_level_db ? Number(form.noise_level_db) : null,
      }
      if (editingId) {
        await api.vehicles.update(editingId, payload)
      } else {
        await api.vehicles.create(payload as Parameters<typeof api.vehicles.create>[0])
      }
      resetForm()
      await load()
    } catch (err) {
      alert(err instanceof Error ? err.message : "Erreur lors de l'ajout")
    }
  }

  async function handleEdit(v: VehicleRead) {
    setForm({
      vehicle_type: v.vehicle_type,
      brand: v.brand,
      model: v.model,
      year: v.year,
      tires: v.tires || "road",
      brakes: v.brakes || "stock",
      noise_level_db: v.noise_level_db?.toString() || "",
    })
    setEditingId(v.id)
    setShowForm(true)
  }

  async function handleDelete(id: string) {
    if (!confirm("Supprimer ce véhicule ?")) return
    await api.vehicles.delete(id)
    await load()
  }

  async function handleActivate(id: string) {
    await api.vehicles.activate(id)
    await load()
  }

  return (
    <div className="page">
      <div className="page-header">
        <h1>Mon Garage</h1>
        <button onClick={() => { resetForm(); setShowForm(true) }} className="btn">
          + Ajouter
        </button>
      </div>

      {showForm && (
        <div className="card">
          <h2>{editingId ? "Modifier" : "Ajouter"} un véhicule</h2>
          <div className="field-row">
            <label>
              Type
              <select value={form.vehicle_type} onChange={(e) => update("vehicle_type", e.target.value)}>
                <option value="auto">Auto</option>
                <option value="moto">Moto</option>
              </select>
            </label>
            <label>Marque<input value={form.brand} onChange={(e) => update("brand", e.target.value)} required /></label>
            <label>Modèle<input value={form.model} onChange={(e) => update("model", e.target.value)} required /></label>
          </div>
          <div className="field-row">
            <label>Année<input type="number" min={1980} max={2030} value={form.year} onChange={(e) => update("year", e.target.value)} /></label>
            <label>
              Pneus
              <select value={form.tires} onChange={(e) => update("tires", e.target.value)}>
                <option value="road">Route</option>
                <option value="semi_slicks">Semi-slicks</option>
                <option value="slicks">Slicks</option>
              </select>
            </label>
            <label>
              Freins
              <select value={form.brakes} onChange={(e) => update("brakes", e.target.value)}>
                <option value="stock">Stock</option>
                <option value="sport">Sport</option>
                <option value="racing">Racing</option>
              </select>
            </label>
          </div>
          <label>Niveau sonore (dB)<input type="number" min={80} max={130} step={0.1} value={form.noise_level_db} onChange={(e) => update("noise_level_db", e.target.value)} placeholder="Ex: 102" /></label>
          <div className="btn-row">
            <button onClick={handleSubmit} className="btn">{editingId ? "Enregistrer" : "Ajouter"}</button>
            <button onClick={resetForm} className="btn secondary">Annuler</button>
          </div>
        </div>
      )}

      {vehicles.length === 0 ? (
        <p className="empty">Aucun véhicule dans le garage. Ajoutez-en un !</p>
      ) : (
        <div className="vehicle-grid">
          {vehicles.map((v) => (
            <div key={v.id} className={`card vehicle-card ${v.is_active ? "active" : ""}`}>
              <div className="vehicle-header">
                <h3>{v.brand} {v.model}</h3>
                {v.is_active && <span className="badge">Actif</span>}
              </div>
              <p>{v.year} · {v.vehicle_type === "auto" ? "Auto" : "Moto"}</p>
              <p>Pneus: {v.tires === "slicks" ? "Slicks" : v.tires === "semi_slicks" ? "Semi-slicks" : "Route"}</p>
              <p>Freins: {v.brakes === "racing" ? "Racing" : v.brakes === "sport" ? "Sport" : "Stock"}</p>
              {v.noise_level_db && <p>🔊 {v.noise_level_db} dB</p>}
              <p>CV Mecanique: {v.total_laps} tours · {v.total_track_km ?? 0} km</p>
              <div className="btn-row">
                {!v.is_active && <button onClick={() => handleActivate(v.id)} className="btn small">Activer</button>}
                <Link to={`/garage/${v.id}/maintenance`} className="btn small">Entretien</Link>
                <button onClick={() => handleEdit(v)} className="btn secondary small">Modifier</button>
                <button onClick={() => handleDelete(v.id)} className="btn danger small">Supprimer</button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
