const API_BASE = "/api"

class ApiError extends Error {
  constructor(public status: number, message: string) {
    super(message)
    this.name = "ApiError"
  }
}

async function request<T>(path: string, options: RequestInit = {}): Promise<T> {
  const token = localStorage.getItem("token")
  const headers: Record<string, string> = {
    "Content-Type": "application/json",
    ...(options.headers as Record<string, string>),
  }
  if (token) headers["Authorization"] = `Bearer ${token}`

  const res = await fetch(`${API_BASE}${path}`, { ...options, headers })
  if (!res.ok) {
    const body = await res.json().catch(() => ({ detail: res.statusText }))
    throw new ApiError(res.status, body.detail || "Request failed")
  }
  if (res.status === 204) return undefined as T
  return res.json()
}

export interface UserRead {
  id: string
  email: string
  first_name: string
  last_name: string
  phone: string | null
  category: string
  license_type: string
  license_number: string | null
  license_expiry: string | null
  address: string | null
  city: string | null
  postal_code: string | null
  country: string | null
  level: string
  is_active: boolean
}

export interface UserUpdate {
  first_name?: string
  last_name?: string
  phone?: string | null
  category?: string
  license_type?: string
  license_number?: string | null
  license_expiry?: string | null
  address?: string | null
  city?: string | null
  postal_code?: string | null
  country?: string | null
  level?: string
}

export interface UserCreate {
  email: string
  password: string
  first_name: string
  last_name: string
  phone?: string
  category?: string
  license_type?: string
  license_number?: string
  license_expiry?: string
  address?: string
  city?: string
  postal_code?: string
  country?: string
  level?: string
}

export interface TokenResponse {
  access_token: string
  token_type: string
}

export interface VehicleRead {
  id: string
  user_id: string
  vehicle_type: string
  brand: string
  model: string
  year: number
  tires: string | null
  brakes: string | null
  noise_level_db: number | null
  total_laps: number
  total_track_km: number | null
  is_active: boolean
}

export interface VehicleCreate {
  vehicle_type: string
  brand: string
  model: string
  year: number
  tires?: string
  brakes?: string
  noise_level_db?: number | null
}

export interface VehicleUpdate {
  vehicle_type?: string
  brand?: string
  model?: string
  year?: number
  tires?: string
  brakes?: string
  noise_level_db?: number | null
}

export interface CircuitSearchResult {
  id: string
  name: string
  slug: string
  city: string | null
  length_km: number | null
  noise_limit_db: number | null
  has_noise_restriction: boolean
  allowed_categories: string[] | null
  image_url: string | null
  distance_km: number | null
  events_count: number
  lat: number | null
  lon: number | null
}

export interface CircuitRead {
  id: string
  name: string
  slug: string
  description: string | null
  address: string | null
  city: string | null
  postal_code: string | null
  country: string | null
  length_km: number | null
  layout_type: string | null
  runoff_areas: string | null
  has_electricity: boolean
  has_compressor: boolean
  has_fuel_station: boolean
  noise_limit_db: number | null
  has_noise_restriction: boolean
  allowed_categories: string[] | null
  image_url: string | null
  website_url: string | null
  is_active: boolean
  created_at: string
}

export interface EventRead {
  id: string
  circuit_id: string
  circuit_name: string | null
  organizer_name: string
  organizer_url: string | null
  start_date: string
  end_date: string
  has_debutant: boolean
  has_intermediaire: boolean
  has_confirme: boolean
  price_base: number | null
  price_license: number | null
  booking_url: string | null
  spots_available: number | null
  is_active: boolean
  created_at: string
}

export interface MaintenanceLogRead {
  id: string
  vehicle_id: string
  consumable: string
  max_laps: number
  current_laps: number
  wear_percent: number | null
  last_replaced_at: string | null
  alert_threshold: number
  is_alerted: boolean | null
}

export interface MaintenanceLogCreate {
  consumable: string
  max_laps: number
  alert_threshold?: number
}

