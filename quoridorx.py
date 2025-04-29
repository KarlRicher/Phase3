"""
Module pour le jeu Quoridor avec une interface graphique utilisant Turtle.

Ce module étend la logique de jeu de la classe Quoridor (supposée définie ailleurs)
en ajoutant une visualisation graphique interactive.
"""
import time
import turtle
from quoridor import Quoridor

# Note: time import removed as it wasn't used in the final main.py logic provided
# import time

class QuoridorX(Quoridor):
    """
    Classe pour encapsuler le jeu Quoridor avec affichage graphique Turtle.
    Hérite de la classe Quoridor pour la logique du jeu.
    """
    def __init__(self, joueurs, murs=None, tour=1):
        """
        Constructeur de la classe QuoridorX.

        Initialise la logique du jeu via Quoridor et prépare l'affichage graphique.

        Args:
            joueurs (List): Liste des dictionnaires des joueurs.
            murs (Dict, optionnel): Dictionnaire des murs initiaux.
            tour (int, optionnel): Tour initial du jeu.
        """
        super().__init__(joueurs, murs, tour) # Initialise Quoridor avec joueurs, murs ET tour
        self.screen = turtle.Screen()
        self.screen.title("QuoridorX")
        self.screen.setup(width=600, height=600)
        self.screen.tracer(0) # Désactive l'animation automatique pour mises à jour manuelles
        self.grid_size = 50 # Taille visuelle d'une case (ajustez si besoin)
        self.offset_x = -self.grid_size * 4.5 # Décalage pour centrer la grille 0,0
        self.offset_y = -self.grid_size * 4.5
        self.player_turtles = []
        self.wall_drawing_turtle = turtle.Turtle() # Tortue dédiée au dessin des murs
        self.wall_drawing_turtle.hideturtle()
        self.wall_drawing_turtle.penup()
        self.wall_drawing_turtle.speed(0)
        self.wall_drawing_turtle.color("black")
        # S'assurer que le constructeur appelle l'initialisation graphique
        self.init_graphics()
        # L'affichage initial se fera lors du premier appel à afficher() dans la boucle main

    def _get_screen_coords(self, grid_x, grid_y):
        """Convertit les coordonnées de grille (1-9) en coordonnées Turtle."""
        screen_x = self.offset_x + (grid_x - 1) * self.grid_size
        screen_y = self.offset_y + (grid_y - 1) * self.grid_size
        return screen_x, screen_y

    def init_graphics(self):
        """Dessine la grille de jeu statique et initialise les tortues des joueurs."""
        # --- Dessin de la grille (une seule fois) ---
        grid_turtle = turtle.Turtle()
        grid_turtle.hideturtle()
        grid_turtle.penup()
        grid_turtle.speed(0)
        grid_turtle.color("grey") # Couleur de la grille

        # Lignes verticales
        for i in range(10):
            x = self.offset_x + i * self.grid_size - self.grid_size / 2
            grid_turtle.goto(x, self.offset_y - self.grid_size / 2)
            grid_turtle.pendown()
            grid_turtle.goto(x, self.offset_y + 8.5 * self.grid_size)
            grid_turtle.penup()

        # Lignes horizontales
        for i in range(10):
            y = self.offset_y + i * self.grid_size - self.grid_size / 2
            grid_turtle.goto(self.offset_x - self.grid_size / 2, y)
            grid_turtle.pendown()
            grid_turtle.goto(self.offset_x + 8.5 * self.grid_size, y)
            grid_turtle.penup()

        # --- Création des tortues pour les joueurs ---
        # Joueur 1
        p1_turtle = turtle.Turtle(shape="circle")
        p1_turtle.color("red")
        p1_turtle.penup()
        self.player_turtles.append(p1_turtle)

        # Joueur 2
        p2_turtle = turtle.Turtle(shape="circle")
        p2_turtle.color("blue")
        p2_turtle.penup()
        self.player_turtles.append(p2_turtle)

        # Cacher la tortue par défaut (la flèche au centre)
        turtle.hideturtle()


    def update_screen(self):
        """Met à jour l'affichage des éléments dynamiques (joueurs, murs)."""
        # --- Placer les joueurs ---
        for i, joueur in enumerate(self.joueurs):
            x, y = joueur["position"]
            sx, sy = self._get_screen_coords(x, y)
            self.player_turtles[i].goto(sx, sy) # Positionne au centre de la case

        # --- Dessiner les murs ---
        # Effacer les anciens murs dessinés par cette tortue
        self.wall_drawing_turtle.clear()

        # Murs horizontaux (barre entre y et y-1)
        self.wall_drawing_turtle.pensize(5) # Épaisseur du mur
        for x, y in self.murs["horizontaux"]:
            # Le mur H [x, y] est entre (x, y) et (x+1, y) ET entre (x, y-1) et (x+1, y-1)
            # Il bloque le passage vertical entre la ligne y-1 et y, sur les colonnes x et x+1
            # On dessine une barre horizontale sur la ligne de grille y-1, entre x-1 et x+1
            start_x, start_y = self._get_screen_coords(x, y) # Coin bas-gauche de la case [x,y]
            # Coordonnée Y de la ligne de séparation
            sep_y = start_y - self.grid_size / 2
            # Coordonnée X du début du mur (bord gauche de la case x)
            sep_start_x = start_x - self.grid_size / 2
            # Coordonnée X de la fin du mur (bord droit de la case x+1)
            sep_end_x = sep_start_x + 2 * self.grid_size

            self.wall_drawing_turtle.penup()
            self.wall_drawing_turtle.goto(sep_start_x, sep_y)
            self.wall_drawing_turtle.pendown()
            self.wall_drawing_turtle.goto(sep_end_x, sep_y)
            self.wall_drawing_turtle.penup()

        # Murs verticaux (barre entre x et x-1)
        for x, y in self.murs["verticaux"]:
            # Le mur V [x, y] est entre (x, y) et (x, y+1) ET entre (x-1, y) et (x-1, y+1)
            # Il bloque le passage horizontal entre la colonne x-1 et x, sur les lignes y et y+1
            # On dessine une barre verticale sur la ligne de grille x-1, entre y-1 et y+1
            start_x, start_y = self._get_screen_coords(x, y) # Coin bas-gauche de la case [x,y]
            # Coordonnée X de la ligne de séparation
            sep_x = start_x - self.grid_size / 2
            # Coordonnée Y du début du mur (bord bas de la case y)
            sep_start_y = start_y - self.grid_size / 2
            # Coordonnée Y de la fin du mur (bord haut de la case y+1)
            sep_end_y = sep_start_y + 2 * self.grid_size

            self.wall_drawing_turtle.penup()
            self.wall_drawing_turtle.goto(sep_x, sep_start_y)
            self.wall_drawing_turtle.pendown()
            self.wall_drawing_turtle.goto(sep_x, sep_end_y)
            self.wall_drawing_turtle.penup()

        # Mettre à jour l'écran après tous les dessins
        self.screen.update()

    # Hérite de __str__ de Quoridor si on veut l'affichage ASCII aussi,
    # ou on peut le redéfinir pour indiquer que c'est une instance graphique.
    # def __str__(self):
    #     # Optionnel: Appeler le __str__ parent pour l'état en console même en mode graphique
    #     # return super().__str__()
    #     return f"QuoridorX Game State (Tour: {self.tour})"

    def afficher(self):
        """Méthode publique pour demander une mise à jour de l'affichage."""
        self.update_screen()

    # Optionnel: Méthode pour gérer la fermeture propre de la fenêtre
    def close_window(self):
        """Ferme la fenêtre turtle."""
        try:
            self.screen.bye()
        except turtle.Terminator:
            pass # Fenêtre déjà fermée


