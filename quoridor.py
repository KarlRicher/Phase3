"""Module de la classe Quoridor

Classes:
    * Quoridor - Classe pour encapsuler le jeu Quoridor.
    * interpréter_la_ligne_de_commande - Génère un interpréteur de commande.
"""

import argparse
from copy import deepcopy
import networkx as nx
from quoridor_error import QuoridorError
from graphe import construire_graphe


class Quoridor:
    """Classe pour encapsuler le jeu Quoridor.

    Vous ne devez pas créer d'autre attributs pour votre classe.

    Attributes:
        joueurs (List): Un itérable de deux dictionnaires joueurs
            dont le premier est toujours celui qui débute la partie.
        murs (Dict): Un dictionnaire contenant une clé 'horizontaux' associée à
            la liste des positions [x, y] des murs horizontaux, et une clé 'verticaux'
            associée à la liste des positions [x, y] des murs verticaux.
        tour (int): Un entier positif représentant le tour du jeu (1 pour le premier tour).
    """

    # Define a constant for the empty board
    EMPTY_DAMIER = [['.' for _ in range(9)] for _ in range(9)]

    def __init__(self, joueurs, murs=None, tour=1):
        """Constructeur de la classe Quoridor.

        Initialise une partie de Quoridor avec les joueurs, les murs et le tour spécifiés,
        en s'assurant de faire une copie profonde de tout ce qui a besoin d'être copié.

        Cette méthode ne devrait pas être modifiée.

        Args:
            joueurs (List): un itérable de deux dictionnaires joueurs
                dont le premier est toujours celui qui débute la partie.
            murs (Dict, optionnel): Un dictionnaire contenant une clé 'horizontaux' associée à
                la liste des positions [x, y] des murs horizontaux, et une clé 'verticaux'
                associée à la liste des positions [x, y] des murs verticaux.
            tour (int, optionnel): Un entier positif représentant le tour du jeu.
        """
        self.tour = tour
        self.joueurs = deepcopy(joueurs)
        self.murs = deepcopy(murs or {"horizontaux": [], "verticaux": []})
        self.max_nom_len = max(len(j["nom"]) for j in self.joueurs)

    def état_partie(self):
        """Produire l'état actuel du jeu.

        Cette méthode ne doit pas être modifiée.

        Returns:
            Dict: Une copie de l'état actuel du jeu sous la forme d'un dictionnaire.
                  Notez que les positions doivent être sous forme de liste [x, y] uniquement.
        """
        return deepcopy(
            {
                "tour": self.tour,
                "joueurs": self.joueurs,
                "murs": self.murs,
            }
        )

    def formater_entête(self) -> str:
        """Formater l'entête avec noms alignés et un seul espace après la virgule."""
        j1 = self.joueurs[0]
        j2 = self.joueurs[1]

        # Trouver la longueur maximale des noms
        max_nom_len = max(len(j1['nom']), len(j2['nom']))

        # Formater chaque ligne avec un seul espace après la virgule
        ligne1 = (
            f"   1={j1['nom']},{' ' * (max_nom_len - len(j1['nom']) + 1)}murs="
            + "|" * j1["murs"]
        )
        ligne2 = (
            f"   2={j2['nom']},{' ' * (max_nom_len - len(j2['nom']) + 1)}murs="
            + "|" * j2["murs"]
        )

        return "Légende:\n" + ligne1 + "\n" + ligne2 + "\n"

    def formater_le_damier(self):
        """Formater la représentation graphique du damier.

        Returns:
            str: Chaîne de caractères représentant le damier.
        """
        damier = [row[:] for row in self.EMPTY_DAMIER]

        # Placement des joueurs
        p1 = self.joueurs[0]["position"]
        p2 = self.joueurs[1]["position"]
        damier[p1[1] - 1][p1[0] - 1] = '1'
        damier[p2[1] - 1][p2[0] - 1] = '2'

        # Convert lists in "horizontaux" to tuples to make them hashable
        mh = set(tuple(pos) for pos in self.murs.get("horizontaux", []))

        lignes = []
        lignes.append("   " + "-" * 35)

        for y in range(9, 0, -1):
            # Ligne principale avec les cases
            ligne = f"{y} |"
            for x in range(1, 10):
                ligne += f" {damier[y - 1][x - 1]}  "
            ligne = ligne.rstrip() + " |"
            lignes.append(ligne)

            # Ligne des murs horizontaux (si ce n'est pas la dernière ligne)
            if y > 1:
                if (any((x, y - 1) in mh for x in range(1, 10)) ):
                    ligne_sep = "  |"
                    for x in range(1, 9):
                        ligne_sep += '-------' if (x, y - 1) in mh else '    '
                        ligne_sep += ''
                    ligne_sep +="|"
                else:
                    ligne_sep = "  |                                   |"
                lignes.append(ligne_sep)

        lignes.append("--|" + "-" * 35)
        lignes.append("  | 1   2   3   4   5   6   7   8   9")

        return "\n".join(lignes) + "\n"

    def __str__(self):
        """Représentation en art ascii de l'état actuel de la partie.

        Cette représentation est la même que celle du projet précédent.

        Returns:
            str: La chaîne de caractères de la représentation.
        """
        return self.formater_entête() + self.formater_le_damier()

    def déplacer_un_joueur(self, joueur, position):
        """Déplace un jeton.

        Pour le joueur spécifié, déplacer son jeton à la position spécifiée.

        Args:
            joueur (str): le nom du joueur.
            position (List[int, int]): La liste [x, y] de la position du jeton (1<=x<=9 et 1<=y<=9).

        Raises:
            QuoridorError: Le joueur n'existe pas.
            QuoridorError: La position est invalide (en dehors du damier).
            QuoridorError: La position est invalide pour l'état actuel du jeu.
        """
        #Étape 1: Vérifier si le joueur existe
        index_joueur = None
        for i, j in enumerate(self.joueurs):
            if j["nom"] == joueur:
                index_joueur = i
                break

        if index_joueur is None:
            raise QuoridorError(f"Le joueur {joueur} n'existe pas.")

        # Étape 2: Vérifier si la position est valide (en dehors du damier)
        x, y = position
        if not (1 <= x <= 9 and 1 <= y <= 9):
            raise QuoridorError(f"La position {position} est invalide.")

        # Étape 3: Vérification de la validité du déplacement
        position_acuelle = tuple(self.joueurs[index_joueur]["position"])
        position_souhaitée = tuple(position)

        graphe = construire_graphe(
            [j["position"] for j in self.joueurs],
            self.murs["horizontaux"],
            self.murs["verticaux"],
        )

        if position_souhaitée not in list(graphe.successors(position_acuelle)):
            raise QuoridorError(f"La position {position} est invalide pour l'état actuel du jeu.")

        # Étape 4: Déplacer le joueur
        self.joueurs[index_joueur]["position"] = list(position_souhaitée)

    def placer_un_mur(self, joueur, position, orientation):
        """Placer un mur.

        Pour le joueur spécifié, placer un mur à la position spécifiée.

        Args:
            joueur (str): le nom du joueur.
            position (List[int, int]): la liste [x, y] de la position du mur.
            orientation (str): l'orientation du mur ('MH' ou 'MV').

        Raises:
            QuoridorError: Le joueur n'existe pas.
            QuoridorError: Le joueur a déjà placé tous ses murs.
            QuoridorError: La position est invalide (en dehors du damier).
            QuoridorError: Un mur occupe déjà cette position.
            QuoridorError: Vous ne pouvez pas enfermer un joueur.
        """
        # Étape 1: Vérifier si le joueur existe
        #  ← ici, pour voir exactement ce que tu envoies
        index_joueur = None
        for i, j in enumerate(self.joueurs):
            if j["nom"] == joueur:
                index_joueur = i
                break

        if index_joueur is None:
            raise QuoridorError(f"Le joueur {joueur} n'existe pas.")

        # Étape 2: Vérifier que le joueur a encore des murs
        if self.joueurs[index_joueur]["murs"] <= 0:
            raise QuoridorError(f"Le joueur {joueur} a déjà placé tous ses murs.")

        # Étape 3: Vérifier que la position est dans les bornes (1 à 8)
        x, y = position
        if not (1 <= x <= 8 and 1 <= y <= 8):
            raise QuoridorError(f"La position {position} est invalide (en dehors du damier).")

        # Étape 4: Vérifier que l'orientation est valide
        if orientation not in ("MH", "MV"):
            raise QuoridorError("L'orientation du mur est invalide (doit être 'MH' ou 'MV').")

        # Étape 5: Vérifier qu'aucun mur n'occupe déjà cette position
        if orientation == "MH" and position in self.murs["horizontaux"]:
            raise QuoridorError(f"Un mur horizontal occupe déjà la position {position}.")
        if orientation == "MV" and position in self.murs["verticaux"]:
            raise QuoridorError(f"Un mur vertical occupe déjà la position {position}.")

        # Étape 6: Vérifier que ce mur ne bloque pas tous les chemins
        murs_temp = deepcopy(self.murs)
        if orientation == "MH":
            murs_temp["horizontaux"].append(position)
        else:
            murs_temp["verticaux"].append(position)

        graphe = construire_graphe(
            [j["position"] for j in self.joueurs],
            murs_temp["horizontaux"],
            murs_temp["verticaux"]
        )

        # Vérifie que chaque joueur a toujours un chemin vers sa cible
        cibles = ["B1", "B2"]
        for i, joueur_pos in enumerate([j["position"] for j in self.joueurs]):
            if not nx.has_path(graphe, tuple(joueur_pos), cibles[i]):
                raise QuoridorError("Vous ne pouvez pas enfermer un joueur.")

        # Étape 7: Ajouter le mur et décrémenter les murs du joueur

        if orientation == "MH":
            self.murs["horizontaux"].append(position)
        else:
            self.murs["verticaux"].append(position)

        self.joueurs[index_joueur]["murs"] -= 1

    def appliquer_un_coup(self, joueur, position, type_coup):
        """Applique un coup de type déplacement ou mur pour un joueur donné.

        Args:
            joueur (str): le nom du joueur.
            position (list[int]): la position cible (déplacement ou mur).
            type_coup (str): le type de coup ('D' pour déplacement, 'M' pour mur).

        Returns:
            tuple: (type_coup, position)

        Raises:
            QuoridorError: joueur invalide, type de coup invalide, position invalide, ou partie terminée.
        """
        # Vérifier si la partie est déjà terminée
        if self.partie_terminée():
            raise QuoridorError("La partie est déjà terminée.")

        # Vérifier que le joueur existe
        index_joueur = None
        for i, j in enumerate(self.joueurs):
            if j["nom"] == joueur:
                index_joueur = i
                break
        if index_joueur is None:
            raise QuoridorError(f"Le joueur {joueur} n'existe pas.")

        # Vérifier le type de coup
        if type_coup not in ("D", "M"):
            raise QuoridorError(f"Type de coup invalide: {type_coup}")

        # Appliquer le coup
        if type_coup == "D":
            self.déplacer_un_joueur(joueur, position)
        elif type_coup == "M":
            if len(position) != 3:
                raise QuoridorError("Le coup de type 'M' doit inclure l'orientation en troisième position.")
            # position = [x, y, orientation]
            x, y, orientation = position
            self.placer_un_mur(joueur, [x, y], orientation)

        # Incrémenter le tour si c'est le joueur 2
        if index_joueur == 1:
            self.tour += 1

        return (type_coup, position)

    def sélectionner_un_coup(self, joueur):
        """Récupérer le coup.

        Notez que seul 2 questions devrait être posée à l'utilisateur.

        Notez aussi que cette méthode ne devrait pas modifier l'état du jeu.

        Args:
            joueur (str): le nom du joueur.

        Raises:
            QuoridorError: Le joueur n'existe pas.
            QuoridorError: Le type de coup est invalide.
            QuoridorError: La position est invalide (en dehors du damier).

        Returns:
            tuple: Un tuple composé d'un type de coup et de la position.
               Le type de coup est une chaîne de caractères.
               La position est une liste de 2 entier [x, y].
        """
        # Vérifier que le joueur existe
        if joueur not in [j["nom"] for j in self.joueurs]:
            raise QuoridorError("Le joueur spécifié n'existe pas.")

        # Demander le type de coup
        type_coup = input("Quel type de coup voulez-vous jouer? [D]éplacement ou [M]ur: ").strip().upper()
        if type_coup not in ("D", "M"):
            raise QuoridorError("Le type de coup est invalide.")

        try:
            if type_coup == "D":
                x = int(input("Entrez la position x de destination: "))
                y = int(input("Entrez la position y de destination: "))
                if not (1 <= x <= 9 and 1 <= y <= 9):
                    raise QuoridorError("La position est invalide (en dehors du damier).")
                return "D", [x, y]

            if type_coup == "M":
                x = int(input("Entrez la position x du mur: "))
                y = int(input("Entrez la position y du mur: "))
                orientation = input("Entrez l'orientation du mur [MH ou MV]: ").strip().upper()
                if not (1 <= x <= 8 and 1 <= y <= 8):
                    raise QuoridorError("La position du mur est invalide (en dehors du damier).")
                if orientation not in ("MH", "MV"):
                    raise QuoridorError("L'orientation du mur est invalide.")
                return "M", [x, y, orientation]

        except ValueError as exc:
            raise QuoridorError("La position doit être composée de nombres entiers.") from exc

    def partie_terminée(self):
        """Retourne le nom du gagnant si la partie est terminée, sinon False."""
        if self.joueurs[0]["position"][1] == 9:
            return self.joueurs[0]["nom"]
        if self.joueurs[1]["position"][1] == 1:
            return self.joueurs[1]["nom"]
        return False

    def jouer_un_coup(self, joueur):
        """Jouer un coup automatique pour un joueur.

        Pour le joueur spécifié, jouer automatiquement son meilleur coup pour l'état actuel
        de la partie. Ce coup est soit le déplacement de son jeton, soit le placement d'un
        mur horizontal ou vertical. La priorité est donnée au placement d'un mur si
        cela empêche l'adversaire de gagner au prochain coup.

        Args:
            joueur (str): le nom du joueur.

        Raises:
            QuoridorError: Le joueur n'existe pas.
            QuoridorError: La partie est déjà terminée.

        Returns:
            tuple: Un tuple composé d'un type de coup ('D', 'M') et de la position.
                   Pour 'D': [x, y]
                   Pour 'M': [x, y, orientation ('MH' ou 'MV')]
        """
        if self.partie_terminée():
            raise QuoridorError("La partie est déjà terminée.")

        id_joueur = -1
        for i, j in enumerate(self.joueurs):
            if j["nom"] == joueur:
                id_joueur = i
                break
        if id_joueur == -1:
            raise QuoridorError(f"Le joueur {joueur} n'existe pas.")

        id_adversaire = 1 - id_joueur
        pos_joueur = tuple(self.joueurs[id_joueur]["position"])
        pos_adversaire = tuple(self.joueurs[id_adversaire]["position"])
        murs_restants = self.joueurs[id_joueur]["murs"]

        cible_joueur = "B1" if id_joueur == 0 else "B2"
        cible_adversaire = "B2" if id_joueur == 0 else "B1"

        if murs_restants > 0:
            graphe_actuel = construire_graphe(
                [self.joueurs[0]["position"], self.joueurs[1]["position"]],
                self.murs["horizontaux"],
                self.murs["verticaux"]
            )

            if nx.has_path(graphe_actuel, pos_adversaire, cible_adversaire):
                chemin_adversaire = nx.shortest_path(graphe_actuel, pos_adversaire, cible_adversaire)
                ligne_victoire_adversaire = 9 if id_adversaire == 0 else 1

                if len(chemin_adversaire) > 1 and isinstance(chemin_adversaire[1], tuple) and chemin_adversaire[1][1] == ligne_victoire_adversaire:
                    coup_bloquant = self._trouver_coup_bloquant(id_joueur, id_adversaire, cible_joueur, cible_adversaire)
                    if coup_bloquant:
                        return coup_bloquant

        graphe_final = construire_graphe(
            [self.joueurs[0]["position"], self.joueurs[1]["position"]],
            self.murs["horizontaux"],
            self.murs["verticaux"]
        )

        if nx.has_path(graphe_final, pos_joueur, cible_joueur):
            chemin_joueur = nx.shortest_path(graphe_final, pos_joueur, cible_joueur)
            prochaine_position = chemin_joueur[1] if len(chemin_joueur) > 1 else cible_joueur

            if isinstance(prochaine_position, str):
                 if len(chemin_joueur) > 1:
                    prochaine_position = chemin_joueur[-2]
                 else:
                     raise QuoridorError("Erreur de chemin: Pas de case intermédiaire avant la cible.")

            if isinstance(prochaine_position, tuple):
                return ("D", list(prochaine_position))
            else:
                raise QuoridorError(f"Erreur inattendue: prochaine_position invalide '{prochaine_position}'.")

        else:
            voisins = list(graphe_final.successors(pos_joueur))
            if voisins:
                voisins_reels = [v for v in voisins if isinstance(v, tuple)]
                if voisins_reels:
                    return ("D", list(voisins_reels[0]))

            raise QuoridorError("Aucun coup valide trouvé (pas de chemin et pas de voisins?).")


    def _trouver_coup_bloquant(self, id_joueur, id_adversaire, cible_joueur, cible_adversaire):
        """
        Cherche un placement de mur qui bloque l'adversaire sans bloquer le joueur.
        Helper pour jouer_un_coup.
        """
        pos_joueur = tuple(self.joueurs[id_joueur]["position"])
        pos_adversaire = tuple(self.joueurs[id_adversaire]["position"])


        for x in range(1, 9):
            for y in range(1, 9):
                for orientation in ["MH", "MV"]:
                    pos_mur = [x, y]
                    murs_h_temp = deepcopy(self.murs["horizontaux"])
                    murs_v_temp = deepcopy(self.murs["verticaux"])
                    mur_ajoute = False # Flag pour savoir si on a tenté d'ajouter
                    placement_valide = True # Flag pour la validation initiale

                    # 1. Valider le placement potentiel du mur (simplifié)
                    #    et préparer les listes temporaires
                    if orientation == "MH":
                         # Vérifie si un mur H est déjà là, ou juste à gauche/droite
                         # Vérifie si un mur V croise au même point (simplifié)
                        if pos_mur in murs_h_temp or \
                           [pos_mur[0]-1, pos_mur[1]] in murs_h_temp or \
                           [pos_mur[0]+1, pos_mur[1]] in murs_h_temp or \
                           (pos_mur in murs_v_temp): # Chevauchement simple avec un mur V
                            placement_valide = False
                        else:
                            murs_h_temp.append(pos_mur)
                            mur_ajoute = True
                    else: # orientation == "MV"
                        # Vérifie si un mur V est déjà là, ou juste au dessus/dessous
                        # Vérifie si un mur H croise au même point (simplifié)
                        if pos_mur in murs_v_temp or \
                           [pos_mur[0], pos_mur[1]-1] in murs_v_temp or \
                           [pos_mur[0], pos_mur[1]+1] in murs_v_temp or \
                           (pos_mur in murs_h_temp): # Chevauchement simple avec un mur H
                            placement_valide = False
                        else:
                            murs_v_temp.append(pos_mur)
                            mur_ajoute = True

                    # Si la validation initiale échoue, passer au mur suivant
                    if not placement_valide:
                        # if pos_mur == [4, 1] and orientation == 'MV':
                        continue

                    # Si le mur n'a pas pu être ajouté pour une raison quelconque (ne devrait pas arriver ici si valide)
                    if not mur_ajoute:
                         continue

                    # 2. Essayer de construire le graphe et vérifier les chemins
                    try:
                        # Essayer de construire le graphe AVEC le mur temporaire
                        graphe_temp = construire_graphe(
                            [self.joueurs[0]["position"], self.joueurs[1]["position"]],
                            murs_h_temp,
                            murs_v_temp
                        )

                        # Si la construction du graphe réussit, vérifier les chemins
                        adversaire_bloque = not nx.has_path(graphe_temp, pos_adversaire, cible_adversaire)
                        joueur_non_bloque = nx.has_path(graphe_temp, pos_joueur, cible_joueur)

                        # Imprimer l'évaluation pour les murs spécifiques en [4, 1
                        # Si ce mur remplit les conditions de blocage
                        if adversaire_bloque and joueur_non_bloque:
                            return ("M", [x, y, orientation])

                    except nx.NetworkXError as e:
                         continue
                    except Exception as e:
                         # Attrape toute autre exception inattendue
                         continue

        return None # Aucun coup bloquant trouvé

def interpréter_la_ligne_de_commande():
    """
    Génère un interpréteur de commande pour le jeu Quoridor Phase 3.

    Prend l'IDUL comme argument positionnel et accepte les options
    pour les modes automatique et graphique.

    Returns:
        Namespace: Un objet Namespace contenant les arguments parseés.
    """
    parser = argparse.ArgumentParser(
        description='Jeu Quoridor',
        usage='main.py [-h] [-a] [-x] idul' # Correspond à l'usage demandé
    )

    parser.add_argument(
        'idul',
        help='IDUL du joueur'
    )

    parser.add_argument(
        '-a', '--automatique',
        action='store_true', # Stocke True si l'option est présente, False sinon
        help='Activer le mode automatique.'
    )

    parser.add_argument(
        '-x', '--graphique',
        action='store_true', # Stocke True si l'option est présente, False sinon
        help='Activer le mode graphique.'
    )

    return parser.parse_args()