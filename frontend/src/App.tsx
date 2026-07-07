import { Routes, Route } from "react-router-dom"
import { Layout } from "./components/Layout"
import { ProtectedRoute } from "./components/ProtectedRoute"
import { Login } from "./pages/Login"
import { Register } from "./pages/Register"
import { Profile } from "./pages/Profile"
import { Garage } from "./pages/Garage"
import { Circuits } from "./pages/Circuits"
import { CircuitDetail } from "./pages/CircuitDetail"
import { Maintenance } from "./pages/Maintenance"
import { BestLaps } from "./pages/BestLaps"
import { NotFound } from "./pages/NotFound"

export default function App() {
  return (
    <Routes>
      <Route element={<Layout />}>
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="/profil" element={<ProtectedRoute><Profile /></ProtectedRoute>} />
        <Route path="/garage" element={<ProtectedRoute><Garage /></ProtectedRoute>} />
        <Route path="/garage/:vehicleId/maintenance" element={<ProtectedRoute><Maintenance /></ProtectedRoute>} />
        <Route path="/circuits" element={<ProtectedRoute><Circuits /></ProtectedRoute>} />
        <Route path="/circuits/:id" element={<ProtectedRoute><CircuitDetail /></ProtectedRoute>} />
        <Route path="/meilleurs-tours" element={<ProtectedRoute><BestLaps /></ProtectedRoute>} />
        <Route path="*" element={<NotFound />} />
      </Route>
    </Routes>
  )
}
