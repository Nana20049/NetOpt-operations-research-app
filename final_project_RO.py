import tkinter as tk
from tkinter import messagebox
import random
import matplotlib.pyplot as plt
from matplotlib.table import Table
import copy
import networkx as nx
from PIL import Image, ImageTk
import string

def generate_subtle_gradient(start_color, end_color, width, height):
    image = Image.new("RGB", (width, height), "#000000")
    for y in range(height):
        ratio = y / height
        r = int(start_color[0] + (end_color[0] - start_color[0]) * ratio)
        g = int(start_color[1] + (end_color[1] - start_color[1]) * ratio)
        b = int(start_color[2] + (end_color[2] - start_color[2]) * ratio)
        for x in range(width):
            image.putpixel((x, y), (r, g, b))
    return image
#---------------------Entrer---------------------------------
def open_algos_description():
    description_win = tk.Toplevel()
    description_win.title("📖 Définitions et Applications")
    description_win.geometry("800x700")
    description_win.configure(bg="#0D1B2A")
    description_win.resizable(False, False)

    container = tk.Frame(description_win, bg="#0D1B2A")
    container.pack(fill="both", expand=True)

    canvas = tk.Canvas(container, width=800, height=700, highlightthickness=0, bg="#0D1B2A")
    scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)

    scrollable_frame = tk.Frame(canvas, bg="#0D1B2A")

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    def _on_mousewheel(event):
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
    scrollable_frame.bind_all("<MouseWheel>", _on_mousewheel)

    tk.Label(scrollable_frame, text="📖 Algorithmes & Réseaux",
             font=("Helvetica", 22, "bold"), fg="#E0E1DD", bg="#0D1B2A").pack(pady=20)

    algos_info = [
        {
            "nom": "🔹 Dijkstra",
            "definition": "Trouve le plus court chemin entre un nœud source et les autres dans un graphe pondéré.",
            "application": "Utilisé dans le routage IP pour déterminer le chemin optimal entre deux routeurs."
        },
        {
            "nom": "🔹 Kruskal",
            "definition": "Construit un arbre couvrant minimal à partir d’un graphe pondéré.",
            "application": "Permet d’optimiser les connexions dans les réseaux tout en réduisant le coût total."
        },
        {
            "nom": "🔹 Welsh-Powell",
            "definition": "Coloration de graphe minimisant le nombre de couleurs sans conflit entre voisins.",
            "application": "Répartition efficace des fréquences sans interférence dans les réseaux cellulaires."
        },
        {
            "nom": "🔹 Moindre Coût",
            "definition": "Méthode d’allocation initiale pour résoudre les problèmes de transport à coût minimal.",
            "application": "Répartit efficacement les ressources (comme la bande passante ou la capacité)."
        },
        {
            "nom": "🔹 Nord-Ouest",
            "definition": "Méthode de base pour créer une solution initiale d’un problème de transport.",
            "application": "Utile dans la gestion des ressources dans les réseaux logistiques ou télécoms."
        },
        {
            "nom": "🔹 Stepping Stone",
            "definition": "Méthode d’optimisation pour améliorer une solution initiale de transport.",
            "application": "Réduit les coûts de transmission dans les réseaux distribués."
        },
        {
            "nom": "🔹 Ford-Fulkerson",
            "definition": "Trouve le flux maximum dans un réseau orienté entre une source et un puits.",
            "application": "Optimise l’utilisation de la bande passante ou des flux de données."
        },
        {
            "nom": "🔹 Potentiel de Métra",
            "definition": "Méthode d’ordonnancement des tâches avec contraintes de précédence.",
            "application": "Gestion de projets réseaux avec délais et dépendances techniques."
        }
    ]
    for algo in algos_info:
        box = tk.Frame(scrollable_frame, bg="#133B5C", padx=15, pady=10, bd=1, relief="raised")
        tk.Label(box, text=algo["nom"], font=("Helvetica", 16, "bold"), fg="#E0E1DD", bg="#133B5C").pack(anchor="w", pady=(0, 5))
        tk.Label(box, text="📌 Définition :", font=("Helvetica", 12, "bold"), fg="#F0F0F0", bg="#133B5C").pack(anchor="w")
        tk.Label(box, text=algo["definition"], font=("Helvetica", 12), fg="#F0F0F0", bg="#133B5C",
                 wraplength=700, justify="left").pack(anchor="w", pady=(0, 5))
        tk.Label(box, text="🔧 Application :", font=("Helvetica", 12, "bold"), fg="#F0F0F0", bg="#133B5C").pack(anchor="w")
        tk.Label(box, text=algo["application"], font=("Helvetica", 12), fg="#F0F0F0", bg="#133B5C",
                 wraplength=700, justify="left").pack(anchor="w", pady=(0, 5))
        box.pack(fill="x", padx=40, pady=10)

    tk.Button(scrollable_frame, text="⬅️ Retour", font=("Helvetica", 14, "bold"),
              bg="white", fg="#00203E", padx=20, pady=10, width=20,
              command=description_win.destroy).pack(pady=30)