export interface LapRecordRead {
  id: string
  user_id: string
  vehicle_id: string | null
  circuit_id: string
  event_id: string | null
  lap_time: string
  lap_number: number | null
  total_laps_session: number | null
  notes: string | null
  validated_at: string | null
  created_at: string
}

export interface LapRecordCreate {
  vehicle_id?: string | null
  circuit_id: string
  event_id?: string | null
  lap_time: string
  lap_number?: number | null
  total_laps_session?: number | null
  notes?: string | null
}

export const api = {
  auth: {
    login: (data: { email: string; password: string }) =>
      request<TokenResponse>("/auth/login", { method: "POST", body: JSON.stringify(data) }),
    register: (data: UserCreate) =>
      request<UserRead>("/auth/register", { method: "POST", body: JSON.stringify(data) }),
    me: () => request<UserRead>("/auth/me"),
  },
  users: {
    update: (data: UserUpdate) =>
      request<UserRead>("/users/me", { method: "PATCH", body: JSON.stringify(data) }),
    delete: () => request<void>("/users/me", { method: "DELETE" }),
  },
  circuits: {
    search: (params: Record<string, string | number | undefined>) => {
      const qs = Object.entries(params)
        .filter(([, v]) => v !== undefined && v !== "")
        .map(([k, v]) => `${k}=${encodeURIComponent(String(v))}`)
        .join("&")
      return request<CircuitSearchResult[]>(`/circuits?${qs}`)
    },
    get: (id: string) => request<CircuitRead>(`/circuits/${id}`),
    events: (id: string, params?: Record<string, string>) => {
      const qs = params ? "?" + new URLSearchParams(params).toString() : ""
      return request<EventRead[]>(`/circuits/${id}/events${qs}`)
    },
  },
  events: {
    list: (params?: Record<string, string>) => {
      const qs = params ? "?" + new URLSearchParams(params).toString() : ""
      return request<EventRead[]>(`/events${qs}`)
    },
  },
  maintenance: {
    list: (vehicleId: string) => request<MaintenanceLogRead[]>(`/vehicles/${vehicleId}/maintenance`),
    create: (vehicleId: string, data: MaintenanceLogCreate) =>
      request<MaintenanceLogRead>(`/vehicles/${vehicleId}/maintenance`, { method: "POST", body: JSON.stringify(data) }),
    update: (vehicleId: string, logId: string, data: { current_laps?: number; alert_threshold?: number }) =>
      request<MaintenanceLogRead>(`/vehicles/${vehicleId}/maintenance/${logId}`, { method: "PATCH", body: JSON.stringify(data) }),
    delete: (vehicleId: string, logId: string) =>
      request<void>(`/vehicles/${vehicleId}/maintenance/${logId}`, { method: "DELETE" }),
  },
  laps: {
    list: (params?: Record<string, string>) => {
      const qs = params ? "?" + new URLSearchParams(params).toString() : ""
      return request<LapRecordRead[]>(`/laps${qs}`)
    },
    create: (data: LapRecordCreate) =>
      request<LapRecordRead>("/laps", { method: "POST", body: JSON.stringify(data) }),
    delete: (id: string) => request<void>(`/laps/${id}`, { method: "DELETE" }),
  },
  vehicles: {
    list: () => request<VehicleRead[]>("/vehicles"),
    create: (data: VehicleCreate) =>
      request<VehicleRead>("/vehicles", { method: "POST", body: JSON.stringify(data) }),
    get: (id: string) => request<VehicleRead>(`/vehicles/${id}`),
    update: (id: string, data: VehicleUpdate) =>
      request<VehicleRead>(`/vehicles/${id}`, { method: "PATCH", body: JSON.stringify(data) }),
    delete: (id: string) => request<void>(`/vehicles/${id}`, { method: "DELETE" }),
    activate: (id: string) =>
      request<VehicleRead>(`/vehicles/${id}/activate`, { method: "PATCH" }),
  },
}
