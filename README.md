# NetOpt: Algorithmes de Recherche Opérationnelle pour les Réseaux & Télécoms

> Application desktop Python qui exécute 9 algorithmes classiques de RO appliqués à des problèmes télécoms concrets — plus court chemin, flot maximum, arbres couvrants, allocation de fréquences et optimisation du transport. Chaque algorithme génère son propre graphe ou matrice de coûts aléatoire, effectue le calcul et visualise le résultat graphiquement.

Réalisée pae **ZAIDOURY NAJLAE**, Module Recherche Opérationnelle, Mai 2025  

---

## Ce que fait l'application

Tu choisis un algorithme, tu entres le nombre de nœuds (ou sources/destinations), et l'app :
1. Génère un graphe pondéré ou une matrice de coûts aléatoire
2. Exécute l'algorithme (implémentation from scratch ou via NetworkX selon le cas)
3. Affiche le résultat, graphiquement avec Matplotlib, ou sous forme de tableau de coûts
4. Met en évidence la solution (chemin en rouge, arêtes MST en pointillés rouges, chemin critique en rouge, arcs saturés, etc.)
5. Affiche une note de contexte Télécoms/Réseaux expliquant à quoi sert l'algorithme dans la réalité

---

## Algorithmes

### Algorithmes de graphes

| Algorithme | Ce qu'il calcule | Cas d'usage télécoms |
|---|---|---|
| **Dijkstra** | Plus court chemin dans un graphe non orienté pondéré, source → tous les nœuds | Routage IP entre routeurs |
| **Bellman-Ford** | Plus court chemin dans un graphe orienté pondéré, avec détection de cycles négatifs | Protocole RIP, topologies complexes |
| **Kruskal** | Arbre couvrant minimal — implémentation Union-Find from scratch | Câblage fibre optique (minimiser le coût d'installation) |
| **Welsh-Powell** | Coloration de graphe par degré décroissant, nombre de couleurs minimal | Allocation de fréquences entre antennes (éviter les interférences) |
| **Ford-Fulkerson** | Flot maximum dans un graphe orienté via chemins augmentants (BFS) | Optimisation de bande passante entre source et puits |
| **Potentiel Métra (CPM)** | Chemin critique dans un DAG (plus long chemin pondéré) | Ordonnancement de projets réseau avec dépendances entre tâches |

### Méthodes de transport

| Méthode | Ce qu'elle calcule | Cas d'usage télécoms |
|---|---|---|
| **Coin Nord-Ouest** | Solution initiale réalisable pour un problème de transport | Point de départ pour l'allocation de ressources entre sites |
| **Moindre Coût** | Solution initiale gloutonne, toujours allouer la cellule la moins chère en premier | Distribution de bande passante en minimisant les coûts de transmission |
| **Stepping Stone** | Optimise une solution de transport initiale en cherchant des cycles améliorants | Réduit le coût produit par Nord-Ouest, utilisé en pipeline |

> Stepping Stone est toujours exécuté à la suite de Nord-Ouest, l'app affiche les deux tableaux côte à côte (avant et après optimisation).

---

## Détails d'implémentation

- **Kruskal** est implémenté from scratch avec un Union-Find (compression de chemin + union par rang), pas la version NetworkX
- **Ford-Fulkerson** utilise une matrice d'adjacence et un BFS pour trouver les chemins augmentants ; affiche aussi les arcs saturés dans une fenêtre séparée
- **Potentiel Métra** génère des DAGs garantis — le générateur relance jusqu'à obtenir un graphe acyclique valide
- **Dijkstra et Bellman-Ford** utilisent `nx.single_source_dijkstra` / `nx.single_source_bellman_ford` de NetworkX sur des graphes générés aléatoirement
- **Welsh-Powell** est une implémentation manuelle — nœuds triés par degré décroissant, couleurs assignées sans conflit avec les voisins
- **Méthodes de transport** (Nord-Ouest, Moindre Coût, Stepping Stone) sont toutes implémentées from scratch sur des tableaux offres/demandes équilibrés aléatoirement, l'app auto-équilibre si `sum(sources) ≠ sum(destinations)`
- Chaque fenêtre d'algorithme inclut un bouton **Vérifier connexité** qui calcule et affiche le taux de connexité du graphe généré
- Le fond dégradé est rendu pixel par pixel avec PIL, aucun fichier image ni thème externe requis

---

## Structure du projet

```
NetOpt/
├── final_project_RO.py     # Tout : algorithmes, fenêtres, interface principale
├── Rapport_projet_ro.pdf   # Rapport complet du projet
└── README.md
```

Tous les algorithmes et interfaces sont dans un seul fichier, organisés en sections clairement séparées (une `interface_*()` + une `lancer_*()` par algorithme).

---

## Installation

**Prérequis :** Python 3.8+

```bash
pip install matplotlib networkx pillow
```

`tkinter` fait partie de la bibliothèque standard Python, pas besoin de l'installer.

---

## Lancement

```bash
python final_project_RO.py
```

La fenêtre principale propose trois options :
- **Algorithmes de Recherche Opérationnelle**, choisir et exécuter un algorithme
- **Entrer**, consulter la définition et l'application télécoms de chaque algorithme
- **Quitter**, fermer l'application

---

## Limites connues

- Pas d'import/export de topologies réseau réelles ou de matrices externes (CSV, JSON)
- Toutes les entrées sont générées aléatoirement, pas d'éditeur de graphe manuel
- Pas d'historique ni de persistance des sessions
- Code non modulaire (pas de fichier séparé par algorithme)

---

## Rapport

Rapport complet du projet (méthodologie, choix de conception, captures d'écran, conclusion) : [`Rapport_projet_ro.pdf`](./Rapport_projet_ro.pdf)

---

## Auteure

**ZAIDOURY Najlae**: Étudiante ingénieure, filière GRT, École Mohammadia d'Ingénieurs