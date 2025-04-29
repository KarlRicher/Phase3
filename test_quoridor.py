import unittest
from quoridor import Quoridor
from quoridor_error import QuoridorError


class TestJouerUnCoup(unittest.TestCase):

    def setUp(self):
        self.joueurs = [
            {"nom": "ordi", "murs": 10, "position": [5, 2]},
            {"nom": "humain", "murs": 10, "position": [5, 8]},
        ]
        self.jeu = Quoridor(self.joueurs)

    def test_deplacement_simple(self):
        coup = self.jeu.jouer_un_coup("ordi")
        self.assertEqual(coup, ('D', [5, 3]))  # Vérifie que l'ordi avance d'une case

    def test_deplacement_avec_mur(self):
        self.jeu.murs = {"horizontaux": [[5, 3]], "verticaux": []}  # Mur horizontal devant l'ordi
        coup = self.jeu.jouer_un_coup("ordi")
        self.assertIn(coup, [('D', [4, 2]), ('D', [6, 2])])  # Vérifie que l'ordi va à gauche ou à droite

    def test_victoire(self):
        self.jeu.joueurs[0]["position"] = [5, 8]  # Ordi proche de gagner
        coup = self.jeu.jouer_un_coup("ordi")
        self.assertEqual(self.jeu.partie_terminée(), "ordi")  # Vérifie que la partie est terminée

    def test_pas_de_chemin(self):
        # Créez une configuration de murs qui bloque complètement l'ordi
        self.jeu.murs = {
            "horizontaux": [[1, 2], [2, 2], [3, 2], [4, 2], [5, 2], [6, 2], [7, 2], [8, 2], [9, 2]],
            "verticaux": [[1, 2], [1, 3], [1, 4], [1, 5], [1, 6], [1, 7], [1, 8]],
        }
        coup = self.jeu.jouer_un_coup("ordi")
        self.assertIsNone(coup)  # Vérifie que la fonction gère bien le cas où il n'y a pas de chemin

if __name__ == '__main__':
    unittest.main()