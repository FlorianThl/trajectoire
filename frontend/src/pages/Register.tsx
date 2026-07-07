import { useState, type FormEvent } from "react"
import { Link, useNavigate } from "react-router-dom"
import { useAuth } from "../contexts/AuthContext"

export function Register() {
  const { register } = useAuth()
  const navigate = useNavigate()
  const [form, setForm] = useState({
    email: "", password: "", confirmPassword: "",
    first_name: "", last_name: "",
    category: "auto", license_type: "none", level: "debutant",
  })
  const [error, setError] = useState("")

  function update(field: string, value: string) {
    setForm((prev) => ({ ...prev, [field]: value }))
  }

  async function handleSubmit(e: FormEvent) {
    e.preventDefault()
    setError("")
    if (form.password !== form.confirmPassword) {
      setError("Les mots de passe ne correspondent pas")
      return
    }
    try {
      await register({
        email: form.email,
        password: form.password,
        first_name: form.first_name,
        last_name: form.last_name,
        category: form.category,
        license_type: form.license_type,
        level: form.level,
      })
      navigate("/login")
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : "Erreur d'inscription")
    }
  }

  return (
    <div className="form-page">
      <form onSubmit={handleSubmit} className="card form-card">
        <h1>Inscription</h1>
        {error && <p className="error">{error}</p>}

        <div className="field-row">
          <label>Prénom<input value={form.first_name} onChange={(e) => update("first_name", e.target.value)} required /></label>
          <label>Nom<input value={form.last_name} onChange={(e) => update("last_name", e.target.value)} required /></label>
        </div>

        <label>Email<input type="email" value={form.email} onChange={(e) => update("email", e.target.value)} required /></label>

        <div className="field-row">
          <label>Mot de passe<input type="password" value={form.password} onChange={(e) => update("password", e.target.value)} required /></label>
          <label>Confirmation<input type="password" value={form.confirmPassword} onChange={(e) => update("confirmPassword", e.target.value)} required /></label>
        </div>

        <label>
          Catégorie
          <select value={form.category} onChange={(e) => update("category", e.target.value)}>
            <option value="auto">Auto</option>
            <option value="moto">Moto</option>
            <option value="both">Auto & Moto</option>
          </select>
        </label>

        <div className="field-row">
          <label>
            Type de licence
            <select value={form.license_type} onChange={(e) => update("license_type", e.target.value)}>
              <option value="none">Non licencié</option>
              <option value="ffsa">FFSA</option>
              <option value="ffm">FFM</option>
            </select>
          </label>
          <label>
            Niveau
            <select value={form.level} onChange={(e) => update("level", e.target.value)}>
              <option value="debutant">Débutant</option>
              <option value="intermediaire">Intermédiaire</option>
              <option value="confirme">Confirmé</option>
            </select>
          </label>
        </div>

        <button type="submit" className="btn">S'inscrire</button>
        <p className="alt-link">Déjà un compte ? <Link to="/login">Se connecter</Link></p>
      </form>
    </div>
  )
}