#---------------------Dijkstra--------------------------
def interface_dijkstra():
    fenetre = tk.Toplevel()
    fenetre.title("Dijkstra - Réseaux & Télécoms")
    fenetre.geometry("750x650")
    fenetre.configure(bg="#233c60")

    entry_nb_noeuds = tk.Entry(fenetre)
    entry_depart = tk.Entry(fenetre)
    entry_arrivee = tk.Entry(fenetre)

    def generer_noms_noeuds(n):
        noms = []
        lettres = string.ascii_uppercase
        i = 0
        while len(noms) < n:
            nom = ''
            temp = i
            while True:
                nom = lettres[temp % 26] + nom
                temp = temp // 26 - 1
                if temp < 0:
                    break
            noms.append(nom)
            i += 1
        return noms

    def generer_graphe_aleatoire(n):
        noms = generer_noms_noeuds(n)
        G = nx.Graph()
        G.add_nodes_from(noms)
        for i in range(n):
            for j in range(i + 1, n):
                if random.random() < 0.4:
                    poids = random.randint(1, 20)
                    G.add_edge(noms[i], noms[j], weight=poids)
        return G

    def taux_connexite(G):
        composants_connexes = list(nx.connected_components(G))
        nb_composants = len(composants_connexes)
        n = len(G.nodes)
        if n <= 1:
            return 100.0
        taux = (1 - (nb_composants - 1) / (n - 1)) * 100
        return taux
    def verifier_connexite():
        try:
            n = int(entry_nb_noeuds.get())
            G = generer_graphe_aleatoire(n)
            connexite = taux_connexite(G)
            message = f"Taux de connexité : {connexite:.2f}%\n\n"
            message += "✅ Le graphe est totalement connexe." if connexite == 100 else "⚠️ Le graphe n’est pas totalement connexe."
            messagebox.showinfo("Taux de connexité", message)
        except Exception as e:
            messagebox.showerror("Erreur", str(e))

    def lancer_dijkstra():
        try:
            n = int(entry_nb_noeuds.get())
            depart_lettre = entry_depart.get().strip().upper()
            arrivee_lettre = entry_arrivee.get().strip().upper()
            if len(depart_lettre) != 1 or len(arrivee_lettre) != 1:
                raise ValueError("Entrez une seule lettre pour les sommets.")
            depart = ord(depart_lettre) - 65
            arrivee = ord(arrivee_lettre) - 65
            if not (0 <= depart < n) or not (0 <= arrivee < n):
                raise ValueError("Les sommets doivent être entre A et " + chr(64 + n))

            G = nx.Graph()
            G.add_nodes_from(range(n))
            for i in range(n):
                for j in range(i + 1, n):
                    if random.random() < 0.6:
                        poids = random.randint(1, 20)
                        G.add_edge(i, j, weight=poids)

            if not nx.has_path(G, depart, arrivee):
                raise ValueError("Il n'existe aucun chemin entre les deux sommets.")

            chemins = nx.single_source_dijkstra_path(G, depart)
            couts = nx.single_source_dijkstra_path_length(G, depart)

            texte = f"📌 Plus courts chemins depuis {chr(65 + depart)} :\n\n"
            for dest in sorted(chemins):
                if dest != depart:
                    chemin = chemins[dest]
                    cout = couts[dest]
                    texte += f"{chr(65 + depart)} → {chr(65 + dest)} : { ' → '.join(chr(65 + i) for i in chemin) } (coût = {cout})\n"

            chemin_cible = chemins[arrivee]
            cout_cible = couts[arrivee]
            texte += f"\n🎯 Chemin entre {chr(65 + depart)} et {chr(65 + arrivee)} : {' → '.join(chr(65 + i) for i in chemin_cible)} (coût = {cout_cible})"

            pos = nx.spring_layout(G)
            labels = {i: chr(65 + i) for i in G.nodes}
            edge_labels = nx.get_edge_attributes(G, 'weight')

            plt.figure(figsize=(8, 6))
            nx.draw(G, pos, with_labels=True, labels=labels, node_color='skyblue', node_size=800, font_weight='bold')
            nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
            edges_chemin = list(zip(chemin_cible, chemin_cible[1:]))
            nx.draw_networkx_edges(G, pos, edgelist=edges_chemin, edge_color='red', width=3)
            plt.title("Graphe - Chemin de Dijkstra")
            plt.tight_layout()
            plt.show()

            messagebox.showinfo("Résultats de Dijkstra", texte)

        except Exception as e:
            messagebox.showerror("Erreur", str(e))

    tk.Label(fenetre, text="🔀 Algorithme de Dijkstra", font=("Helvetica", 20, "bold"), fg="white", bg="#233c60").pack(pady=20)
    tk.Label(fenetre, text="Nombre de nœuds :", fg="white", bg="#233c60", font=("Arial", 12)).pack()
    entry_nb_noeuds.pack(pady=5)
    tk.Label(fenetre, text="Point de départ :", fg="white", bg="#233c60", font=("Arial", 12)).pack()
    entry_depart.pack(pady=5)
    tk.Label(fenetre, text="Point d'arrivée :", fg="white", bg="#233c60", font=("Arial", 12)).pack()
    entry_arrivee.pack(pady=5)
    tk.Button(fenetre, text="Générer graphe & Dijkstra", command=lancer_dijkstra, bg="#ADEFD1", fg="black", font=("Arial", 12, "bold")).pack(pady=10)
    tk.Button(fenetre, text="Vérifier connexité", command=verifier_connexite, bg="#89B9E6", fg="black", font=("Arial", 12, "bold")).pack(pady=10)
    tk.Button(fenetre, text="❌ Quitter",font=("Arial", 12, "bold"), command=fenetre.destroy, bg="#657FEA", fg="white").pack(pady=10)

    footer = tk.Label(
        fenetre,
        text="📡 Dijkstra optimise le routage en réseau.\nTrouve le chemin le plus court pour une meilleure transmission des données.",
        fg="white",
        bg="#233c60",
        font=("Arial", 11),
        justify="center"
    )
    footer.pack(side="bottom", pady=30)

#---------------------Kruskal------------------------------
edges_globale = []
nodes_globale = []

def kruskal(graph_edges, nodes):
    parent = {}
    rank = {}

    def find(node):
        if parent[node] != node:
            parent[node] = find(parent[node])
        return parent[node]

    def union(node1, node2):
        root1 = find(node1)
        root2 = find(node2)
        if root1 != root2:
            if rank[root1] > rank[root2]:
                parent[root2] = root1
            else:
                parent[root1] = root2
                if rank[root1] == rank[root2]:
                    rank[root2] += 1

    for node in nodes:
        parent[node] = node
        rank[node] = 0

    mst = []
    graph_edges = sorted(graph_edges, key=lambda x: x[2])

    for u, v, weight in graph_edges:
        if find(u) != find(v):
            union(u, v)
            mst.append((u, v, weight))

    return mst

