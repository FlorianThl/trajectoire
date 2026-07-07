# Trajectoire — Plateforme Trackdays

Centralisation des calendriers de roulage sur circuit avec filtrage intelligent (bruit, licence, géolocalisation).

## Stack

| Composant | Technologie |
|-----------|-------------|
| Base de Données | PostgreSQL + PostGIS |
| Backend | Python / FastAPI |
| Frontend | React + TypeScript |
| Cartographie | MapLibre GL JS |
| Dataviz | Recharts |
| Infrastructure | Docker |

## Démarrage rapide

```bash
cp .env.example .env
docker compose up -d
```

Accès :
- API : http://localhost:8000
- Documentation API : http://localhost:8000/docs
- Frontend : http://localhost:3000

## Fonctionnalités (V1)

| Module | Description |
|--------|-------------|
| **Profil Pilote** | Inscription, connexion JWT, statut légal (licencié FFSA/FFM), niveau |
| **Garage Virtuel** | Gestion des véhicules, configuration piste (dB, pneus, freins) |
| **Recherche Circuits** | Filtrage auto-adaptatif (bruit), multicritères (rayon, dates, niveau), carte MapLibre |
| **Réservation** | Redirection traçable vers les organisateurs, scrapers M2R et RS Trackdays |
| **Télémétrie** | Chronos, meilleurs tours, progression Recharts, CV mécanique |
| **Entretien** | Suivi d'usure des consommables, alertes à 80%, jauges de progression |

## Structure du projet

```
trajectoire/
├── backend/          # API FastAPI (Python)
│   ├── app/
│   │   ├── routers/      # Endpoints REST
│   │   ├── models/       # SQLAlchemy ORM
│   │   ├── schemas/      # Pydantic validation
│   │   ├── config.py     # Configuration
│   │   ├── database.py   # Connexion PostgreSQL + PostGIS
│   │   └── dependencies.py
│   ├── tests/            # Tests pytest-asyncio
│   └── requirements.txt
├── frontend/         # Application React + TypeScript
│   ├── src/
│   │   ├── pages/        # Pages (Garage, Circuits, BestLaps, ...)
│   │   ├── components/   # Layout, ProtectedRoute
│   │   ├── contexts/     # AuthContext (JWT)
│   │   └── services/     # API client
│   └── package.json
├── scrapers/         # Collecte de données (M2R, RS Trackdays)
│   └── src/              # BaseScraper, scrapers par organisateur
├── database/         # Scripts SQL (init, seed)
└── .github/          # CI/CD (GitHub Actions)
```

## API

Documentation interactive : http://localhost:8000/docs (Swagger/OpenAPI)

Principaux endpoints :

| Méthode | Path | Description |
|---------|------|-------------|
| POST | `/auth/register` | Création de compte |
| POST | `/auth/login` | Connexion (JWT) |
| GET | `/circuits` | Recherche circuits (filtres: lat, lon, radius, noise, dates) |
| GET | `/circuits/{id}` | Détail circuit |
| GET | `/circuits/{id}/events` | Événements d'un circuit |
| GET/POST | `/vehicles` | Liste / Création véhicule |
| GET/POST | `/laps` | Liste / Création chrono |
| GET | `/laps/stats/progression` | Progression par circuit (Recharts) |
| GET | `/laps/export/csv` | Export CSV des chronos |
| GET | `/laps/stats/vehicle` | CV Mécanique par véhicule |
| GET/POST | `/vehicles/{id}/maintenance` | Liste / Création suivi d'usure |

## Scrapers

```bash
# Lancer manuellement
docker compose --profile scrapers run scrapers

# En arrière-plan
docker compose --profile scrapers up -d scrapers
```

## Tests

```bash
cd backend
pip install -r requirements.txt
pytest -v
```

## CI/CD

- **CI** : lint, typecheck, build, tests (sur chaque push)
- **CD** : build & push des images Docker vers GitHub Container Registry (sur tag v*)
