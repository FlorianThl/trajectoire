-- Trajectoire - Schéma de base de données PostgreSQL/PostGIS
-- Sprint 1 : tables fondamentales

CREATE EXTENSION IF NOT EXISTS postgis;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ============================================================
-- 1. UTILISATEURS
-- ============================================================
CREATE TYPE license_type AS ENUM ('ffsa', 'ffm', 'none');
CREATE TYPE pilot_category AS ENUM ('auto', 'moto', 'both');

CREATE TABLE users (
    id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email           VARCHAR(255) UNIQUE NOT NULL,
    password_hash   VARCHAR(255) NOT NULL,
    first_name      VARCHAR(100) NOT NULL,
    last_name       VARCHAR(100) NOT NULL,
    phone           VARCHAR(20),
    category        pilot_category NOT NULL DEFAULT 'auto',
    license_type    license_type NOT NULL DEFAULT 'none',
    license_number  VARCHAR(50),
    license_expiry  DATE,
    -- Adresse pour géolocalisation
    address         TEXT,
    city            VARCHAR(100),
    postal_code     VARCHAR(10),
    country         VARCHAR(100) DEFAULT 'France',
    location        GEOGRAPHY(Point, 4326),
    -- Niveau pilote
    level           VARCHAR(20) NOT NULL DEFAULT 'debutant'
                    CHECK (level IN ('debutant', 'intermediaire', 'confirme')),
    is_active       BOOLEAN DEFAULT true,
    created_at      TIMESTAMPTZ DEFAULT NOW(),
    updated_at      TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_location ON users USING GIST(location);

-- ============================================================
-- 2. VÉHICULES (Garage Virtuel)
-- ============================================================
CREATE TYPE vehicle_type AS ENUM ('auto', 'moto');
CREATE TYPE tire_type AS ENUM ('slicks', 'semi_slicks', 'road');
CREATE TYPE brake_type AS ENUM ('stock', 'sport', 'racing');

CREATE TABLE vehicles (
    id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id         UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    vehicle_type    vehicle_type NOT NULL,
    brand           VARCHAR(100) NOT NULL,
    model           VARCHAR(100) NOT NULL,
    year            INTEGER NOT NULL CHECK (year >= 1980 AND year <= 2030),
    -- Setup piste
    tires           tire_type DEFAULT 'road',
    brakes          brake_type DEFAULT 'stock',
    noise_level_db  DECIMAL(5,1) CHECK (noise_level_db >= 80 AND noise_level_db <= 130),
    -- CV Mécanique
    total_laps      INTEGER DEFAULT 0,
    total_track_km  DECIMAL(10,1) DEFAULT 0,
    is_active       BOOLEAN DEFAULT false,
    created_at      TIMESTAMPTZ DEFAULT NOW(),
    updated_at      TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_vehicles_user ON vehicles(user_id);
CREATE INDEX idx_vehicles_active ON vehicles(user_id, is_active) WHERE is_active = true;

-- ============================================================
-- 3. CIRCUITS
-- ============================================================
CREATE TABLE circuits (
    id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name            VARCHAR(200) NOT NULL,
    slug            VARCHAR(200) UNIQUE NOT NULL,
    description     TEXT,
    -- Localisation
    address         TEXT,
    city            VARCHAR(100),
    postal_code     VARCHAR(10),
    country         VARCHAR(100) DEFAULT 'France',
    location        GEOGRAPHY(Point, 4326) NOT NULL,
    -- Caractéristiques techniques
    length_km       DECIMAL(6,3),
    layout_type     VARCHAR(50) DEFAULT 'permanent',
    runoff_areas    VARCHAR(50) DEFAULT 'asphalte'
                    CHECK (runoff_areas IN ('asphalte', 'graviers', 'mixte')),
    -- Commodités
    has_electricity BOOLEAN DEFAULT false,
    has_compressor  BOOLEAN DEFAULT false,
    has_fuel_station BOOLEAN DEFAULT false,
    -- Restrictions sonores
    noise_limit_db  DECIMAL(5,1) CHECK (noise_limit_db >= 80 AND noise_limit_db <= 130),
    has_noise_restriction BOOLEAN DEFAULT false,
    -- Catégorie autorisée
    allowed_categories VARCHAR(20)[] DEFAULT '{auto}',
    -- Métadonnées
    image_url       TEXT,
    website_url     TEXT,
    is_active       BOOLEAN DEFAULT true,
    created_at      TIMESTAMPTZ DEFAULT NOW(),
    updated_at      TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_circuits_location ON circuits USING GIST(location);
CREATE INDEX idx_circuits_noise ON circuits(noise_limit_db) WHERE has_noise_restriction = true;
CREATE INDEX idx_circuits_slug ON circuits(slug);

-- ============================================================
-- 4. ÉVÉNEMENTS (Trackdays)
-- ============================================================
CREATE TABLE events (
    id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    circuit_id      UUID NOT NULL REFERENCES circuits(id) ON DELETE CASCADE,
    organizer_name  VARCHAR(200) NOT NULL,
    organizer_url   TEXT,
    -- Date
    start_date      DATE NOT NULL,
    end_date        DATE NOT NULL,
    -- Groupes de niveau
    has_debutant    BOOLEAN DEFAULT false,
    has_intermediaire BOOLEAN DEFAULT false,
    has_confirme    BOOLEAN DEFAULT false,
    -- Tarifs
    price_base      DECIMAL(8,2),
    price_license   DECIMAL(8,2),
    -- Booking
    booking_url     TEXT,
    spots_available INTEGER,
    -- Métadonnées
    is_active       BOOLEAN DEFAULT true,
    scraped_at      TIMESTAMPTZ,
    created_at      TIMESTAMPTZ DEFAULT NOW(),
    updated_at      TIMESTAMPTZ DEFAULT NOW(),
    CONSTRAINT valid_dates CHECK (end_date >= start_date)
);

CREATE INDEX idx_events_circuit ON events(circuit_id);
CREATE INDEX idx_events_dates ON events(start_date, end_date);
CREATE INDEX idx_events_active ON events(is_active) WHERE is_active = true;

-- ============================================================
-- 5. HISTORIQUE PILOTE (Best Laps)
-- ============================================================
CREATE TABLE lap_records (
    id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id         UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    vehicle_id      UUID REFERENCES vehicles(id) ON DELETE SET NULL,
    circuit_id      UUID NOT NULL REFERENCES circuits(id) ON DELETE CASCADE,
    event_id        UUID REFERENCES events(id) ON DELETE SET NULL,
    lap_time        INTERVAL NOT NULL,
    lap_number      INTEGER,
    -- Contexte
    total_laps_session INTEGER,
    notes           TEXT,
    validated_at    TIMESTAMPTZ DEFAULT NOW(),
    created_at      TIMESTAMPTZ DEFAULT NOW(),
    updated_at      TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_laps_user ON lap_records(user_id);
CREATE INDEX idx_laps_circuit ON lap_records(circuit_id);

-- ============================================================
-- 6. CARNET D'ENTRETIEN PRÉDICTIF
-- ============================================================
CREATE TYPE consumable_type AS ENUM ('plaquettes', 'disques', 'huile', 'liquide_frein', 'pneus');

CREATE TABLE maintenance_logs (
    id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    vehicle_id      UUID NOT NULL REFERENCES vehicles(id) ON DELETE CASCADE,
    consumable      consumable_type NOT NULL,
    -- Seuils
    max_laps        INTEGER NOT NULL,
    current_laps    INTEGER DEFAULT 0,
    wear_percent    DECIMAL(5,2) GENERATED ALWAYS AS
                    ((current_laps::DECIMAL / NULLIF(max_laps, 0)) * 100) STORED,
    -- Statut
    last_replaced_at TIMESTAMPTZ,
    alert_threshold DECIMAL(5,2) DEFAULT 80.00,
    is_alerted      BOOLEAN GENERATED ALWAYS AS
                    ((current_laps::DECIMAL / NULLIF(max_laps, 0)) * 100 >= alert_threshold) STORED,
    created_at      TIMESTAMPTZ DEFAULT NOW(),
    updated_at      TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_maintenance_vehicle ON maintenance_logs(vehicle_id);
CREATE INDEX idx_maintenance_alert ON maintenance_logs(is_alerted) WHERE is_alerted = true;

-- ============================================================
-- Triggers : updated_at automatique
-- ============================================================
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_users_updated_at
    BEFORE UPDATE ON users FOR EACH ROW EXECUTE FUNCTION update_updated_at();
CREATE TRIGGER trg_vehicles_updated_at
    BEFORE UPDATE ON vehicles FOR EACH ROW EXECUTE FUNCTION update_updated_at();
CREATE TRIGGER trg_circuits_updated_at
    BEFORE UPDATE ON circuits FOR EACH ROW EXECUTE FUNCTION update_updated_at();
CREATE TRIGGER trg_events_updated_at
    BEFORE UPDATE ON events FOR EACH ROW EXECUTE FUNCTION update_updated_at();
CREATE TRIGGER trg_maintenance_updated_at
    BEFORE UPDATE ON maintenance_logs FOR EACH ROW EXECUTE FUNCTION update_updated_at();
CREATE TRIGGER trg_lap_records_updated_at
    BEFORE UPDATE ON lap_records FOR EACH ROW EXECUTE FUNCTION update_updated_at();
