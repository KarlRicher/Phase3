from quoridor import Quoridor

états_de_jeu = [
    # Test 1: État initial
    {
        "description": "État initial sans murs",
        "joueurs": [
            {"nom": "joueur1", "murs": 10, "position": [5, 1]},
            {"nom": "joueur2", "murs": 10, "position": [5, 9]},
        ],
        "murs": {"horizontaux": [], "verticaux": []}
    },

    # Test 2: Un mur horizontal au centre
    {
        "description": "Mur horizontal au centre",
        "joueurs": [
            {"nom": "joueur1", "murs": 9, "position": [5, 2]},
            {"nom": "joueur2", "murs": 10, "position": [5, 9]},
        ],
        "murs": {"horizontaux": [[4, 5]], "verticaux": []}
    },

    # Test 3: Un mur vertical au centre
    {
        "description": "Mur vertical au centre",
        "joueurs": [
            {"nom": "joueur1", "murs": 9, "position": [4, 2]},
            {"nom": "joueur2", "murs": 10, "position": [6, 9]},
        ],
        "murs": {"horizontaux": [], "verticaux": [[5, 5]]}
    },

    # Test 4: Plusieurs murs superposés
    {
        "description": "Murs en croix au centre",
        "joueurs": [
            {"nom": "joueur1", "murs": 7, "position": [5, 5]},
            {"nom": "joueur2", "murs": 8, "position": [4, 4]},
        ],
        "murs": {"horizontaux": [[4, 5], [5, 5]], "verticaux": [[5, 4], [5, 5]]}
    },

    # Test 5: Bords de la grille
    {
        "description": "Murs sur les bords",
        "joueurs": [
            {"nom": "joueur1", "murs": 5, "position": [1, 1]},
            {"nom": "joueur2", "murs": 5, "position": [9, 9]},
        ],
        "murs": {
            "horizontaux": [[1, 1], [7, 9]],
            "verticaux": [[1, 1], [9, 7]]
        }
    },

    # Test 6: Tous les murs d’un joueur utilisés
    {
        "description": "Joueur1 sans murs restants",
        "joueurs": [
            {"nom": "joueur1", "murs": 0, "position": [5, 6]},
            {"nom": "joueur2", "murs": 10, "position": [5, 4]},
        ],
        "murs": {"horizontaux": [[2, 3], [3, 4]], "verticaux": [[4, 5], [5, 6]]}
    },

    # Test 7: Murs collés
    {
        "description": "Murs alignés en série",
        "joueurs": [
            {"nom": "joueur1", "murs": 8, "position": [3, 3]},
            {"nom": "joueur2", "murs": 8, "position": [7, 7]},
        ],
        "murs": {
            "horizontaux": [[3, 4], [4, 4], [5, 4]],
            "verticaux": [[6, 5], [6, 6], [6, 7]]
        }
    },

    # Test 8: Les deux joueurs au même endroit (collision)
    {
        "description": "Les deux joueurs sur la même case",
        "joueurs": [
            {"nom": "joueur1", "murs": 9, "position": [5, 5]},
            {"nom": "joueur2", "murs": 9, "position": [5, 5]},
        ],
        "murs": {"horizontaux": [], "verticaux": []}
    },
]

# Exécution des tests
for i, etat in enumerate(états_de_jeu):
    print(f"\n--- Test {i + 1}: {etat['description']} ---")
    q = Quoridor(etat["joueurs"], etat["murs"])
    print(q)