def interface_kruskal_auto(n):
    global edges_globale, nodes_globale

    nodes = [chr(65 + i) for i in range(n)]
    edges = []

    for i in range(n):
        for j in range(i + 1, n):
            if random.random() < 0.6:
                poids = random.randint(1, 20)
                edges.append((nodes[i], nodes[j], poids))


    if not edges:
        messagebox.showerror("Erreur", "Aucune arête générée. Réessayez.")
        return

    edges_globale = edges.copy()
    nodes_globale = nodes.copy()

    mst = kruskal(edges, nodes)
    total = sum(w for _, _, w in mst)
    result_text = "\n".join([f"{u} - {v} : {w}" for u, v, w in mst])
    messagebox.showinfo("Résultat", f"Arbre couvrant minimal :\n{result_text}\n\nCoût total : {total}")

    G = nx.Graph()
    G.add_nodes_from(nodes)
    G.add_weighted_edges_from(edges)

    pos = nx.spring_layout(G, seed=42)
    edge_labels = nx.get_edge_attributes(G, 'weight')
    mst_edges = [(u, v) for u, v, _ in mst]
    other_edges = [e for e in G.edges() if e not in mst_edges and (e[1], e[0]) not in mst_edges]

    plt.figure(figsize=(9, 7))
    nx.draw_networkx_edges(G, pos, edgelist=other_edges, edge_color='lightgray', width=1)
    nx.draw_networkx_edges(G, pos, edgelist=mst_edges, edge_color='red', style='dashed', width=2)
    nx.draw_networkx_nodes(G, pos, node_color="#ADEFD1", node_size=800)
    nx.draw_networkx_labels(G, pos, font_weight='bold')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    plt.title("Algorithme de Kruskal : Arbre couvrant minimal", fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.show()

def verifier_connexite_kruskal():
    if not edges_globale or not nodes_globale:
        messagebox.showerror("Erreur", "Aucun graphe généré.")
        return

    G = nx.Graph()
    G.add_nodes_from(nodes_globale)
    G.add_weighted_edges_from(edges_globale)

    est_connexe = nx.is_connected(G)
    nb_composantes = nx.number_connected_components(G)

    tailles = [len(c) for c in nx.connected_components(G)]
    plus_grande = max(tailles)
    taux_connexite = (plus_grande / len(nodes_globale)) * 100

    msg = f"📊 Taux de connexité (taille de la plus grande composante) : {taux_connexite:.2f} %\n"
    msg += f"🔗 Nombre de composantes connexes : {nb_composantes}\n"
    msg += "✅ Le graphe est totalement connexe." if est_connexe else "❌ Le graphe n’est pas totalement connexe."

    messagebox.showinfo("Taux de Connexité", msg)

def page_accueil():
    def lancer():
        try:
            n = int(entry_nb_nodes.get())
            if n < 2:
                raise ValueError
        except:
            messagebox.showerror("Erreur", "Veuillez entrer un nombre de nœuds valide (>= 2).")
            return
        interface_kruskal_auto(n)

    global root
    root = tk.Tk()
    root.title("🌐 Kruskal Télécoms")
    root.geometry("600x500")
    root.configure(bg="#233c60")

    tk.Label(root, text="🌐 Algorithme de Kruskal", bg="#233c60", fg="white",
             font=("Arial", 18, "bold")).pack(pady=10)

    tk.Label(root, text="Nombre de nœuds :", bg="#233c60", fg="white", font=("Arial", 12)).pack(pady=5)
    entry_nb_nodes = tk.Entry(root, font=("Arial", 12))
    entry_nb_nodes.pack(pady=5)

    tk.Button(root, text="Lancer l’algorithme", font=("Arial", 12, "bold"),
              bg="#ADEFD1", fg="#192c46", command=lancer).pack(pady=15)

    tk.Button(root, text="🔗 Vérifier la connexité", font=("Arial", 12, "bold"),
              bg="#ADEFD1", fg="#192c46", command=verifier_connexite_kruskal).pack(pady=5)

    tk.Button(root, text="❌ Quitter", font=("Arial", 12, "bold"),
              bg="#657FEA", fg="white", command=root.destroy).pack(pady=10)

    message_info = (
        "📡 Dans le contexte des réseaux de télécommunications, l’algorithme de Kruskal permet "
        "de minimiser le coût d’installation de la fibre optique tout en garantissant "
        "la connexion entre les sites."
    )

    tk.Label(root, text=message_info, wraplength=550, justify="center", fg="white", bg="#233c60",
             font=("Arial", 10)).pack(pady=20)

    root.mainloop()
#---------------------Welshpowel-----------------------------
def interface_welsh_powell():
    fenetre = tk.Toplevel()
    fenetre.title("Welsh-Powell - Coloration de Graphe")
    fenetre.geometry("750x650")
    fenetre.configure(bg="#233c60")

    entry_nb_noeuds = tk.Entry(fenetre)

    def generer_noms_noeuds(n):
        noms = []
        lettres = string.ascii_uppercase
        i = 0
        while len(noms) < n:
            nom = ''
            temp = i
            while True:
                nom = lettres[temp % 26] + nom
                temp = temp // 26 - 1
                if temp < 0:
                    break
            noms.append(nom)
            i += 1
        return noms

    def generer_graphe_aleatoire(n):
        noms = generer_noms_noeuds(n)
        G = nx.Graph()
        G.add_nodes_from(noms)
        for i in range(n):
            for j in range(i + 1, n):
                if random.random() < 0.4:
                    G.add_edge(noms[i], noms[j])
        return G

    def taux_connexite(G):
        n = G.number_of_nodes()
        if n == 0:
            return 0.0
        if nx.is_connected(G):
            return 100.0
        composantes = list(nx.connected_components(G))
        plus_grande = max(len(c) for c in composantes)
        return (plus_grande / n) * 100


    def verifier_connexite():
        try:
            n = int(entry_nb_noeuds.get())
            G = generer_graphe_aleatoire(n)
            densite = taux_connexite(G)
            est_connexe = nx.is_connected(G)

            message = f"Taux de connexité (densité) : {densite:.2f}%\n"
            message += "✅ Le graphe est connexe." if est_connexe else "❌ Le graphe n'est pas connexe."
            messagebox.showinfo("Analyse du graphe", message)

        except Exception as e:
            messagebox.showerror("Erreur", str(e))

    def lancer_welsh_powell():
        try:
            n = int(entry_nb_noeuds.get())
            G = generer_graphe_aleatoire(n)
            sommets_tries = sorted(G.degree, key=lambda x: x[1], reverse=True)
            couleurs = {}
            couleur_actuelle = 0

            for sommet, _ in sommets_tries:
                if sommet not in couleurs:
                    couleurs[sommet] = couleur_actuelle
                    for autre, _ in sommets_tries:
                        if autre not in couleurs:
                            if all(couleurs.get(voisin) != couleur_actuelle for voisin in G.neighbors(autre)):
                                couleurs[autre] = couleur_actuelle
                    couleur_actuelle += 1

            nb_couleurs = max(couleurs.values()) + 1
            messagebox.showinfo("Résultat", f"Nombre de couleurs utilisées : {nb_couleurs}")

            couleurs_nodes = [couleurs[node] for node in G.nodes()]
            pos = nx.spring_layout(G)
            nx.draw(G, pos, with_labels=True, node_color=couleurs_nodes, cmap=plt.cm.Set3, node_size=800, font_weight='bold')
            plt.title("Welsh-Powell- (Coloration de Graphe)")
            plt.show()

        except Exception as e:
            messagebox.showerror("Erreur", str(e))

    tk.Label(fenetre, text="🎨 Welsh-Powell - Coloration de Graphe", font=("Helvetica", 20, "bold"), fg="white", bg="#233c60").pack(pady=20)
    tk.Label(fenetre, text="Nombre de nœuds :", fg="white", bg="#233c60", font=("Arial", 12)).pack()
    entry_nb_noeuds.pack(pady=5)
    tk.Button(fenetre, text="Générer & Colorier", command=lancer_welsh_powell, bg="#ADBFEF", fg="black", font=("Arial", 12, "bold")).pack(pady=10)
    tk.Button(fenetre, text="Vérifier connexité", command=verifier_connexite, bg="#89B9E6", fg="black", font=("Arial", 12, "bold")).pack(pady=10)
    tk.Button(fenetre, text="❌ Quitter",font=("Arial", 12, "bold"), command=fenetre.destroy, bg="#657FEA", fg="white").pack(pady=10)

    footer = tk.Label(
        fenetre,
        text="💡 En télécom, Welsh-Powell aide à éviter les interférences en minimisant les conflits entre fréquences.",
        fg="white",
        bg="#233c60",
        font=("Helvetica", 11),
        justify="center"
    )
    footer.pack(side="bottom", pady=30)

#--------------------FordFulkerson---------------------
dernier_graphe = None
def indice_vers_lettre(i):
    return chr(65 + i)

def ford_fulkerson(graph, source, sink):
    parent = [-1] * len(graph)

    def bfs():
        visited = [False] * len(graph)
        queue = [source]
        visited[source] = True
        while queue:
            u = queue.pop(0)
            for v, capacity in enumerate(graph[u]):
                if not visited[v] and capacity > 0:
                    queue.append(v)
                    visited[v] = True
                    parent[v] = u
                    if v == sink:
                        return True
        return False

    max_flow = 0
    while bfs():
        path_flow = float('inf')
        s = sink
        while s != source:
            path_flow = min(path_flow, graph[parent[s]][s])
            s = parent[s]
        max_flow += path_flow
        v = sink
        while v != source:
            u = parent[v]
            graph[u][v] -= path_flow
            graph[v][u] += path_flow
            v = parent[v]
    return max_flow

def generer_graphe_aleatoire(n):
    graph = [[0]*n for _ in range(n)]
    for i in range(n-1):
        graph[i][i+1] = random.randint(5, 20)
    nb_arcs = random.randint(n, n*(n-1)//2)
    for _ in range(nb_arcs):
        u = random.randint(0, n-2)
        v = random.randint(u+1, n-1)
        if graph[u][v] == 0:
            graph[u][v] = random.randint(1, 20)
    return graph

def est_connexe(graph):
    visited = [False] * len(graph)
    def dfs(u):
        visited[u] = True
        for v, cap in enumerate(graph[u]):
            if cap > 0 and not visited[v]:
                dfs(v)
    dfs(0)
    return all(visited)

def dessiner_graphe(graph, title, flow_graph=None):
    G = nx.DiGraph()
    n = len(graph)
    for i in range(n):
        for j in range(n):
            if graph[i][j] > 0:
                if flow_graph:
                    label = f"{flow_graph[i][j]}/{graph[i][j]}"
                else:
                    label = f"{graph[i][j]}"
                G.add_edge(indice_vers_lettre(i), indice_vers_lettre(j), capacity=graph[i][j], label=label)

    pos = nx.spring_layout(G)
    plt.figure(figsize=(8,6))
    nx.draw_networkx_nodes(G, pos, node_color='lightblue', node_size=700)
    nx.draw_networkx_labels(G, pos)
    nx.draw_networkx_edges(G, pos, arrowstyle='-|>', arrowsize=20)
    edge_labels = nx.get_edge_attributes(G, 'label')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red')
    plt.title(title)
    plt.axis('off')
    plt.show()

def lancer_ford_fulkerson():
    global dernier_graphe
    try:
        n = int(entry_nodes.get())
        if n < 2:
            raise ValueError("Le nombre de nœuds doit être au moins 2.")

        graph = generer_graphe_aleatoire(n)
        dernier_graphe = graph  
        graph_initial = [row[:] for row in graph]

        max_flow = ford_fulkerson(graph, 0, n-1)

        flow_graph = [[0]*n for _ in range(n)]
        for u in range(n):
            for v in range(n):
                if graph_initial[u][v] > 0:
                    flow_graph[u][v] = graph_initial[u][v] - graph[u][v]

        dessiner_graphe(graph_initial, "Graphe initial (capacités)")
        dessiner_graphe(graph_initial, f"Graphe avec flots max = {max_flow}", flow_graph=flow_graph)

        saturés = []
        for u in range(n):
            for v in range(n):
                if graph_initial[u][v] > 0 and flow_graph[u][v] == graph_initial[u][v]:
                    saturés.append(f"Arc {indice_vers_lettre(u)} → {indice_vers_lettre(v)} : flot = capacité = {graph_initial[u][v]}")

        if saturés:
            fen = tk.Toplevel()
            fen.title("Arcs saturés")
            fen.configure(bg="#00203E")
            tk.Label(fen, text="Arcs saturés (flot = capacité max)", font=("Helvetica", 14, "bold"),
                     fg="white", bg="#00203E").pack(pady=10)
            text = tk.Text(fen, width=50, height=10, font=("Helvetica", 12))
            text.pack(padx=10, pady=10)
            for arc in saturés:
                text.insert(tk.END, arc + "\n")
            text.config(state=tk.DISABLED)
            tk.Button(fen, text="Fermer", command=fen.destroy,
                      font=("Helvetica", 12, "bold"), bg="white", fg="#00203E").pack(pady=10)
        else:
            messagebox.showinfo("Info", "Aucun arc saturé trouvé.")
    except Exception as e:
        messagebox.showerror("Erreur", str(e))

def verifier_connexite():
    global dernier_graphe
    try:
        if dernier_graphe is None:
            raise ValueError("Veuillez d’abord générer un graphe avec le bouton 'Calculer flot max'.")

        n = len(dernier_graphe)
        G = nx.Graph()  
        for u in range(n):
            for v in range(n):
                if dernier_graphe[u][v] > 0 or dernier_graphe[v][u] > 0:
                    G.add_edge(u, v)

        composants_connexes = list(nx.connected_components(G))
        nb_composants = len(composants_connexes)

        if n <= 1:
            taux = 100.0
        else:
            taux = (1 - (nb_composants - 1) / (n - 1)) * 100

        message = f"Taux de connexité : {taux:.2f}%\n\n"
        message += "✅ Le graphe est totalement connexe." if taux == 100 else "⚠️ Le graphe n’est pas totalement connexe."
        messagebox.showinfo("Taux de connexité", message)

    except Exception as e:
        messagebox.showerror("Erreur", str(e))

def interface_ford_fulkerson():
    global entry_nodes
    root = tk.Tk()
    root.title("🔗 Ford-Fulkerson (Flot Max)")
    root.geometry("600x450")
    root.configure(bg="#233c60")

    tk.Label(root, text="🔗 Algorithme Ford-Fulkerson", font=("Helvetica", 18, "bold"),
             fg="white", bg="#233c60").pack(pady=15)

    tk.Label(root, text="Nombre de nœuds (≥ 2) :", font=("Helvetica", 12),
             fg="white", bg="#233c60").pack()
    entry_nodes = tk.Entry(root, font=("Helvetica", 12), width=10)
    entry_nodes.pack(pady=8)

    tk.Button(root, text="Calculer flot max 🧠", font=("Helvetica", 12, "bold"),
              bg="white", fg="#233c60", command=lancer_ford_fulkerson).pack(pady=10)

    tk.Button(root, text="Vérifier connexité 🔍", font=("Helvetica", 12, "bold"),
              bg="white", fg="#233c60", command=verifier_connexite).pack(pady=5)

    tk.Button(root, text="❌ Quitter", font=("Arial", 12, "bold"),
              bg="#657FEA", fg="white", command=root.destroy).pack(pady=10)

    tk.Label(root,
             text="💡 En télécom, Ford-Fulkerson permet d’optimiser\n"
                  "le flux de données entre source et destination sur un réseau.",
             font=("Helvetica", 10), fg="white", bg="#233c60", justify="center").pack(pady=30)

    root.mainloop()

#---------------------BellmanFord-------------------------------
dernier_graphe_bellman = None

def indice_vers_lettre(i):
    return chr(65 + i)

def lettre_vers_indice(l):
    l = l.upper()
    if len(l) == 1 and 'A' <= l <= 'Z':
        return ord(l) - 65
    else:
        raise ValueError("Entrée invalide : utilisez une lettre de A à Z.")

def bellman_ford(G, source):
    try:
        dist, paths = nx.single_source_bellman_ford(G, source, weight='weight')
        return dist, paths
    except nx.NetworkXUnbounded:
        raise ValueError("⚠️ Cycle de poids négatif détecté.")

def afficher_graphe(G, source, target=None, path_nodes=None):
    plt.figure(figsize=(8, 6))
    pos = nx.spring_layout(G)
    labels = nx.get_edge_attributes(G, 'weight')
    node_labels = {i: indice_vers_lettre(i) for i in G.nodes}
    node_colors = ['lightgreen' if i == source else 'salmon' if i == target else 'lightblue' for i in G.nodes]

    nx.draw(G, pos, with_labels=True, labels=node_labels,
            node_color=node_colors, node_size=800, arrows=True)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)

    if path_nodes:
        path_edges = list(zip(path_nodes[:-1], path_nodes[1:]))
        nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='red', width=3)

    plt.title("Graphe Bellman-Ford")
    plt.axis('off')
    plt.show()

