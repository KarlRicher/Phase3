"""Jeu Quoridor

Ce programme permet de jouer au jeu Quoridor.
Il supporte les modes manuel, automatique et graphique.
"""
import sys # Ajout pour sys.exit
from api import créer_une_partie, récupérer_une_partie # Gardé pour référence future
# Correction de l'import de Quoridor et ajout de QuoridorX
from quoridor import Quoridor, interpréter_la_ligne_de_commande
from quoridor_error import QuoridorError
from quoridorx import QuoridorX # Ajout de l'import pour le mode graphique

# Mettre ici votre IDUL comme clé et votre Jeton comme secret.
# JETONS = {
#     "karic49": "f526631a-587c-4170-a0a1-2e658361e7e0",
# } # Commenté pour l'instant, pas utilisé sans serveur

if __name__ == "__main__":
    # 1. Interpréter les arguments de ligne de commande
    args = interpréter_la_ligne_de_commande()

    # 2. Définir les joueurs
    # Note: Pour l'instant, le deuxième joueur est toujours "automate"
    # En mode serveur, ce serait le nom renvoyé par l'API
    joueur_principal = args.idul
    adversaire = "automate"
    joueurs = [
        {"nom": joueur_principal, "murs": 10, "position": [5, 1]},
        {"nom": adversaire, "murs": 10, "position": [5, 9]}
    ]
    murs = {"horizontaux": [], "verticaux": []}

    # 3. Instancier la bonne classe de jeu
    if args.graphique:
        partie = QuoridorX(joueurs, murs)
    else:
        partie = Quoridor(joueurs, murs)

    # 4. Boucle principale du jeu
    tour_joueur_principal = True # Le joueur principal (IDUL) commence
    gagnant = False

    while not gagnant:
        # Afficher l'état du jeu
        if args.graphique:
            partie.afficher() # Mise à jour de l'affichage graphique
        else:
            print(partie) # Affichage ASCII

        # Déterminer le joueur courant
        joueur_courant = joueur_principal if tour_joueur_principal else adversaire

        print(f"\nTour {partie.tour} - C'est au tour de: {joueur_courant}")

        try:
            type_coup = None
            position = None

            # 5. Obtenir le coup
            if joueur_courant == joueur_principal:
                # Tour du joueur principal (IDUL)
                if args.automatique:
                    print("Mode automatique activé pour vous...")
                    type_coup, position = partie.jouer_un_coup(joueur_principal)
                    print(f"Coup choisi par l'IA ({joueur_principal}): {type_coup} {position}")
                else:
                    # Mode manuel
                    type_coup, position = partie.sélectionner_un_coup(joueur_principal)
            else:
                # Tour de l'adversaire ("automate")
                # Pour l'instant, on le fait jouer automatiquement avec la même IA
                # (En mode serveur, ce serait différent)
                print(f"L'adversaire ({adversaire}) réfléchit...")
                type_coup, position = partie.jouer_un_coup(adversaire)
                print(f"Coup choisi par l'IA ({adversaire}): {type_coup} {position}")

            # 6. Appliquer le coup choisi
            partie.appliquer_un_coup(joueur_courant, position, type_coup)

            # 7. Vérifier si la partie est terminée
            gagnant = partie.partie_terminée()

            # 8. Passer au joueur suivant
            tour_joueur_principal = not tour_joueur_principal

        except QuoridorError as e:
            print(f"\nERREUR : {e}\n")
            # En cas d'erreur, on pourrait arrêter ou laisser réessayer
            # Pour l'instant, on arrête.
            sys.exit(1)
        except Exception as e_gen:
            # Attraper d'autres erreurs potentielles
            print(f"\nERREUR INATTENDUE : {e_gen}\n")
            sys.exit(1)

    # Fin de la partie
    print("\nPartie terminée !")
    if args.graphique:
        partie.afficher() # Afficher l'état final
        print(f"Le gagnant est {gagnant} !")
        print("Cliquez sur la fenêtre graphique pour quitter.")
        partie.screen.exitonclick() # Garde la fenêtre ouverte jusqu'au clic
    else:
        print(partie) # Afficher l'état final
        print(f"Le gagnant est {gagnant} !")