# --- Bloc de test optionnel ---
if __name__ == '__main__':
    # Exemple d'utilisation pour tester l'affichage
    joueurs_test = [
        {"nom": "Joueur Rouge", "murs": 10, "position": [5, 1]},
        {"nom": "Joueur Bleu", "murs": 10, "position": [5, 9]}
    ]
    murs_test = {
        "horizontaux": [[4, 5], [5, 5]], # Un mur au centre
        "verticaux": [[5, 4]]  # Un mur vertical
    }

    print("Lancement du test QuoridorX...")
    jeu_graphique = QuoridorX(joueurs_test, murs_test)

    # Simuler quelques tours pour voir les mises à jour
    try:
        # Tour 1 - J1 déplace
        print("Tour 1 - J1 déplace...")
        jeu_graphique.joueurs[0]["position"] = [5, 2]
        jeu_graphique.afficher()
        time.sleep(2) # Pause pour voir l'état

        # Tour 1 - J2 place mur
        print("Tour 1 - J2 place mur...")
        jeu_graphique.joueurs[1]["position"] = [4, 9] # Petit déplacement J2
        jeu_graphique.murs["verticaux"].append([4, 8])
        jeu_graphique.joueurs[1]["murs"] -= 1
        jeu_graphique.tour += 1
        jeu_graphique.afficher()
        time.sleep(2) # Pause pour voir l'état

        print("Affichage initial et simulation terminés.")
        print("Cliquez sur la fenêtre pour quitter.")
        jeu_graphique.screen.exitonclick()

    except turtle.Terminator:
        print("Fenêtre fermée pendant le test.")
    except Exception as e:
        print(f"Une erreur est survenue: {e}")
        import traceback
        traceback.print_exc()
