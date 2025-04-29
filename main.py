"""
Client principal pour le jeu Quoridor interactif ou automatique,
avec support pour l'affichage texte ou graphique (Turtle).

Interagit avec une API externe pour gérer l'état de la partie
et appliquer les coups des joueurs. Supporte le mode manuel
et un mode "automatique" (nécessite l'implémentation de la
logique de jeu automatique dans la classe Quoridor ou QuoridorX).
"""

import sys
import argparse
import time
import turtle
from copy import deepcopy
from api import créer_une_partie, récupérer_une_partie, appliquer_un_coup
from quoridor import Quoridor
from quoridor_error import QuoridorError
from quoridorx import QuoridorX

# Mettre ici votre IDUL comme clé et votre Jeton comme secret.
JETONS = {
    "karic49": "f526631a-587c-4170-a0a1-2e658361e7e0",
    # Ajoutez d'autres IDULs et jetons si nécessaire
}

# --- Méthode utilitaire pour mettre à jour l'état local ---
# (Alternative: ajouter cette logique à Quoridor/__init__ ou une méthode dédiée)
def créer_ou_mettre_à_jour_partie(classe_jeu, état_serveur, partie_existante=None):
    """Crée ou met à jour une instance de jeu Quoridor/QuoridorX."""
    joueurs = état_serveur['joueurs']
    murs = état_serveur['murs']
    tour = état_serveur.get('tour', 1) # Récupère le tour si présent, sinon 1

    if isinstance(partie_existante, classe_jeu):
        # Mise à jour simple (si les objets sont conçus pour être mutables)
        partie_existante.joueurs = deepcopy(joueurs) # Utiliser deepcopy par sécurité
        partie_existante.murs = deepcopy(murs)
        partie_existante.tour = tour
        # Recalculer max_nom_len si nécessaire
        partie_existante.max_nom_len = max(len(j["nom"]) for j in partie_existante.joueurs)

        return partie_existante
        # Création d'une nouvelle instance
    return classe_jeu(joueurs, murs, tour)