def lancer_bellman():
    global dernier_graphe_bellman
    try:
        n = int(entry_nb_nodes.get())
        source_lettre = entry_source.get().strip()
        target_lettre = entry_target.get().strip()

        if n < 2:
            raise ValueError("Veuillez entrer au moins 2 sommets.")

        source = lettre_vers_indice(source_lettre)
        target = lettre_vers_indice(target_lettre)

        if not (0 <= source < n) or not (0 <= target < n):
            raise ValueError(f"Les lettres doivent être dans la plage de A à {chr(65 + n - 1)}.")

        G = nx.DiGraph()
        G.add_nodes_from(range(n))
        for i in range(n):
            for j in range(n):
                if i != j and random.random() < 0.4:
                    poids = random.randint(1, 15)
                    G.add_edge(i, j, weight=poids)

        dernier_graphe_bellman = G

        dist, paths = bellman_ford(G, source)
        chemin = paths.get(target, [])
        afficher_graphe(G, source, target, path_nodes=chemin)

        distances_text = ""
        for k in dist:
            if k == source:
                continue
            chemin_k = paths.get(k, [])
            if chemin_k:
                chemin_lettres = " → ".join(indice_vers_lettre(i) for i in chemin_k)
                distances_text += f"{indice_vers_lettre(source)} → {indice_vers_lettre(k)} : {dist[k]}   (chemin : {chemin_lettres})\n"
            else:
                distances_text += f"{indice_vers_lettre(source)} → {indice_vers_lettre(k)} : ❌ Inaccessible\n"

        chemin_final_lettres = " → ".join(indice_vers_lettre(i) for i in chemin)
        messagebox.showinfo("Distances et Chemin",
            f"Distances depuis {indice_vers_lettre(source)} :\n\n{distances_text}\n\n"
            f"🛣️ Chemin vers {indice_vers_lettre(target)} : {chemin_final_lettres if chemin else '—'}")

    except Exception as e:
        messagebox.showerror("Erreur", str(e))

