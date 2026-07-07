import { useState } from "react"
import { Link } from "react-router-dom"
import { useAuth } from "../contexts/AuthContext"
import { api } from "../services/api"

export function Profile() {
  const { user } = useAuth()
  const [editing, setEditing] = useState(false)
  const [form, setForm] = useState({
    first_name: user?.first_name || "",
    last_name: user?.last_name || "",
    phone: user?.phone || "",
    address: user?.address || "",
    city: user?.city || "",
    postal_code: user?.postal_code || "",
    license_type: user?.license_type || "none",
    license_number: user?.license_number || "",
    level: user?.level || "debutant",
  })
  const [saving, setSaving] = useState(false)

  function update(field: string, value: string) {
    setForm((prev) => ({ ...prev, [field]: value }))
  }

  async function handleSave() {
    setSaving(true)
    try {
      await api.users.update(form)
      await api.auth.me()
      setEditing(false)
    } catch {
      alert("Erreur lors de la sauvegarde")
    } finally {
      setSaving(false)
    }
  }

  if (!user) return null

  return (
    <div className="page">
      <h1>Mon Profil</h1>

      <div className="card">
        {!editing ? (
          <>
            <div className="profile-info">
              <p><strong>{user.first_name} {user.last_name}</strong></p>
              <p>{user.email}</p>
              {user.phone && <p>Tél: {user.phone}</p>}
              <p>Catégorie: {user.category === "auto" ? "Auto" : user.category === "moto" ? "Moto" : "Auto & Moto"}</p>
              <p>Licence: {user.license_type === "none" ? "Non licencié" : user.license_type.toUpperCase()}{user.license_number ? ` (${user.license_number})` : ""}</p>
              <p>Niveau: {user.level}</p>
              {user.city && <p>{user.address}, {user.postal_code} {user.city}</p>}
            </div>
            <button onClick={() => setEditing(true)} className="btn">Modifier</button>
            <Link to="/garage" className="btn secondary" style={{ marginLeft: "0.5rem" }}>Mon Garage</Link>
          </>
        ) : (
          <>
            <div className="field-row">
              <label>Prénom<input value={form.first_name} onChange={(e) => update("first_name", e.target.value)} /></label>
              <label>Nom<input value={form.last_name} onChange={(e) => update("last_name", e.target.value)} /></label>
            </div>
            <label>Téléphone<input value={form.phone} onChange={(e) => update("phone", e.target.value)} /></label>
            <label>Adresse<input value={form.address} onChange={(e) => update("address", e.target.value)} /></label>
            <div className="field-row">
              <label>Ville<input value={form.city} onChange={(e) => update("city", e.target.value)} /></label>
              <label>Code postal<input value={form.postal_code} onChange={(e) => update("postal_code", e.target.value)} /></label>
            </div>
            <div className="field-row">
              <label>
                Licence
                <select value={form.license_type} onChange={(e) => update("license_type", e.target.value)}>
                  <option value="none">Non licencié</option>
                  <option value="ffsa">FFSA</option>
                  <option value="ffm">FFM</option>
                </select>
              </label>
              <label>N° licence<input value={form.license_number} onChange={(e) => update("license_number", e.target.value)} /></label>
            </div>
            <label>
              Niveau
              <select value={form.level} onChange={(e) => update("level", e.target.value)}>
                <option value="debutant">Débutant</option>
                <option value="intermediaire">Intermédiaire</option>
                <option value="confirme">Confirmé</option>
              </select>
            </label>
            <div className="btn-row">
              <button onClick={handleSave} className="btn" disabled={saving}>{saving ? "Sauvegarde..." : "Sauvegarder"}</button>
              <button onClick={() => setEditing(false)} className="btn secondary">Annuler</button>
            </div>
          </>
        )}
      </div>
    </div>
  )
}