if __name__ == "__main__":
    # === Analyse des arguments ===
    parser = argparse.ArgumentParser(prog="main.py", description="Quoridor")
    parser.add_argument("idul", help="IDUL du joueur")
    parser.add_argument("-a", "--automatique", action="store_true",
                         help="Activer le mode automatique.")
    parser.add_argument("-x", "--graphique", action="store_true", help="Activer le mode graphique.")
    args = parser.parse_args()

    # === Récupération du secret ===
    idul_joueur = args.idul
    if idul_joueur not in JETONS:
        print(f"ERREUR: IDUL '{idul_joueur}' non trouvé dans les jetons définis.")
        sys.exit(1)
    secret_joueur = JETONS[idul_joueur]

    # === Création de la partie via API ===
    id_partie = None
    état_partie_actuel = None
    try:
        print(f"Création de la partie pour {idul_joueur}...")
        id_partie, état_partie_actuel = créer_une_partie(idul_joueur, secret_joueur)
        print(f"Partie créée avec ID: {id_partie}")

    except (PermissionError, RuntimeError, ConnectionError) as e:
        print(f"ERREUR API : {e}")
        sys.exit(1)
    except Exception as e_gen:
        print(f"ERREUR Inattendue lors de la création de partie : {e_gen}")
        sys.exit(1)

    # === Initialisation de l'instance de jeu (sera créée/MAJ dans la boucle) ===
    partie = None
    gagnant = None
    classe_jeu = QuoridorX if args.graphique else Quoridor

    # === Boucle principale du jeu ===
    while gagnant is None:
        try:
            # 1. Mettre à jour/Créer l'instance locale et afficher
            partie = créer_ou_mettre_à_jour_partie(classe_jeu, état_partie_actuel, partie)

            if args.graphique:
                partie.afficher()
            else:
                print(partie)

            # 2. Déterminer qui doit jouer selon l'état du serveur
            joueur_actif = état_partie_actuel['joueurs'][0]['nom']
            print(f"\nTour {partie.tour} - C'est au tour de: {joueur_actif}")

            # 3. Si c'est notre tour, jouer
            if joueur_actif == idul_joueur:
                type_coup = None
                position = None

                # Obtenir le coup (manuel ou auto)
                try:
                    if args.automatique:
                        print("Mode automatique activé pour vous...")
                        type_coup, position = partie.jouer_un_coup(idul_joueur)
                        print(f"Coup choisi par l'IA ({idul_joueur}): {type_coup} {position}")
                    else:
                        print("Mode manuel activé.")
                        type_coup, position = partie.sélectionner_un_coup(idul_joueur)

                except QuoridorError as e_local:
                    # Erreur dans la logique locale (sélection/décision)
                    print(f"\nERREUR de jeu local : {e_local}")
                    print("Arrêt de la partie.")
                    sys.exit(1)


                # Appliquer le coup via l'API
                print(f"Envoi du coup {type_coup} {position} au serveur...")
                appliquer_un_coup(id_partie, type_coup, position, idul_joueur, secret_joueur)

                # Si on arrive ici, le coup a été accepté et la partie n'est pas finie par ce coup
                print("Coup accepté par le serveur. Récupération de l'état...")
                try:
                    _, état_partie_actuel = récupérer_une_partie(id_partie, idul_joueur,
                                                                 secret_joueur)
                except (PermissionError, RuntimeError, ConnectionError,
                         ReferenceError) as e_recup:
                    print(f"\nERREUR API lors de la récupération après coup : {e_recup}")
                    print("Arrêt de la partie.")
                    sys.exit(1)


            else:
                # Ce n'est pas notre tour, attendre/récupérer l'état
                print("En attente du coup de l'adversaire...")
                # Pause optionnelle pour ne pas surcharger le serveur avec des GETs
                time.sleep(0.5)
                try:
                    _, état_partie_actuel = récupérer_une_partie(id_partie, idul_joueur,
                                                              secret_joueur)
                except (PermissionError, RuntimeError, ConnectionError,
                         ReferenceError) as e_recup_attente:
                    print(f"\nERREUR API lors de la récupération en attente : {e_recup_attente}")
                    print("Arrêt de la partie.")
                    sys.exit(1)


        except StopIteration as e:
            gagnant = e.value # L'API renvoie le nom du gagnant via StopIteration
            print("\nPartie terminée ! (Signalée par l'API)")
        except (PermissionError, RuntimeError, ConnectionError, ReferenceError) as e:
            # Erreur API lors de l'application du coup
            print(f"\nERREUR API lors de l'application du coup : {e}")
            print("Arrêt de la partie.")
            sys.exit(1)
        except Exception as e_gen:
            # Toute autre erreur imprévue
            print(f"\nERREUR INATTENDUE : {e_gen}")
            import traceback
            traceback.print_exc()
            print("Arrêt de la partie.")
            sys.exit(1)


    # --- Fin de Partie ---
    print("\n===== PARTIE TERMINÉE =====")
    # Essayer de récupérer un dernier état pour affichage final
    try:
        _, état_final = récupérer_une_partie(id_partie, idul_joueur, secret_joueur)
        partie = créer_ou_mettre_à_jour_partie(classe_jeu, état_final, partie)
        if args.graphique and partie:
            partie.afficher()
        elif partie:
            print(partie)
    except Exception as e_final:
        print(f"Impossible de récupérer l'état final : {e_final}")
        # Afficher le dernier état connu si disponible
        if args.graphique and partie:
            partie.afficher()
        elif partie:
            print(partie)


    print(f"Le gagnant est : {gagnant}")

    if args.graphique and partie:
        print("Cliquez sur la fenêtre graphique pour quitter.")
        # Garder la fenêtre ouverte jusqu'au clic
        try:
            partie.screen.exitonclick()
        except turtle.Terminator:
            print("Fenêtre Turtle fermée.") # Gérer l'erreur si la fenêtre est fermée autrement
