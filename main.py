"""Jeu Quoridor

Ce programme permet de jouer au jeu Quoridor.
"""

import argparse
from api import créer_une_partie, récupérer_une_partie
from quoridor import Quoridor, interpréter_la_ligne_de_commande
from quoridor_error import QuoridorError

JETONS = {
    "karic49": "f526631a-587c-4170-a0a1-2e658361e7e0",
}

if __name__ == "__main__":
    # === PARSEUR D'ARGUMENTS CONFORME À L'ÉNONCÉ ===
    parser = argparse.ArgumentParser(
        prog="main.py",
        description="Quoridor"
    )
    parser.add_argument(
        "idul",
        help="IDUL du joueur"
    )
    parser.add_argument(
        "-a", "--automatique",
        action="store_true",
        help="Activer le mode automatique."
    )
    parser.add_argument(
        "-x", "--graphique",
        action="store_true",
        help="Activer le mode graphique."
    )
    args = parser.parse_args()


    joueurs = [
        {"nom": args.idul, "murs": 10, "position": [5, 1]},
        {"nom": "automate", "murs": 10, "position": [5, 9]}
    ]
    murs = {"horizontaux": [], "verticaux": []}
    quoridor = Quoridor(joueurs, murs)

    # === BOUCLE PRINCIPALE DU JEU ===
    while not quoridor.partie_terminée():
        print(quoridor)

        try:
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

            quoridor.appliquer_un_coup(args.idul, position, type_coup)

        except QuoridorError as e:
            print(f"Erreur : {e}")
            break

