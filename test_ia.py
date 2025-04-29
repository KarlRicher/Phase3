# Dans votre fichier de test (ex: tests.py ou test_ia.py)
from quoridor import Quoridor
# from quoridor_error import QuoridorError # Si vous testez des cas d'erreur

# --- EXEMPLES DE TESTS UNITAIRES POUR jouer_un_coup ---

def test_jouer_un_coup_blocage_obligatoire_reussi():
    """
    Teste si l'IA place un mur pour bloquer l'adversaire
    quand celui-ci est à une case de gagner.
    """
    # Scénario: Joueur 2 (adv) est en [5, 2], Joueur 1 (ia) en [5, 5] avec des murs.
    # Un mur en [4, 1] MH bloquerait la victoire directe de Joueur 2.
    joueurs = [
        {"nom": "IA_Test", "murs": 5, "position": [5, 5]},
        {"nom": "Adversaire", "murs": 10, "position": [5, 2]},
    ]
    murs = {"horizontaux": [], "verticaux": []}
    partie = Quoridor(joueurs, murs)

    # C'est au tour de l'IA (Joueur 1) de jouer
    coup_attendu = ('M', [4, 1, 'MH']) # ou [5, 1, 'MH'] selon l'implémentation exacte de _trouver_coup_bloquant
    coup_calcule = partie.jouer_un_coup("IA_Test")

    # Vérification: Le coup doit être un mur à la position bloquante
    # Note: Il peut y avoir plusieurs murs bloquants valides. Ce test suppose [4,1,MH].
    # Adaptez si votre fonction _trouver_coup_bloquant en choisit un autre (ex: [5,1,MH]).
    assert coup_calcule == coup_attendu, \
        f"Blocage obligatoire attendu {coup_attendu}, mais obtenu {coup_calcule}"
    print("test_jouer_un_coup_blocage_obligatoire_reussi: PASS")


def test_jouer_un_coup_pas_de_murs_pour_bloquer():
    """
    Teste si l'IA se déplace quand elle n'a plus de murs,
    même si l'adversaire est sur le point de gagner.
    """
    # Scénario: Joueur 2 (adv) en [5, 2], Joueur 1 (ia) en [5, 5] SANS murs.
    joueurs = [
        {"nom": "IA_Test", "murs": 0, "position": [5, 5]}, # 0 murs !
        {"nom": "Adversaire", "murs": 10, "position": [5, 2]},
    ]
    murs = {"horizontaux": [], "verticaux": []}
    partie = Quoridor(joueurs, murs)

    # C'est au tour de l'IA (Joueur 1) de jouer
    coup_calcule = partie.jouer_un_coup("IA_Test")

    # Vérification: Le coup doit être un déplacement ('D') car pas de murs
    assert coup_calcule[0] == 'D', \
        f"Déplacement attendu (pas de murs), mais obtenu {coup_calcule}"
    # Optionnel: vérifier que le déplacement est valide/logique (ex: vers [5, 6])
    # assert coup_calcule[1] == [5, 6] # si c'est le plus court chemin
    print("test_jouer_un_coup_pas_de_murs_pour_bloquer: PASS")


def test_jouer_un_coup_deplacement_normal():
    """
    Teste si l'IA choisit un déplacement sur le plus court chemin
    quand aucune situation de blocage n'est présente.
    """
    # Scénario: Début de partie ou milieu, pas de menace imminente.
    joueurs = [
        {"nom": "Joueur1", "murs": 8, "position": [5, 3]}, # IA
        {"nom": "Joueur2", "murs": 8, "position": [5, 7]},
    ]
    murs = {"horizontaux": [[4,5]], "verticaux": []} # Un mur au milieu
    partie = Quoridor(joueurs, murs)

    # C'est au tour de Joueur1 (IA)
    # Le plus court chemin vers B1 (ligne 9) depuis [5, 3] est d'aller en [5, 4]
    coup_attendu = ('D', [5, 4])
    coup_calcule = partie.jouer_un_coup("Joueur1")

    # Vérification: Le coup doit être un déplacement vers la case suivante du chemin le plus court
    assert coup_calcule == coup_attendu, \
        f"Déplacement normal attendu {coup_attendu}, mais obtenu {coup_calcule}"
    print("test_jouer_un_coup_deplacement_normal: PASS")

