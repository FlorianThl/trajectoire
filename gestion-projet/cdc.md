# DOCUMENT DE SPÉCIFICATIONS FONCTIONNELLES ET TECHNIQUES (Cahier des Charges)

**Projet :** Plateforme "Trajectoire" (Module Trackdays)
**Version :** 1.0 (Lancement Initial - V1)
**Statut :** Pour validation
**Date :** Juillet 2026

---

## 1. Présentation du Projet et Contexte

**Trajectoire** est une plateforme web logicielle (SaaS) de référence destinée aux passionnés de pilotage **Automobile (sportive, piste)** et **Moto**. 

Le projet vise à résoudre la fragmentation de l'information dans le domaine des journées de roulage sur circuit (*Trackdays*). L'application centralise les calendriers d'événements et propose un système de filtrage intelligent basé sur les caractéristiques réelles du véhicule de l'utilisateur (notamment les restrictions sonores). 

La plateforme agit comme un écosystème complet intégrant un **Profil Pilote**, un **Garage Virtuel**, le suivi des démarches administratives (licences) et l'analyse de la télémétrie.

> *Note de périmètre : Le développement du module "Route" (planification de road-trips et balades) est expressément exclu du périmètre de cette V1 et fait l'objet d'un lotissement ultérieur (V2).*

---

## 2. Exigences Fonctionnelles (Périmètre V1)

L'application garantit une étanchéité totale entre les univers **Auto** et **Moto**. L'utilisateur ne se voit proposer que des environnements de roulage adaptés à sa catégorie.

### 2.1. Gestion des Utilisateurs et "Garage Virtuel"