def verifier_connexite_bellman():
    global dernier_graphe_bellman
    try:
        if dernier_graphe_bellman is None:
            raise ValueError("Veuillez d’abord générer un graphe avec le bouton 'Lancer l’algorithme'.")

        n = len(dernier_graphe_bellman)
        visited = [False] * n

        def dfs(u):
            visited[u] = True
            for v in dernier_graphe_bellman.successors(u):
                if not visited[v]:
                    dfs(v)

        dfs(0)
        nb_atteints = sum(visited)
        pourcentage = (nb_atteints / n) * 100

        if nb_atteints == n:
            messagebox.showinfo("Connexité", f"✅ Le graphe est connexe.\nTous les {n} sommets sont accessibles.")
        else:
            messagebox.showwarning("Connexité",
                f"❌ Le graphe n’est pas connexe.\n"
                f"{nb_atteints} sommets atteints sur {n} ({pourcentage:.2f} %)")

    except Exception as e:
        messagebox.showerror("Erreur", str(e))

def interface_bellman_ford():
    global entry_nb_nodes, entry_source, entry_target

    root = tk.Tk()
    root.title("📡 Algorithme de Bellman-Ford")
    root.geometry("640x520")
    root.configure(bg="#233c60")

    tk.Label(root, text="📡 Algorithme de Bellman-Ford", font=("Helvetica", 18, "bold"),
             fg="white", bg="#233c60").pack(pady=15)

    tk.Label(root, text="Nombre de sommets (≥ 2) :", font=("Helvetica", 12),
             fg="white", bg="#233c60").pack()
    entry_nb_nodes = tk.Entry(root, font=("Helvetica", 12), width=10)
    entry_nb_nodes.pack(pady=5)

    tk.Label(root, text="Sommet de départ :", font=("Helvetica", 12),
             fg="white", bg="#233c60").pack()
    entry_source = tk.Entry(root, font=("Helvetica", 12), width=10)
    entry_source.pack(pady=5)

    tk.Label(root, text="Sommet d’arrivée :", font=("Helvetica", 12),
             fg="white", bg="#233c60").pack()
    entry_target = tk.Entry(root, font=("Helvetica", 12), width=10)
    entry_target.pack(pady=5)

    tk.Button(root, text="Lancer l’algorithme 🧠", font=("Helvetica", 12, "bold"),
              bg="white", fg="#233c60", command=lancer_bellman).pack(pady=15)

    tk.Button(root, text="Vérifier connexité 🔍", font=("Helvetica", 12, "bold"),
              bg="white", fg="#233c60", command=verifier_connexite_bellman).pack(pady=5)

    tk.Button(root, text="❌ Quitter", font=("Helvetica", 12, "bold"),
              bg="#657FEA", fg="white", command=root.destroy).pack(pady=15)

    tk.Label(root,
             text="💡 En réseaux & télécoms, Bellman-Ford est utilisé dans les protocoles de routage (ex: protocole RIP)\n"
                  "pour trouver les chemins les plus courts même avec des poids variables.",
             font=("Helvetica", 10), fg="white", bg="#233c60", justify="center").pack(pady=20)

    root.mainloop()

#---------------------potentielMetra------------------------
def metra_algo(G):
    if not nx.is_directed_acyclic_graph(G):
        raise ValueError("Le graphe doit être orienté acyclique.")
    duree = nx.dag_longest_path_length(G, weight='weight')
    chemin = nx.dag_longest_path(G, weight='weight')
    return duree, chemin

def generer_dag(n):
    while True:
        G = nx.DiGraph()
        G.add_nodes_from(range(n))

        for i in range(n):
            for j in range(i + 1, n):
                if random.random() < 0.4:
                    poids = random.randint(1, 10)
                    G.add_edge(i, j, weight=poids)

        for i in range(n):
            if G.out_degree(i) == 0 and i < n - 1:
                j = random.randint(i + 1, n - 1)
                poids = random.randint(1, 10)
                G.add_edge(i, j, weight=poids)
            elif G.in_degree(i) == 0 and i > 0:
                j = random.randint(0, i - 1)
                poids = random.randint(1, 10)
                G.add_edge(j, i, weight=poids)

        if nx.is_directed_acyclic_graph(G):
            return G

def verifier_connexite_orientee(G, noms):
    if not nx.is_directed(G):
        messagebox.showwarning("Attention", "Le graphe doit être orienté.")
        return

    n = len(G.nodes())
    reachable_pairs = set()

    for u in G.nodes():
        for v in nx.descendants(G, u):
            reachable_pairs.add((u, v))

    taux = (len(reachable_pairs) / (n * (n - 1))) * 100 if n > 1 else 0

    connexe = taux == 100.0
    etat = "✅ Graphe connexe" if connexe else "❌ Graphe non connexe"

    messagebox.showinfo("Taux de connexité",
                        f"Taux de connexité (accessibilité unique) : {taux:.2f}%\n{etat}")

def lancer_metra():
    global G_global, noms
    try:
        n = int(entry_nodes.get())
        if n < 2:
            raise ValueError("Veuillez entrer un nombre ≥ 2.")

        G = generer_dag(n)
        G_global = G
        noms = {i: chr(65 + i) for i in range(n)}

        duree, chemin = metra_algo(G)

        try:
            pos = nx.nx_pydot.graphviz_layout(G, prog='dot')
        except:
            pos = nx.spring_layout(G, seed=42)

        labels = nx.get_edge_attributes(G, 'weight')

        plt.figure(figsize=(8, 6))
        nx.draw(G, pos, labels=noms, with_labels=True, node_color='skyblue',
                node_size=1000, font_weight='bold', arrows=True, font_size=12)
        nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)

        edges_critique = list(zip(chemin, chemin[1:]))
        nx.draw_networkx_edges(G, pos, edgelist=edges_critique,
                               edge_color='red', width=3)

        plt.title(f"Chemin critique 🔴\nDurée minimale : {duree}", fontsize=14)
        plt.show()

        nom_chemin = [noms[i] for i in chemin]
        messagebox.showinfo("Résultat",
                            f"Chemin critique : {' ➜ '.join(nom_chemin)}\nDurée minimale : {duree}")

    except Exception as e:
        messagebox.showerror("Erreur", str(e))

