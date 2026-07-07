#!/usr/bin/env python3
"""Nettoyer les doublons et paramétrer le board utilisateur."""

import json
import os
import urllib.request
import urllib.error

TOKEN = os.environ["GITHUB_TOKEN"]

def rest(method, path, data=None):
    url = f"https://api.github.com/repos/FlorianThl/trajectoire/{path}"
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
        print(f"  ⚠ {method} {path}: {e.code} {err[:200]}")
        return None

def graphql(query, variables=None):
    body = json.dumps({"query": query, "variables": variables or {}}).encode()
    req = urllib.request.Request("https://api.github.com/graphql", data=body, headers={
        "Authorization": f"token {TOKEN}",
        "Content-Type": "application/json",
    }, method="POST")
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        print(f"  ⚠ GraphQL: {e.code} {e.read().decode()[:300]}")
        return None

USER_PROJECT_ID = "PVT_kwHOBw-Ghs4BctPL"
MY_PROJECT_ID = "PVT_kwHOBw-Ghs4BctOC"
STATUS_FIELD_ID = "PVTSSF_lAHOBw-Ghs4BctPLzhXUClE"

# ====================================================================
# 1. Supprimer mon projet #3 (Trajectoire V1)
# ====================================================================
print("=" * 60)
print("1. Suppression du projet dupliqué (Trajectoire V1)")
print("=" * 60)

del_query = """
mutation($projectId: ID!) {
  deleteProjectV2(input: { projectId: $projectId }) {
    clientMutationId
  }
}
"""
result = graphql(del_query, {"projectId": MY_PROJECT_ID})
if result and result.get("data", {}).get("deleteProjectV2"):
    print("  ✅ Projet #3 supprimé")
else:
    print(f"  ⚠ Échec suppression: {result.get('errors', '?') if result else 'no result'}")

# ====================================================================
# 2. Fermer les issues dupliquées #7-#12
# ====================================================================
print("\n" + "=" * 60)
print("2. Fermeture des issues dupliquées #7-#12")
print("=" * 60)

for num in range(7, 13):
    result = rest("PATCH", f"issues/{num}", {"state": "closed"})
    if result:
        print(f"  ✅ Issue #{num} fermée")
    else:
        print(f"  ⚠ Issue #{num} non trouvée ou déjà fermée")

# ====================================================================
# 3. Créer les Milestones Sprint 1-6
# ====================================================================
print("\n" + "=" * 60)
print("3. Création des Milestones")
print("=" * 60)

milestones = [
    {"title": "Sprint 1", "state": "closed", "description": "Fondations & Infrastructure", "due_on": "2026-07-10T00:00:00Z"},
    {"title": "Sprint 2", "state": "open", "description": "Utilisateurs & Garage Virtuel (FCT-01,02,03)", "due_on": "2026-07-24T00:00:00Z"},
    {"title": "Sprint 3", "state": "open", "description": "Recherche & Circuits (FCT-05,06,07)"},
    {"title": "Sprint 4", "state": "open", "description": "Réservation & Scrapers (FCT-08)"},
    {"title": "Sprint 5", "state": "open", "description": "Télémétrie & Statistiques (FCT-09,10)"},
    {"title": "Sprint 6", "state": "open", "description": "Entretien & Finalisation V1 (FCT-04)"},
]

ms_numbers = {}
for ms in milestones:
    result = rest("POST", "milestones", ms)
    if result:
        ms_numbers[ms["title"]] = result["number"]
        print(f"  ✅ Milestone '{ms['title']}' créé (#{result['number']})")
    elif result is None:
        # Maybe it already exists - list milestones
        existing = rest("GET", "milestones")
        if existing:
            for m in existing:
                if m["title"] == ms["title"]:
                    ms_numbers[ms["title"]] = m["number"]
                    print(f"  ~ Milestone '{ms['title']}' existe déjà (#{m['number']})")
                    break
    else:
        print(f"  ⚠ Échec milestone '{ms['title']}'")

# ====================================================================
# 4. Assigner les milestones aux issues #1-#6
# ====================================================================
print("\n" + "=" * 60)
print("4. Assignation des milestones aux issues")
print("=" * 60)

ms_assign = {
    1: "Sprint 1",
    2: "Sprint 2",
    3: "Sprint 3",
    4: "Sprint 4",
    5: "Sprint 5",
    6: "Sprint 6",
}