| ID | Fonctionnalité | Description |
| :--- | :--- | :--- |
| **FCT-01** | **Profil Pilote & Administratif** | Création de compte utilisateur incluant la saisie du statut légal (Licencié FFSA, Licencié FFM, ou non-licencié). Adaptation dynamique de la tarification (déduction automatique de l'assurance RC Piste si applicable) et déblocage des événements restreints. |
| **FCT-02** | **Garage Virtuel** | Interface d'ajout et de gestion de véhicules (Auto/Moto) avec saisie de la marque, modèle, et année. |
| **FCT-03** | **Configuration "Setup Piste"** | Renseignement détaillé de la configuration de chaque véhicule : type de pneumatiques (slicks, semi-slicks), type de freinage, et **relevé certifié des émissions sonores de l'échappement (en décibels - dB)**. |
| **FCT-04** | **Carnet d'Entretien Prédictif** | Module de suivi de l'usure des consommables (plaquettes, disques, fluides) indexé sur le nombre de tours de piste validés par l'utilisateur. |

### 2.2. Moteur de Recherche et Réservation

| ID | Fonctionnalité | Description |
| :--- | :--- | :--- |
| **FCT-05** | **Filtrage Auto-Adaptatif (Bruit)** | Fonctionnalité centrale : exclusion automatique des circuits dont la limite sonore est inférieure aux émissions du véhicule actif sélectionné dans le Garage Virtuel. |
| **FCT-06** | **Filtres Multicritères** | Filtrage par rayon kilométrique (géolocalisation), dates, et disponibilité des places en fonction du groupe de niveau du pilote (Débutant, Intermédiaire, Confirmé). |
| **FCT-07** | **Fiches Circuits Détaillées** | Affichage des données techniques de l'infrastructure : tracé, longueur, type de dégagements (asphalte/graviers), et commodités (bornes électriques, compresseurs, station SP98). |
| **FCT-08** | **Passerelle de Réservation** | Redirection traçable vers la plateforme de billetterie du club ou de l'organisateur de l'événement. |

### 2.3. Télémétrie et Statistiques (Palmarès)

| ID | Fonctionnalité | Description |
| :--- | :--- | :--- |
| **FCT-09** | **Historique Pilote (Best Laps)** | Tableau de bord personnel agrégeant les meilleurs chronos par circuit. Ces données sont rattachées au profil du pilote, indépendamment du véhicule prêté ou possédé. |
| **FCT-10** | **CV Mécanique du Véhicule** | Agrégation du kilométrage total sur piste et du nombre de tours effectués par une machine spécifique (historique valorisable pour la revente). |

---

## 3. Cas d'Usage Type (Workflow Utilisateur)

**Exemple de parcours d'un utilisateur "Pilote Moto" :**

1. **Onboarding & Qualification :** L'utilisateur crée son compte, renseigne son numéro de licence FFM en cours de validité et ajoute sa *Yamaha R1* dans son Garage Virtuel (en précisant une émission sonore de 102 dB et une monte en pneus slicks).
2. **Recherche Intelligente :** Il effectue une recherche de roulage à moins de 300 km. Le moteur de recherche écarte de lui-même les circuits restrictifs (ex: Laquais, Bresse) au profit de tracés permissifs. Les tarifs affichés sont calculés net (sans supplément RC Piste).
3. **Conversion :** L'utilisateur sélectionne une date au Pôle Mécanique d'Alès et est redirigé vers l'organisateur pour la transaction.
4. **Acquisition de Données (Post-Événement) :** L'utilisateur valide sa participation dans l'application, saisit son volume de roulage (60 tours) et son meilleur chrono (1'18"200).
5. **Mise à jour du Système :** Le tableau de bord met à jour son record personnel, incrémente le CV mécanique de la Yamaha R1, et déclenche une alerte concernant l'usure estimée de ses plaquettes de frein (franchissement du seuil des 80%).

---

## 4. Architecture et Contraintes Techniques

Pour assurer un traitement en temps réel des données géographiques, administratives et sonores, l'infrastructure repose sur une stack technologique moderne et évolutive.

| Composant | Technologie | Rôle et Justification technique |
| :--- | :--- | :--- |
| **Base de Données** | **PostgreSQL + PostGIS** | Gestion relationnelle stricte (séparation Pilotes/Véhicules/Événements). L'extension PostGIS permet l'exécution de requêtes spatiales complexes (calcul de rayons kilométriques autour du domicile). |
| **Serveur d'API (Backend)** | **Python / FastAPI** | Architecture asynchrone garantissant des temps de réponse ultra-rapides (<200ms) pour les requêtes croisées complexes (localisation + décibels + licences). |
| **Collecte de Données** | **Scrapers Python** | Exécution de tâches planifiées (CRON) automatisant l'extraction des calendriers depuis les sites web des organisateurs, garantissant une base de données à jour sans intervention manuelle. |
| **Interface (Frontend)** | **React (TypeScript)** | Gestion dynamique de l'état (State). Le changement de véhicule dans le garage met à jour instantanément les résultats du calendrier de réservation. |
| **Cartographie & Dataviz** | **MapLibre GL JS / Recharts** | Rendu vectoriel fluide des cartes d'infrastructures et génération de graphiques analytiques (courbes de progression des chronos, jauges d'usure). |
| **Infrastructure** | **Docker** | Conteneurisation globale (micro-services) pour sécuriser le déploiement en production, faciliter la scalabilité et préparer l'intégration de la V2. |

---

## 5. Livrables Attendus

Pour acter la validation et la réception de la version 1.0 du projet, le prestataire / l'équipe technique devra fournir les éléments suivants :

*   **Dépôts de Code (Repositories) :** Accès aux environnements Git documentés pour l'ensemble des briques logicielles (Frontend, Backend, Scrapers).
*   **Base de Données Opérationnelle :** Déploiement du schéma PostgreSQL/PostGIS avec les scripts SQL de création des tables relationnelles et des index géospatiaux.
*   **Moteurs d'Automatisation :** Scripts de scraping fonctionnels et configurés sur le serveur pour une exécution nocturne automatique.
*   **Environnement de Déploiement :** Un ensemble de fichiers de configuration (ex: `docker-compose.yml`) permettant de provisionner l'application complète en une commande.
*   **Documentation Complète :** 
    *   Un manuel technique (`README.md` détaillé, gestion des variables d'environnement, clés d'API).
    *   La documentation autogénérée de l'API REST (via Swagger/OpenAPI intégrée à FastAPI).

---

## 6. Évolutions Envisageables (Roadmap V2 — Module "Route")

Afin de ne pas retarder la mise sur le marché (Time-To-Market) du module Trackdays, les fonctionnalités destinées à la pratique sur route ouverte sont planifiées pour la V2 :

*   **Heatmap de Sinuosité :** Algorithmique PostGIS exploitant les données OpenStreetMap (OSM) pour colorer le réseau routier selon la densité des virages.
*   **Viabilité en Temps Réel :** Interfaçage avec les API institutionnelles (Bison Futé, Conseils Départementaux) pour l'état d'ouverture des cols de montagne.
*   **Crowdsourcing & Alertes :** Système communautaire de signalement de dangers temporaires (gravillons, chaussée dégradée).
*   **Filtres de Gabarit Routier :** Prise en compte de la largeur des routes et du pourcentage de pente pour la préservation mécanique des véhicules anciens ou de prestige.
*   **Export Télématique :** Génération de fichiers d'itinéraires standardisés (GPX/KML) pour intégration directe dans les GPS spécialisés (Garmin, TomTom) ou les systèmes d'infodivertissement (CarPlay, Android Auto).