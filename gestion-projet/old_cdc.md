# Cahier des charges — Plateforme Trajectoire (Auto & Moto)

## 1. Présentation du projet

**Trajectoire** est une plateforme web d'aide à la planification d'itinéraires et de sorties sur piste, spécialement conçue pour les passionnés de **conduite automobile (sportives, prestige, collection) et de deux-roues (roadsters, sportives, trails, GT)**.

L'objectif est de permettre à un pilote de **choisir précisément où et quand rouler** pour maximiser son plaisir de conduite (recherche de routes sinueuses, panoramas, ou sessions sur circuit), tout en s'adaptant aux spécificités de sa machine (autonomie, qualité du revêtement, largeur des voies). La plateforme permet ensuite de **préparer concrètement sa sortie** (vérifications mécaniques, équipement, respect des contraintes sonores, gestion du relief).

**Zone géographique couverte : La région Auvergne-Rhône-Alpes** (territoire d'exception incluant les grands cols alpins, le Massif central et de nombreux circuits homologués).

## 2. Contexte et objectifs

Un conducteur ou motard passionné fait face à trois problématiques majeures avant de prendre la route :

1. **Où rouler ?** → Trouver des routes adaptées : sinuosité pour le plaisir, mais aussi **qualité du revêtement** (cruciale pour les motos face aux gravillons/nids-de-poule) et largeur de voie (croisements difficiles pour les voitures de sport).
2. **Quand partir ?** → Anticiper la viabilité hivernale (fermeture des cols de haute altitude), les fortes chaleurs et consulter le calendrier des journées de roulage libre (*trackdays* auto / moto).
3. **Comment se préparer ?** → Adapter son équipement (cuir/dorsale pour la moto, casque sur circuit), anticiper les limites sonores et adopter un comportement éco-responsable.

### Objectifs
- Visualiser la topologie, l'indice de sinuosité et l'état des routes de la région.
- Identifier les périodes d'ouverture des cols et centraliser les dates de roulage sur circuit, séparées par type de véhicule (Auto / Moto).
- Fournir des fiches techniques par itinéraire (avec alertes d'autonomie) et des check-lists de préparation mécanique spécifiques (2 ou 4 roues).

## 3. Périmètre fonctionnel

### 3.1 Carte interactive avec heatmap de sinuosité et points de vigilance
- Carte affichant une **heatmap** (carte de chaleur) basée sur l'indice de sinuosité des routes.
- Affichage différencié des **points de vigilance** : zones fréquentes de gravillons, cols sans glissières de sécurité doublées (motards), passages canadiens.
- Superposition des tracés de cols majeurs et localisation des circuits automobiles/motos homologués.

### 3.2 Filtrage par mode de conduite (Auto / Moto) et multicritères
- **Sélecteur de mode (Auto / Moto)** adaptant automatiquement les recommandations et les distances entre les points d'intérêt (les motos ayant souvent une autonomie plus réduite : 150-250 km).
- Sélection par **profil de parcours** : pourcentage moyen de pente, largeur de la route, possibilité de sélectionner des chemins carrossables (pour les motos Trails/Adventure).
- Filtrage des circuits selon l'homologation (Auto/Moto) et les **limites sonores** autorisées (ex: 95 dB, 100 dB, échappement d'origine exigé).

### 3.3 Frise chronologique et calendrier des disponibilités
- **Frise temporelle annuelle** indiquant les périodes historiques d'ouverture et de fermeture des cols alpins.
- Calendrier agrégé des journées de roulage (*trackdays*), avec un code couleur clair distinguant les **sessions Auto**, **sessions Moto**, et **sessions Mixtes**.

### 3.4 Fiches techniques des tracés et circuits
Chaque tracé ou circuit dispose d'une fiche descriptive détaillée :
- **Pour les routes/cols :** profil altimétrique, présence de stations-services rapprochées (SP98), typologie des parkings panoramiques (alerte si parking en fort dévers, très compliqué pour stationner une moto lourde).
- **Pour les circuits :** longueur, dégagements (bacs à graviers vs asphalte), compresseurs/prises électriques disponibles, consignes pour les paddocks.

### 3.5 Conseils de préparation et charte de bonne conduite
- **Check-lists spécifiques selon le profil :**
  - *Moto* : Pression des pneus, tension/graissage de la chaîne, équipement du pilote (dorsale, sliders), fatigue physique (prévoir des pauses tous les 100km en montagne).
  - *Auto* : Purge liquide de frein HTX, gestion thermique moteur, pressions à chaud.
- **Éthique et environnement :** sensibilisation aux nuisances sonores, règles de dépassement sécurisé (cyclistes pour les autos, files de voitures pour les motos en respectant les distances).

## 4. Sources de données

- Source principale : **OpenStreetMap (OSM)** — géométrie des routes, attributs de surface, largeur.
- **Données de viabilité hivernale** : Flux open data des conseils départementaux et de Bison Futé.
- **Référentiel des circuits** : Base de données du Ministère des Sports + scrapping éthique / API des calendriers de trackdays.
- **Données communautaires (Crowdsourcing)** : Permettre aux utilisateurs (notamment les motards) de signaler l'état des routes (présence de gravillons suite à des "point-à-temps", gasoil sur la chaussée).

## 5. Contraintes techniques

### Backend & Base de données
- **Python** + **FastAPI**.
- Base de données **PostgreSQL + PostGIS** pour stocker les objets géographiques et exécuter les requêtes spatiales.
- Architecture gérant des profils d'utilisateurs distincts ou des préférences de filtrage persistantes (Auto vs Moto).

### Frontend & Ergonomie mobile ("Mode Gants")
- **React (TypeScript)** + **MapLibre GL JS**.
- **Ergonomie spécifique Moto :** Interface mobile optimisée avec des zones de clics larges (utilisable avec des gants d'été compatibles écrans tactiles) et un contraste très élevé pour une lisibilité en plein soleil sur un support guidon/quadlock.

### Conteneurisation
- **Docker** (et docker-compose) pour orchestrer backend, base de données et frontend.

## 6. Livrables

- Application web fonctionnelle (backend FastAPI + interface).
- Environnement conteneurisé via Docker.
- Documentation d'installation et d'utilisation.

## 7. Évolutions envisageables (hors périmètre initial)

- Export des itinéraires au format **GPX / KML / ITN** pour intégration dans les GPS Auto (CarPlay/Android Auto) ou Moto (TomTom Rider, Garmin Zumo, Calimoto, Kurviger).
- Couplage avec une API météo en temps réel (alerte pluie/verglas/vent fort, particulièrement sensible pour les deux-roues).
- Module de création de "Roadbooks" partagés pour les clubs (Clubs Porsche, groupes de motards, etc.).