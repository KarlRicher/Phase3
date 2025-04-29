"""Jeu Quoridor

Ce programme permet de joueur au jeu Quoridor.
"""

from api import créer_une_partie, récupérer_une_partie
from quoridor import Quoridor, interpréter_la_ligne_de_commande
from quoridor_error import QuoridorError

# Mettre ici votre IDUL comme clé et votre Jeton comme secret.
JETONS = {
    "karic49": "f526631a-587c-4170-a0a1-2e658361e7e0",
}

AUTOMATIQUE = False

if __name__ == "__main__":
    # Initialisation du jeu
    args = interpréter_la_ligne_de_commande()
    joueurs = [
        {"nom": args.idul, "murs": 10, "position": [5, 1]},
        {"nom": "automate", "murs": 10, "position": [5, 9]}
    ]
    murs = {"horizontaux": [], "verticaux": []}
    quoridor = Quoridor(joueurs, murs)

    # Boucle principale du jeu
    while not quoridor.partie_terminée():
        print(quoridor)  # Affiche l'état actuel du jeu

        try:
            # Demander le type de coup et la position
            type_coup = input("Quel type de coup voulez-vous jouer? [D]éplacement ou [M]ur: ").strip().upper()
            if type_coup == "D":
                x = int(input("Entrez la position x de destination: "))
                y = int(input("Entrez la position y de destination: "))
                position = [x, y]
            elif type_coup == "M":
                x = int(input("Entrez la position x du mur: "))
                y = int(input("Entrez la position y du mur: "))
                orientation = input("Entrez l'orientation du mur [MH ou MV]: ").strip().upper()
                position = [x, y, orientation]
            else:
                raise QuoridorError("Type de coup invalide.")

            # Appliquer le coup
            quoridor.appliquer_un_coup(args.idul, position, type_coup)

        except QuoridorError as e:
            print(f"Erreur : {e}")
            break
