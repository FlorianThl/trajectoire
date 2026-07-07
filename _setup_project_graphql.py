#!/usr/bin/env python3
"""Gestion de projet via GitHub GraphQL (Projects v2)."""

import json
import os
import urllib.request
import urllib.error

USER = "FlorianThl"
REPO = "FlorianThl/trajectoire"
TOKEN = os.environ["GITHUB_TOKEN"]
USER_NODE_ID = "U_kgDOBw-Ghg"

HEADERS = {
    "Authorization": f"token {TOKEN}",
    "Content-Type": "application/json",
}

def graphql(query, variables=None):
    url = "https://api.github.com/graphql"
    data = {"query": query}
    if variables:
        data["variables"] = variables
    body = json.dumps(data).encode()
    req = urllib.request.Request(url, data=body, headers=HEADERS, method="POST")
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        err = e.read().decode()
        print(f"  ⚠ HTTPError {e.code}: {err[:500]}")
        return None

def rest(method, path, data=None):
    url = f"https://api.github.com/repos/{REPO}/{path}"
    body = json.dumps(data).encode() if data else None
    req = urllib.request.Request(url, data=body, headers={
        "Authorization": f"token {TOKEN}",
        "Accept": "application/vnd.github.v3+json",
        "Content-Type": "application/json",
    }, method=method)
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        err = e.read().decode()
        print(f"  ⚠ HTTPError {e.code}: {err[:300]}")
        return None

print("=" * 60)
print("1. Création du ProjectV2 (GitHub Projects)")
print("=" * 60)

# Créer le projet via GraphQL
create_project_query = """
mutation($ownerId: ID!, $title: String!) {
  createProjectV2(input: {
    ownerId: $ownerId,
    title: $title
  }) {
    projectV2 {
      id
      number
      title
      url
    }
  }
}
"""

result = graphql(create_project_query, {
    "ownerId": USER_NODE_ID,
    "title": "Trajectoire V1",
})

if result and result.get("data", {}).get("createProjectV2"):
    project = result["data"]["createProjectV2"]["projectV2"]
    project_id = project["id"]
    project_url = project["url"]
    print(f"  ✅ Project créé: {project_url}")
    print(f"  ID: {project_id}")
else:
    errs = result.get("errors", [{}]) if result else []
    print(f"  ⚠ Erreur: {errs}")
    print("  → Le projet existe peut-être déjà. Récupération...")
    # Chercher le projet existant
    search_query = """
    query($login: String!) {
      user(login: $login) {
        projectsV2(first: 20) {
          nodes {
            id
            number
            title
            url
          }
        }
      }
    }
    """
    result = graphql(search_query, {"login": USER})
    if result:
        projects = result.get("data", {}).get("user", {}).get("projectsV2", {}).get("nodes", [])
        for p in projects:
            if "Trajectoire" in p["title"]:
                project_id = p["id"]
                project_url = p["url"]
                print(f"  ✅ Projet existant trouvé: {project_url}")
                break
        else:
            print("  ⚠ Aucun projet trouvé")
            exit(1)

# ====================================================================
# 2. Configurer les champs du projet (Status)
# ====================================================================
print("\n" + "=" * 60)
print("2. Configuration du champ Status")
print("=" * 60)

# Récupérer les métadonnées du projet pour trouver le champ Status
meta_query = """
query($projectId: ID!) {
  node(id: $projectId) {
    ... on ProjectV2 {
      fields(first: 20) {
        nodes {
          ... on ProjectV2Field {
            id
            name
            dataType
          }
          ... on ProjectV2SingleSelectField {
            id
            name
            dataType
            options {
              id
              name
            }
          }
        }
      }
    }
  }
}
"""