def interface_potentiel_metra():
    global entry_nodes
    root = tk.Tk()
    root.title("📊 Potentiel de Métra (CPM)")
    root.geometry("600x500")
    root.configure(bg="#233c60")

    tk.Label(root, text="📊 Potentiel de Métra (CPM)", font=("Helvetica", 18, "bold"),
             fg="white", bg="#233c60").pack(pady=10)

    tk.Label(root, text="Nombre de tâches (nœuds ≥ 2) :", font=("Helvetica", 12),
             fg="white", bg="#233c60").pack()

    entry_nodes = tk.Entry(root, font=("Helvetica", 12), width=10)
    entry_nodes.pack(pady=10)

    tk.Button(root, text="Lancer l’algorithme 🧠", font=("Helvetica", 12, "bold"),
              bg="white", fg="#233c60", command=lancer_metra).pack(pady=10)

    tk.Button(root, text="🔍 Vérifier connexité", font=("Helvetica", 12, "bold"),
              bg="white", fg="#233c60",
              command=lambda: verifier_connexite_orientee(G_global, noms)).pack(pady=5)

    tk.Button(root, text="❌ Quitter", font=("Arial", 12, "bold"),
              bg="#657FEA", fg="white", command=root.destroy).pack(pady=10)

    tk.Label(root, text="💡 En réseaux & télécoms, le potentiel de Métra permet de planifier les tâches critiques\n"
                    "comme l’installation de fibre, les interventions ou les mises en service,\n"
                    "en identifiant le chemin le plus long (durée minimale totale).",
             font=("Helvetica", 10), fg="white", bg="#233c60", justify="center").pack(pady=30)

    root.mainloop()

#---------------------moindrecout---------------------
def moindre_cout(sources, destinations, couts):
    m = len(sources)
    n = len(destinations)
    solution = [[0]*n for _ in range(m)]

    offres = sources.copy()
    demandes = destinations.copy()

    while True:
        min_cost = float('inf')
        min_pos = None
        for i in range(m):
            for j in range(n):
                if offres[i] > 0 and demandes[j] > 0 and couts[i][j] < min_cost:
                    min_cost = couts[i][j]
                    min_pos = (i, j)

        if min_pos is None:
            break

        i, j = min_pos
        q = min(offres[i], demandes[j])
        solution[i][j] = q
        offres[i] -= q
        demandes[j] -= q

    return solution

def lancer_moindre_cout():
    try:
        m = int(entry_sources.get())
        n = int(entry_destinations.get())
        if m < 1 or n < 1:
            raise ValueError("Les valeurs doivent être ≥ 1.")

        sources = [random.randint(30, 100) for _ in range(m)]
        destinations = [random.randint(30, 100) for _ in range(n)]

        total_sources = sum(sources)
        total_destinations = sum(destinations)

        if total_sources > total_destinations:
            destinations.append(total_sources - total_destinations)
            n += 1
        elif total_destinations > total_sources:
            sources.append(total_destinations - total_sources)
            m += 1

        couts = [[random.randint(1, 20) for _ in range(n)] for _ in range(m)]
        solution = moindre_cout(sources, destinations, couts)

        total = sum(solution[i][j] * couts[i][j] for i in range(m) for j in range(n))

        fig, ax = plt.subplots()
        ax.set_axis_off()
        tableau = Table(ax, bbox=[0, 0, 1, 1])
        hauteur, largeur = len(couts), len(couts[0])

        cell_w, cell_h = 1.0 / (largeur+2), 1.0 / (hauteur+2)

        tableau.add_cell(0, 0, cell_w, cell_h, text="S/D", loc='center', facecolor="#40466e")
        for j in range(largeur):
            tableau.add_cell(0, j+1, cell_w, cell_h, text=f"D{j+1}", loc='center', facecolor="#40466e")
        for i in range(hauteur):
            tableau.add_cell(i+1, 0, cell_w, cell_h, text=f"S{i+1}", loc='center', facecolor="#40466e")

        for i in range(hauteur):
            for j in range(largeur):
                if solution[i][j] > 0:
                    val = f"{couts[i][j]}\n({solution[i][j]})"
                else:
                    val = f"{couts[i][j]}"
                tableau.add_cell(i+1, j+1, cell_w, cell_h, text=val, loc='center')

        for j in range(largeur):
            tableau.add_cell(hauteur+1, j+1, cell_w, cell_h,
                             text=f"D={destinations[j]}", loc='center', facecolor="#d1d1d1")
        for i in range(hauteur):
            tableau.add_cell(i+1, largeur+1, cell_w, cell_h,
                             text=f"S={sources[i]}", loc='center', facecolor="#d1d1d1")

        ax.add_table(tableau)
        plt.title(f"🚚 Méthode du Moindre Coût — Coût total : {total}", fontsize=12)
        plt.show()

    except Exception as e:
        messagebox.showerror("Erreur", str(e))

def interface_moindre_cout():
    global entry_sources, entry_destinations
    root = tk.Tk()
    root.title("🚚 Méthode du Moindre Coût")
    root.geometry("600x500")
    root.configure(bg="#233c60")

    tk.Label(root, text="🚚 Méthode du Moindre Coût", font=("Helvetica", 18, "bold"),
             fg="white", bg="#233c60").pack(pady=10)

    tk.Label(root, text="Nombre de sources :", font=("Helvetica", 12),
             fg="white", bg="#233c60").pack()
    entry_sources = tk.Entry(root, font=("Helvetica", 12), width=10)
    entry_sources.pack(pady=5)

    tk.Label(root, text="Nombre de destinations :", font=("Helvetica", 12),
             fg="white", bg="#233c60").pack()
    entry_destinations = tk.Entry(root, font=("Helvetica", 12), width=10)
    entry_destinations.pack(pady=5)

    tk.Button(root, text="Lancer l’algorithme 🧠", font=("Helvetica", 12, "bold"),
              bg="white", fg="#233c60", command=lancer_moindre_cout).pack(pady=20)
    tk.Button(root, text="❌ Quitter", font=("Arial", 12, "bold"),
                   bg="#657FEA", fg="white", command=root.destroy).pack(pady=10)
    tk.Label(root,
             text="💡 En télécom, cet algorithme permet d’allouer des ressources comme la bande passante\n"
                  "entre des sites tout en minimisant les coûts de transmission.",
             font=("Helvetica", 10), fg="white", bg="#233c60", justify="center").pack(pady=30)

    root.mainloop()
#---------------------nordsouest----------------------------
def nord_ouest(sources, destinations):
    m = len(sources)
    n = len(destinations)
    solution = [[0] * n for _ in range(m)]
    i = j = 0
    sources = sources.copy()
    destinations = destinations.copy()

    while i < m and j < n:
        q = min(sources[i], destinations[j])
        solution[i][j] = q
        sources[i] -= q
        destinations[j] -= q
        if sources[i] == 0:
            i += 1
        if destinations[j] == 0:
            j += 1

    return solution

