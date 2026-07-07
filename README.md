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

## Structure du projet

```
trajectoire/
├── backend/          # API FastAPI
├── frontend/         # Application React
├── scrapers/         # Collecte de données
├── database/         # Scripts SQL
└── .github/          # CI/CD
```