result = graphql(meta_query, {"projectId": project_id})
if result:
    fields = result.get("data", {}).get("node", {}).get("fields", {}).get("nodes", [])
    print(f"  {len(fields)} champ(s) trouvé(s)")
    status_field = None
    for f in fields:
        print(f"  - {f.get('name')} ({f.get('dataType')})")
        if f.get("name") == "Status":
            status_field = f
    if status_field:
        print(f"  ✅ Champ Status existant: {status_field['id']}")
        status_field_id = status_field["id"]
        existing_options = {o["name"]: o["id"] for o in status_field["options"]}
        print(f"  Options: {list(existing_options.keys())}")
    else:
        print("  ⚠ Création du champ Status...")
        # Créer le champ Status (SingleSelect)
        add_field_query = """
        mutation($projectId: ID!, $fieldName: String!, $options: [String!]!) {
          createProjectV2Field(input: {
            projectId: $projectId,
            name: $fieldName,
            dataType: SINGLE_SELECT
            singleSelectOptions: $options
          }) {
            projectV2Field {
              ... on ProjectV2SingleSelectField {
                id
                name
                options { id name }
              }
            }
          }
        }
        """
        result = graphql(add_field_query, {
            "projectId": project_id,
            "fieldName": "Status",
            "options": ["Backlog", "To Do", "In Progress", "Review", "Done"],
        })
        if result and result.get("data", {}).get("createProjectV2Field"):
            status_field = result["data"]["createProjectV2Field"]["projectV2Field"]
            status_field_id = status_field["id"]
            existing_options = {o["name"]: o["id"] for o in status_field["options"]}
            print(f"  ✅ Champ Status créé: {status_field_id}")
            print(f"  Options: {list(existing_options.keys())}")
        else:
            errs = result.get("errors", [{}]) if result else []
            print(f"  ⚠ Erreur création Status: {errs}")
            # Maybe it already exists, let me try to get it differently
            status_field_id = None
            existing_options = {}
else:
    status_field_id = None
    existing_options = {}

# ====================================================================
# 3. Créer les Milestones (sprints)
# ====================================================================
print("\n" + "=" * 60)
print("3. Création des Milestones")
print("=" * 60)

milestones_data = [
    {"title": "Sprint 1", "description": "Fondations & Infrastructure", "state": "closed"},
    {"title": "Sprint 2", "description": "Gestion des Utilisateurs & Garage Virtuel", "state": "open"},
    {"title": "Sprint 3", "description": "Moteur de Recherche & Circuits", "state": "open"},
    {"title": "Sprint 4", "description": "Réservation & Automatisation", "state": "open"},
    {"title": "Sprint 5", "description": "Télémétrie & Statistiques", "state": "open"},
    {"title": "Sprint 6", "description": "Carnet d'Entretien & Finalisation V1", "state": "open"},
]

milestone_map = {}
for ms in milestones_data:
    existing = rest("GET", f"milestones?state=all")
    if existing:
        for m in existing:
            if m["title"] == ms["title"]:
                milestone_map[ms["title"]] = m
                print(f"  ~ Milestone '{ms['title']}' existe déjà (id={m['number']})")
                break
        else:
            result = rest("POST", "milestones", ms)
            if result:
                milestone_map[ms["title"]] = result
                print(f"  ✅ Milestone '{ms['title']}' créé (id={result['number']})")
            else:
                print(f"  ⚠ Échec création milestone '{ms['title']}'")
    else:
        print(f"  ⚠ Impossible de vérifier les milestones")

# ====================================================================
# 4. Créer les Issues pour chaque sprint
# ====================================================================
print("\n" + "=" * 60)
print("4. Création des Issues (tâches des sprints)")
print("=" * 60)

issues_data = [
    {
        "title": "Sprint 1 — Fondations & Infrastructure",
        "labels": ["sprint-1", "devops"],
        "milestone": "Sprint 1",
        "body": "### Ce qui a été livré\n\n- [x] Repository GitHub créé\n- [x] Docker Compose + Dockerfiles\n- [x] Schéma BDD PostgreSQL/PostGIS\n- [x] Backend FastAPI squelette\n- [x] Frontend React/TypeScript\n- [x] CI/CD GitHub Actions\n- [x] Documentation de base",
        "status": "Done",
    },
    {
        "title": "Sprint 2 — Utilisateurs & Garage Virtuel",
        "labels": ["sprint-2", "backend", "frontend"],
        "milestone": "Sprint 2",
        "body": "Voir le cahier des charges FCT-01, FCT-02, FCT-03.\n\n### Tâches\n- [ ] Inscription / Connexion JWT\n- [ ] CRUD Profil Pilote avec licence\n- [ ] CRUD Garage Virtuel (Auto/Moto)\n- [ ] Configuration Setup Piste (dB, pneus, freins)\n- [ ] Tests unitaires et intégration\n- [ ] Pages frontend (profil + garage)",
        "status": "To Do",
    },
    {
        "title": "Sprint 3 — Recherche & Circuits",
        "labels": ["sprint-3", "backend", "frontend"],
        "milestone": "Sprint 3",
        "body": "Voir le cahier des charges FCT-05, FCT-06, FCT-07.\n\n### Tâches\n- [ ] Filtrage Auto-Adaptatif (bruit)\n- [ ] Filtres multicritères (rayon, dates, niveau)\n- [ ] Fiches circuits détaillées avec carte\n- [ ] Requêtes PostGIS\n- [ ] Interface frontend (recherche + résultats)",
        "status": "Backlog",
    },
    {
        "title": "Sprint 4 — Réservation & Scrapers",
        "labels": ["sprint-4", "backend", "devops"],
        "milestone": "Sprint 4",
        "body": "Voir le cahier des charges FCT-08 + Scrapers.\n\n### Tâches\n- [ ] Passerelle de réservation (redirection traçable)\n- [ ] Architecture scraper modulaire\n- [ ] Parsing calendriers organisateurs\n- [ ] Tâche CRON scraping\n- [ ] Circuit initial seeding",
        "status": "Backlog",
    },
    {
        "title": "Sprint 5 — Télémétrie & Statistiques",
        "labels": ["sprint-5", "backend", "frontend"],
        "milestone": "Sprint 5",
        "body": "Voir le cahier des charges FCT-09, FCT-10.\n\n### Tâches\n- [ ] Saisie chronos post-événement\n- [ ] Tableau de bord Best Laps\n- [ ] Courbes de progression (Recharts)\n- [ ] CV Mécanique du véhicule\n- [ ] Export PDF",
        "status": "Backlog",
    },
    {
        "title": "Sprint 6 — Entretien & Finalisation V1",
        "labels": ["sprint-6", "backend", "frontend", "devops"],
        "milestone": "Sprint 6",
        "body": "Voir le cahier des charges FCT-04 + finalisation.\n\n### Tâches\n- [ ] Carnet d'entretien prédictif (alertes 80%)\n- [ ] Jaunes d'usure interface\n- [ ] Documentation complète\n- [ ] Tests d'intégration\n- [ ] Déploiement final",
        "status": "Backlog",
    },
]