def test_jouer_un_coup_blocage_qui_enfermerait_ia():
    """
    Teste si l'IA ne place pas un mur qui la bloquerait elle-même,
    même si ce mur bloquerait aussi l'adversaire sur le point de gagner.
    """
    # Scénario: Joueur 2 (adv) en [1, 8]. Joueur 1 (ia) en [1, 6].
    # Un mur en [1, 7] MV bloquerait J2.
    # MAIS, s'il y a aussi des murs en [2, 6] MH et [2, 7] MH,
    # placer [1, 7] MV enfermerait complètement J1.
    joueurs = [
        {"nom": "IA_Bloquée", "murs": 5, "position": [1, 6]}, # IA
        {"nom": "Adv_Gagnant", "murs": 10, "position": [1, 8]}, # Adversaire proche
    ]
    # Murs créant un couloir pour l'IA, qui serait fermé par le mur bloquant
    murs = {
        "horizontaux": [[1, 7], [2, 7]], # Murs à droite et au dessus de la case [1,7]
        "verticaux": []
    }
    partie = Quoridor(joueurs, murs)

    # C'est au tour de l'IA
    coup_calcule = partie.jouer_un_coup("IA_Bloquée")

    # Vérification: L'IA ne doit PAS placer le mur en [1, 7] MV, elle doit se déplacer.
    # Le seul déplacement possible est [2, 6]
    coup_attendu_deplacement = ('D', [2, 6])
    assert coup_calcule[0] == 'D', \
        f"Déplacement attendu (car mur bloquerait IA), mais obtenu {coup_calcule}"
    assert coup_calcule == coup_attendu_deplacement, \
        f"Déplacement attendu vers [2, 6], mais obtenu {coup_calcule}"
    print("test_jouer_un_coup_blocage_qui_enfermerait_ia: PASS")

if __name__ == '__main__':
    print("--- Début des tests IA ---") # Ajout pour voir si le bloc est atteint
    test_jouer_un_coup_blocage_obligatoire_reussi()
    test_jouer_un_coup_pas_de_murs_pour_bloquer()
    test_jouer_un_coup_deplacement_normal()
    test_jouer_un_coup_blocage_qui_enfermerait_ia()
    print("--- Fin des tests IA ---") # Ajout pour voir si le bloc se termine


# --- Pour exécuter ces tests ---
# Si vous mettez ces fonctions dans tests.py et que ce fichier contient déjà
# if __name__ == "__main__": ...
# ajoutez simplement les appels à ces nouvelles fonctions :
#
# if __name__ == "__main__":
#     test_formater_entête_pour_une_nouvelle_partie()
#     print("Test de formater_entête pour une nouvelle partie réussi")
#     # ... autres tests existants ...
#     print("-" * 20)
#     # Nouveaux tests IA
#     test_jouer_un_coup_blocage_obligatoire_reussi()
#     test_jouer_un_coup_pas_de_murs_pour_bloquer()
#     test_jouer_un_coup_deplacement_normal()
#     test_jouer_un_coup_blocage_qui_enfermerait_ia()


# Ou si vous créez un nouveau fichier test_ia.py:
# Ajoutez à la fin du fichier test_ia.py :
# if __name__ == '__main__':
#     test_jouer_un_coup_blocage_obligatoire_reussi()
#     test_jouer_un_coup_pas_de_murs_pour_bloquer()
#     test_jouer_un_coup_deplacement_normal()
#     test_jouer_un_coup_blocage_qui_enfermerait_ia()
#
# Et exécutez avec : python test_ia.py