def lancer_nord_ouest():
    try:
        m = int(entry_sources.get())
        n = int(entry_destinations.get())
        if m < 1 or n < 1:
            raise ValueError("Les valeurs doivent être ≥ 1.")

        sources = [random.randint(30, 100) for _ in range(m)]
        destinations = [random.randint(30, 100) for _ in range(n)]

        total_sources = sum(sources)
        total_destinations = sum(destinations)

        if total_sources > total_destinations:
            destinations.append(total_sources - total_destinations)
            n += 1
        elif total_destinations > total_sources:
            sources.append(total_destinations - total_sources)
            m += 1

        couts = [[random.randint(1, 20) for _ in range(n)] for _ in range(m)]

        solution = nord_ouest(sources, destinations)

        total = sum(solution[i][j] * couts[i][j] for i in range(m) for j in range(n))

        fig, ax = plt.subplots()
        ax.set_axis_off()
        tableau = Table(ax, bbox=[0, 0, 1, 1])
        hauteur, largeur = len(couts), len(couts[0])

        tableau.add_cell(0, 0, 0.1, 0.1, text="S/D", loc='center', facecolor="#40466e").get_text().set_color('white')
        for j in range(largeur):
            cell = tableau.add_cell(0, j+1, 0.1, 0.1, text=f"D{j+1}", loc='center', facecolor="#40466e")
            cell.get_text().set_color('white')
        for i in range(hauteur):
            cell = tableau.add_cell(i+1, 0, 0.1, 0.1, text=f"S{i+1}", loc='center', facecolor="#40466e")
            cell.get_text().set_color('white')

        for i in range(hauteur):
            for j in range(largeur):
                val = f"{couts[i][j]}\n({solution[i][j]})" if solution[i][j] != 0 else f"{couts[i][j]}"
                tableau.add_cell(i+1, j+1, 0.1, 0.1, text=val, loc='center', facecolor='white')

        for i in range(hauteur):
            total_source = sum(solution[i])
            tableau.add_cell(i+1, largeur+1, 0.1, 0.1, text=str(total_source), loc='center', facecolor='#d1e7dd')

        for j in range(largeur):
            total_dest = sum(solution[i][j] for i in range(hauteur))
            tableau.add_cell(hauteur+1, j+1, 0.1, 0.1, text=str(total_dest), loc='center', facecolor='#f8d7da')

        tableau.add_cell(hauteur+1, 0, 0.1, 0.1, text="∑", loc='center', facecolor='#40466e').get_text().set_color('white')
        tableau.add_cell(0, largeur+1, 0.1, 0.1, text="∑", loc='center', facecolor='#40466e').get_text().set_color('white')
        tableau.add_cell(hauteur+1, largeur+1, 0.1, 0.1, text="", loc='center', facecolor='white')

        ax.add_table(tableau)
        plt.title(f"📦 Méthode Nord-Ouest — Coût total = {total}", fontsize=12)
        plt.show()

    except Exception as e:
        messagebox.showerror("Erreur", str(e))

def interface_nord_ouest():
    global entry_sources, entry_destinations
    root = tk.Tk()
    root.title("📦 Méthode du Coin Nord-Ouest")
    root.geometry("600x500")
    root.configure(bg="#233c60")

    titre = tk.Label(root, text="📦 Méthode du Coin Nord-Ouest", font=("Helvetica", 18, "bold"),
                     fg="white", bg="#233c60")
    titre.pack(pady=10)

    label1 = tk.Label(root, text="Nombre de sources :", font=("Helvetica", 12), fg="white", bg="#233c60")
    label1.pack()
    entry_sources = tk.Entry(root, font=("Helvetica", 12), width=10)
    entry_sources.pack(pady=5)

    label2 = tk.Label(root, text="Nombre de destinations :", font=("Helvetica", 12), fg="white", bg="#233c60")
    label2.pack()
    entry_destinations = tk.Entry(root, font=("Helvetica", 12), width=10)
    entry_destinations.pack(pady=5)

    bouton = tk.Button(root, text="Lancer l’algorithme 🧠", font=("Helvetica", 12, "bold"),
                       bg="white", fg="#233c60", command=lancer_nord_ouest)
    bouton.pack(pady=20)
    tk.Button(root, text="❌ Quitter", font=("Arial", 12, "bold"),
                   bg="#657FEA", fg="white", command=root.destroy).pack(pady=10)
    info = tk.Label(root,
             text="💡 En télécom, cette méthode permet de démarrer une allocation\n"
                  "de ressources simple entre centres d’émission et de réception.",
             font=("Helvetica", 10), fg="white", bg="#233c60", justify="center")
    info.pack(pady=30)

    root.mainloop()

#--------------------steppingstone---------------------------
def nord_ouest(sources, destinations):
    m, n = len(sources), len(destinations)
    supply = sources.copy()
    demand = destinations.copy()
    solution = [[0]*n for _ in range(m)]
    i = j = 0
    while i < m and j < n:
        q = min(supply[i], demand[j])
        solution[i][j] = q
        supply[i] -= q
        demand[j] -= q
        if supply[i] == 0: i += 1
        if demand[j] == 0: j += 1
    return solution

def calcul_cout(solution, couts):
    return sum(solution[i][j] * couts[i][j] for i in range(len(solution)) for j in range(len(solution[0])))

def stepping_stone(sources, destinations, couts, solution):
    m, n = len(sources), len(destinations)
    while True:
        delta = [[None]*n for _ in range(m)]
        amelioration = False
        for i in range(m):
            for j in range(n):
                if solution[i][j] == 0:
                    chemin = trouver_cycle(i, j, solution)
                    if chemin:
                        gain = 0
                        sign = 1
                        for x, y in chemin:
                            gain += sign * couts[x][y]
                            sign *= -1
                        delta[i][j] = gain
                        if gain < 0:
                            amelioration = True
        if not amelioration:
            break  

        min_gain = 0
        best_pos = None
        best_cycle = []
        for i in range(m):
            for j in range(n):
                if delta[i][j] is not None and delta[i][j] < min_gain:
                    min_gain = delta[i][j]
                    best_pos = (i, j)
                    best_cycle = trouver_cycle(i, j, solution)

        if best_cycle:
            min_q = min(solution[x][y] for k, (x, y) in enumerate(best_cycle) if k % 2 == 1)
            for k, (x, y) in enumerate(best_cycle):
                if k % 2 == 0:
                    solution[x][y] += min_q
                else:
                    solution[x][y] -= min_q
    return solution

def trouver_cycle(si, sj, solution):
    m, n = len(solution), len(solution[0])
    def dfs(path, visited, horizontal):
        last_i, last_j = path[-1]
        for k in range(n if horizontal else m):
            i, j = (last_i, k) if horizontal else (k, last_j)
            if (i, j) == (si, sj) and len(path) >= 4:
                return path
            if (i, j) != (last_i, last_j) and solution[i][j] != 0 and (i, j) not in visited:
                new_path = path + [(i, j)]
                res = dfs(new_path, visited | {(i, j)}, not horizontal)
                if res:
                    return res
        return None

    return dfs([(si, sj)], set(), True)

def afficher_tableau(sources, destinations, couts, solution, titre):
    m, n = len(sources), len(destinations)
    fig, ax = plt.subplots()
    ax.set_axis_off()
    tableau = Table(ax, bbox=[0, 0, 1, 1])

    tableau.add_cell(0, 0, 0.1, 0.1, text="S/D", loc='center', facecolor="#40466e").get_text().set_color('white')
    for j in range(n):
        cell = tableau.add_cell(0, j+1, 0.1, 0.1, text=f"D{j+1}", loc='center', facecolor="#40466e")
        cell.get_text().set_color('white')
    for i in range(m):
        cell = tableau.add_cell(i+1, 0, 0.1, 0.1, text=f"S{i+1}", loc='center', facecolor="#40466e")
        cell.get_text().set_color('white')

    for i in range(m):
        for j in range(n):
            val = f"{couts[i][j]}\n({solution[i][j]})" if solution[i][j] > 0 else f"{couts[i][j]}"
            tableau.add_cell(i+1, j+1, 0.1, 0.1, text=val, loc='center', facecolor='white')

    for i in range(m):
        total_source = sum(solution[i])
        tableau.add_cell(i+1, n+1, 0.1, 0.1, text=str(total_source), loc='center', facecolor='#d1e7dd')
    for j in range(n):
        total_dest = sum(solution[i][j] for i in range(m))
        tableau.add_cell(m+1, j+1, 0.1, 0.1, text=str(total_dest), loc='center', facecolor='#f8d7da')
    tableau.add_cell(0, n+1, 0.1, 0.1, text="∑", loc='center', facecolor='#40466e').get_text().set_color('white')
    tableau.add_cell(m+1, 0, 0.1, 0.1, text="∑", loc='center', facecolor='#40466e').get_text().set_color('white')
    tableau.add_cell(m+1, n+1, 0.1, 0.1, text="", loc='center', facecolor='white')

    ax.add_table(tableau)
    total = calcul_cout(solution, couts)
    plt.title(f"{titre} — Coût total = {total}", fontsize=12)
    plt.show()