issue_map = {}

for issue_data in issues_data:
    status = issue_data.pop("status", "Backlog")

    # Créer l'issue
    issue = rest("POST", "issues", {
        "title": issue_data["title"],
        "body": issue_data["body"],
        "labels": issue_data["labels"],
        "milestone": milestone_map.get(issue_data["milestone"], {}).get("number"),
    })

    if issue:
        issue_map[issue_data["title"]] = issue
        print(f"  ✅ {issue_data['title'][:55]:55s} → Issue #{issue['number']}")

        # Ajouter l'issue au projet (ProjectV2)
        if project_id:
            add_item_query = """
            mutation($projectId: ID!, $contentId: ID!) {
              addProjectV2ItemById(input: {
                projectId: $projectId,
                contentId: $contentId
              }) {
                item {
                  id
                }
              }
            }
            """
            item_result = graphql(add_item_query, {
                "projectId": project_id,
                "contentId": issue["node_id"],
            })
            if item_result and item_result.get("data", {}).get("addProjectV2ItemById"):
                item_id = item_result["data"]["addProjectV2ItemById"]["item"]["id"]
                print(f"    → Ajouté au projet (item_id={item_id[:15]}...)")

                # Mettre à jour le champ Status
                if status_field_id and status in existing_options:
                    update_query = """
                    mutation($projectId: ID!, $itemId: ID!, $fieldId: ID!, $optionId: String!) {
                      updateProjectV2ItemFieldValue(input: {
                        projectId: $projectId,
                        itemId: $itemId,
                        fieldId: $fieldId,
                        value: { singleSelectOptionId: $optionId }
                      }) {
                        projectV2Item {
                          id
                        }
                      }
                    }
                    """
                    update_result = graphql(update_query, {
                        "projectId": project_id,
                        "itemId": item_id,
                        "fieldId": status_field_id,
                        "optionId": existing_options[status],
                    })
                    if update_result and update_result.get("data", {}).get("updateProjectV2ItemFieldValue"):
                        print(f"    → Statut: {status}")
                    else:
                        print(f"    ⚠ Échec mise à jour statut: {update_result.get('errors', 'unknown')}")
            else:
                print(f"    ⚠ Échec ajout au projet")
    else:
        print(f"  ⚠ Échec: {issue_data['title']}")

# ====================================================================
# Résumé
# ====================================================================
print("\n" + "=" * 60)
print("RÉSUMÉ — Gestion de projet")
print("=" * 60)
print(f"""
✅ Projet GitHub:      {project_url}
📌 Issues:            https://github.com/{REPO}/issues
🏷️  Labels:            11 labels créés
📅 Milestones:        6 sprints

📊 Board virtuel:
   Backlog     │ Sprint 3, 4, 5, 6
   To Do       │ Sprint 2
   In Progress │ (rien)
   Review      │ (rien)
   Done        │ Sprint 1
""")

# Nettoyage
os.remove(os.path.join(os.path.dirname(os.path.abspath(__file__)), "_setup_project_mgmt.py"))