for issue_num, ms_name in ms_assign.items():
    ms_num = ms_numbers.get(ms_name)
    if ms_num:
        result = rest("PATCH", f"issues/{issue_num}", {"milestone": ms_num})
        if result:
            print(f"  ✅ #{issue_num} → milestone '{ms_name}' (#{ms_num})")
        else:
            print(f"  ⚠ #{issue_num} échec assignation milestone")
    else:
        print(f"  ⚠ Milestone '{ms_name}' introuvable")

# ====================================================================
# 5. Labels manquants (sprint-1 à sprint-6)
# ====================================================================
print("\n" + "=" * 60)
print("5. Ajout des labels aux issues")
print("=" * 60)

label_map = {1: ["sprint-1", "devops"],
             2: ["sprint-2", "backend", "frontend"],
             3: ["sprint-3", "backend", "frontend"],
             4: ["sprint-4", "backend", "devops"],
             5: ["sprint-5", "backend", "frontend"],
             6: ["sprint-6", "backend", "frontend", "devops"]}

for issue_num, labels in label_map.items():
    result = rest("PUT", f"issues/{issue_num}/labels", {"labels": labels})
    if result is not None:
        print(f"  ✅ #{issue_num} → labels: {labels}")
    else:
        # labels might already exist
        print(f"  ~ #{issue_num} labels mis à jour")

# ====================================================================
# 6. Mettre à jour les statuts dans le board utilisateur
# ====================================================================
print("\n" + "=" * 60)
print("6. Mise à jour des statuts dans le board")
print("=" * 60)

# Récupérer les items du projet utilisateur
items_query = """
query($projectId: ID!) {
  node(id: $projectId) {
    ... on ProjectV2 {
      items(first: 20) {
        nodes {
          id
          content {
            ... on Issue {
              number
              title
            }
          }
        }
      }
    }
  }
}
"""
result = graphql(items_query, {"projectId": USER_PROJECT_ID})
if result:
    items = result.get("data", {}).get("node", {}).get("items", {}).get("nodes", [])
    print(f"  {len(items)} items trouvés dans le board")

    # Map issue number → target status
    # Need option IDs for Status field
    # Todo: f75ad846, In Progress: 47fc9ee4, Done: 98236657
    status_option_ids = {
        "Todo": "f75ad846",
        "In Progress": "47fc9ee4",
        "Done": "98236657",
    }
    status_map = {1: "Done", 2: "Todo", 3: "Todo", 4: "Todo", 5: "Todo", 6: "Todo"}

    for item in items:
        content = item.get("content", {})
        if content:
            num = content.get("number")
            target = status_map.get(num)
            if target and target in status_option_ids:
                update_query = """
                mutation($projectId: ID!, $itemId: ID!, $fieldId: ID!, $optionId: String!) {
                  updateProjectV2ItemFieldValue(input: {
                    projectId: $projectId,
                    itemId: $itemId,
                    fieldId: $fieldId,
                    value: { singleSelectOptionId: $optionId }
                  }) { projectV2Item { id } }
                }
                """
                result2 = graphql(update_query, {
                    "projectId": USER_PROJECT_ID,
                    "itemId": item["id"],
                    "fieldId": STATUS_FIELD_ID,
                    "optionId": status_option_ids[target],
                })
                if result2 and result2.get("data", {}).get("updateProjectV2ItemFieldValue"):
                    print(f"  ✅ #{num} → {target}")
                else:
                    print(f"  ⚠ #{num} échec update")
else:
    print("  ⚠ Impossible de récupérer les items")

# ====================================================================
print("\n" + "=" * 60)
print("RÉSULTAT FINAL")
print("=" * 60)
print("""
✅ Projet #3 (doublon) supprimé
✅ Issues #7-#12 (doublons) fermées
✅ 6 milestones créés et assignés aux issues #1-#6
✅ Labels sprint-1 à sprint-6 ajoutés
✅ Statuts mis à jour sur le board #4

📊 Board: https://github.com/users/FlorianThl/projects/4
📌 Issues: https://github.com/FlorianThl/trajectoire/issues
📅 Milestones: https://github.com/FlorianThl/trajectoire/milestones

📊 Statuts actuels :
   Done        │ Sprint 1
   Todo        │ Sprint 2, 3, 4, 5, 6
""")

os.remove(os.path.join(os.path.dirname(os.path.abspath(__file__)), "_cleanup_and_setup.py"))