def lancer_stepping_stone():
    try:
        m = int(entry_sources.get())
        n = int(entry_destinations.get())
        if m < 1 or n < 1:
            raise ValueError("Les valeurs doivent être ≥ 1.")
        
        sources = [random.randint(30, 100) for _ in range(m)]
        destinations = [random.randint(30, 100) for _ in range(n)]

        total_sources = sum(sources)
        total_destinations = sum(destinations)

        if total_sources > total_destinations:
            destinations.append(total_sources - total_destinations)
            n += 1
        elif total_destinations > total_sources:
            sources.append(total_destinations - total_sources)
            m += 1

        couts = [[random.randint(1, 20) for _ in range(n)] for _ in range(m)]
        sol_init = nord_ouest(sources, destinations)
        afficher_tableau(sources, destinations, couts, sol_init, "🔹 Solution initiale (Nord-Ouest)")

        sol_opt = copy.deepcopy(sol_init)
        sol_opt = stepping_stone(sources, destinations, couts, sol_opt)
        afficher_tableau(sources, destinations, couts, sol_opt, "✅ Solution optimisée (Stepping Stone)")

    except Exception as e:
        messagebox.showerror("Erreur", str(e))

def interface_stepping_stone():
    global entry_sources, entry_destinations
    root = tk.Tk()
    root.title("🔄 Méthode Stepping Stone")
    root.geometry("600x500")
    root.configure(bg="#233c60")

    tk.Label(root, text="🔄 Méthode Stepping Stone", font=("Helvetica", 18, "bold"),
             fg="white", bg="#233c60").pack(pady=10)

    tk.Label(root, text="Nombre de sources :", font=("Helvetica", 12),
             fg="white", bg="#233c60").pack()
    entry_sources = tk.Entry(root, font=("Helvetica", 12), width=10)
    entry_sources.pack(pady=5)

    tk.Label(root, text="Nombre de destinations :", font=("Helvetica", 12),
             fg="white", bg="#233c60").pack()
    entry_destinations = tk.Entry(root, font=("Helvetica", 12), width=10)
    entry_destinations.pack(pady=5)

    tk.Button(root, text="Optimiser avec Stepping Stone 🧠", font=("Helvetica", 12, "bold"),
              bg="white", fg="#233c60", command=lancer_stepping_stone).pack(pady=20)
    tk.Button(root, text="❌ Quitter", font=("Arial", 12, "bold"),
                   bg="#657FEA", fg="white", command=root.destroy).pack(pady=10)
    tk.Label(root,
             text="💡 En télécom, cette méthode améliore la distribution initiale des ressources\n"
                  "en minimisant davantage les coûts de transport de données.",
             font=("Helvetica", 10), fg="white", bg="#233c60", justify="center").pack(pady=30)

    root.mainloop()

# -------------------- Interface principale ---------------------
def main_interface():
    root = tk.Tk()
    root.title("🔒 SMART Desktop Application")
    root.geometry("600x600")
    root.resizable(False, False)

    start_color = (0, 32, 62)
    end_color = (80, 120, 180)
    gradient = generate_subtle_gradient(start_color, end_color, 600, 600)
    bg_image = ImageTk.PhotoImage(gradient)
    root.bg_image = bg_image  

    canvas = tk.Canvas(root, width=600, height=600, highlightthickness=0)
    canvas.pack(fill="both", expand=True)
    canvas.create_image(0, 0, anchor="nw", image=bg_image)

    canvas.create_text(300, 40, text="🔒 SMART Desktop Application", font=("Helvetica", 22, "bold"), fill="#f0f0f0")

    # ------------ Buttons ----------------
    def open_programs():
        root.withdraw()
        second_window(root)

    bouton1 = tk.Button(root, text="➕ Algorithme de recherche opérationnelle", font=("Helvetica", 16, "bold"),
                        bg="white", fg="#00203E", padx=20, pady=10, width=30, height=2, command=open_programs)
    canvas.create_window(300, 150, window=bouton1)

    bouton2 = tk.Button(root, text="📜 Entrer", font=("Helvetica", 16, "bold"),
                    bg="white", fg="#00203E", padx=20, pady=10, width=30, height=2,
                    command=open_algos_description)
    canvas.create_window(300, 250, window=bouton2)

    bouton3 = tk.Button(root, text="❌ Quitter", font=("Helvetica", 16, "bold"),
                        bg="white", fg="#00203E", padx=20, pady=10, width=30, height=2, command=root.destroy)
    canvas.create_window(300, 350, window=bouton3)

    root.mainloop()

# -------------------- Deuxième fenêtre ---------------------
def second_window(root):
    second = tk.Toplevel()
    second.title("📘 Algorithmes de Recherche Opérationnelle")
    second.geometry("720x700")
    second.resizable(False, False)

    start_color = (0, 32, 62)
    end_color = (80, 120, 180)
    gradient = generate_subtle_gradient(start_color, end_color, 720, 700)
    bg_image = ImageTk.PhotoImage(gradient)
    second.bg_image = bg_image 

    canvas = tk.Canvas(second, width=720, height=700, highlightthickness=0)
    canvas.pack(fill="both", expand=True)
    canvas.create_image(0, 0, anchor="nw", image=bg_image)

    canvas.create_text(360, 40, text="📘 Algorithmes de Recherche Opérationnelle",
                       font=("Helvetica", 20, "bold"), fill="#f0f0f0")

    algo_names = [
        "Welsh Powel", "Dijkstra", "Potentiel Metra",
        "Kruskal", "Bellman Ford", "Ford Fulckerson",
        "Nord-Ouest", "Moindre Cout", "Stepping-Stone"
    ]

    algo_actions = {
        "Welsh Powel": interface_welsh_powell,
        "Dijkstra": interface_dijkstra,
        "Potentiel Metra": interface_potentiel_metra,
        "Kruskal": page_accueil,
        "Bellman Ford": interface_bellman_ford,
        "Ford Fulckerson": interface_ford_fulkerson,
        "Nord-Ouest": interface_nord_ouest,
        "Moindre Cout": interface_moindre_cout,
        "Stepping-Stone": interface_stepping_stone,
    }

    positions = [(i, j) for i in range(3) for j in range(3)]
    for idx, name in enumerate(algo_names):
        row, col = positions[idx]
        x = 140 + col * 220
        y = 120 + row * 130
        action = algo_actions.get(name, lambda: print("Non implémenté"))
        bouton = tk.Button(second, text=name, font=("Helvetica", 14, "bold"),
                           bg="white", fg="#00203E", padx=10, pady=10,
                           width=16, height=2, command=action)
        canvas.create_window(x, y, window=bouton)

    retour = tk.Button(second, text="⬅️ Retour", font=("Helvetica", 14, "bold"),
                       bg="white", fg="#00203E", padx=20, pady=10, width=20, height=2,
                       command=lambda: (second.destroy(), root.deiconify()))
    canvas.create_window(360, 580, window=retour)


# ------------------- Launch ---------------------
main_interface()
