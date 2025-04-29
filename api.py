"""Module d'API du jeu Quoridor"""

import requests

URL = "https://pax.ulaval.ca/quoridor/api/h25"


def créer_une_partie(idul, secret):
    """Créer une nouvelle partie"""
    print("DEBUG:", idul, secret)  # ← ici, pour voir exactement ce que tu envoies

    rep = requests.post(f"{URL}/parties", auth=(idul, secret))

    if rep.status_code == 200:
        data = rep.json()
        return data["id"], data["état"]

    elif rep.status_code == 401:
        raise PermissionError(rep.json()["message"])

    elif rep.status_code == 406:
        raise RuntimeError(rep.json()["message"])

    else:
        raise ConnectionError(f"Erreur inattendue ({rep.status_code})")

def récupérer_une_partie(id_partie, idul, secret):
    """Récupérer l'état d'une partie existante"""
    rep = requests.get(f"{URL}/parties/{id_partie}", auth=(idul, secret))

    if rep.status_code == 200:
        data = rep.json()
        return data["id"], data["état"]

    elif rep.status_code == 401:
        raise PermissionError(rep.json()["message"])

    elif rep.status_code == 404:
        raise ReferenceError(rep.json()["message"])

    elif rep.status_code == 406:
        raise RuntimeError(rep.json()["message"])

    else:
        raise ConnectionError(f"Erreur inattendue ({rep.status_code})")


def appliquer_un_coup(id_partie, coup, position, idul, secret):
    """Appliquer un coup à une partie"""
    rep = requests.put(
        f"{URL}/parties/{id_partie}",
        auth=(idul, secret),
        json={"coup": coup, "position": position},
    )

    if rep.status_code == 200:
        data = rep.json()

        if data["partie"] == "terminée":
            raise StopIteration(data["gagnant"])
        
        return data["coup"], data ["position"]
    
    elif rep.status_code == 401:
        raise PermissionError(rep.json()["message"])
    
    elif rep.status_code == 404:
        raise ReferenceError(rep.json()["message"])
    
    elif rep.status_code == 406:
        raise RuntimeError(rep.json()["message"])
    
    else:
        raise ConnectionError(f"Erreur inattendue ({rep.status_code})")
