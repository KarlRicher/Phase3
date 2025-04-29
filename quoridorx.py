import turtle
from quoridor import Quoridor
import time  # Optionnel

class QuoridorX(Quoridor):
    def __init__(self, joueurs, murs=None):
        super().__init__(joueurs, murs)  # Initialise Quoridor
        self.screen = turtle.Screen()
        self.screen.title("QuoridorX")
        self.screen.setup(width=600, height=600)  # Ajustez la taille selon vos besoins
        self.screen.tracer(0)  # Désactive l'animation automatique
        self.grid_size = 60  # Taille d'une case de la grille
        self.player_turtles = []
        self.wall_turtles = []
        self.init_grid()
        self.update_screen()

    def init_grid(self):
        """Dessine la grille de jeu et initialise les tortues des joueurs."""
        # Dessiner les lignes de la grille
        grid_turtle = turtle.Turtle()
        grid_turtle.speed(0)  # Vitesse maximale
        grid_turtle.penup()
        for x in range(-4, 5):
            grid_turtle.goto(x * self.grid_size, -4 * self.grid_size)
            grid_turtle.pendown()
            grid_turtle.goto(x * self.grid_size, 4 * self.grid_size)
            grid_turtle.penup()
        for y in range(-4, 5):
            grid_turtle.goto(-4 * self.grid_size, y * self.grid_size)
            grid_turtle.pendown()
            grid_turtle.goto(4 * self.grid_size, y * self.grid_size)
            grid_turtle.penup()
        grid_turtle.hideturtle()

        # Créer les tortues pour les joueurs
        player1_turtle = turtle.Turtle(shape="circle")
        player1_turtle.color("red")
        player1_turtle.penup()
        self.player_turtles.append(player1_turtle)

        player2_turtle = turtle.Turtle(shape="circle")
        player2_turtle.color("blue")
        player2_turtle.penup()
        self.player_turtles.append(player2_turtle)
    
    def update_screen(self):
        """Met à jour l'affichage de la fenêtre."""
        # Placer les joueurs
        for i, joueur in enumerate(self.joueurs):
            x, y = joueur["position"]
            self.player_turtles[i].goto((x - 5) * self.grid_size, (y - 5) * self.grid_size)  # Ajustement des coordonnées
        
        # Placer les murs
        for wall in self.wall_turtles:
            wall.clear()
            wall.hideturtle()
        self.wall_turtles = []

        for x, y in self.murs["horizontaux"]:
            wall_turtle = turtle.Turtle()
            wall_turtle.shape("square")
            wall_turtle.color("black")
            wall_turtle.shapesize(stretch_wid=0.5, stretch_len=2)  # Ajuster la taille du mur horizontal
            wall_turtle.penup()
            wall_turtle.goto((x - 4.5) * self.grid_size, (y - 4.5) * self.grid_size)  # Positionnement du mur
            self.wall_turtles.append(wall_turtle)

        for x, y in self.murs["verticaux"]:
            wall_turtle = turtle.Turtle()
            wall_turtle.shape("square")
            wall_turtle.color("black")
            wall_turtle.shapesize(stretch_wid=2, stretch_len=0.5)  # Ajuster la taille du mur vertical
            wall_turtle.penup()
            wall_turtle.goto((x - 4.5) * self.grid_size, (y - 4.5) * self.grid_size)
            self.wall_turtles.append(wall_turtle)

        self.screen.update()

    def __str__(self):
        return "QuoridorX game"  # Ou une autre chaîne temporaire
    
    def afficher(self):
        self.update_screen()

    def run(self):
        turtle.mainloop()

if __name__ == '__main__':
    joueurs = [
        {"nom": "J1", "murs": 10, "position": [5, 1]},
        {"nom": "J2", "murs": 10, "position": [5, 9]}
    ]
    game = QuoridorX(joueurs)
    game.run()