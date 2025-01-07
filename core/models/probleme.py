from typing import List
from core.models.city import City

Etat = List[City]  # Un état est une liste de villes (City)

class Probleme:
    """
    Représente le problème avec un état initial et un tableau de villes.
    """
    def __init__(self, etat_initial: Etat, villes: List[City]):
        self.etat_initial = etat_initial
        self.villes = villes

class Noeud:
    """
    Représente un nœud de l'arbre de recherche avec un état courant
    et le coût (valeur) associé.
    """
    def __init__(self, etat: Etat, valeur: float):
        self.etat = etat
        self.valeur = valeur
