import numpy as np
import trimesh
from tqdm import tqdm

from utils import make_pca, lstsq_quadrics_fitting

# Objectif : Charger les attributs principaux d'un maillage 3D à partir d'un fichier.
# Paramètres :
# - path_to_model (str) : Chemin vers le fichier du maillage 3D.
# Retour :
# - maillage (objet trimesh) : Objet représentant le maillage.
# - dict_attribut_base (dictionnaire) : Dictionnaire contenant les attributs de base du maillage.
def load_mesh(path_to_model):
    # Load model with Trimesh
    maillage = trimesh.load(path_to_model, force='mesh')
    ## Coordonnées de sommets : np.array nx3
    sommets = np.array(maillage.vertices)
    nsommets = len(sommets)
    ## Indices de chaque face : np.array mx3
    faces = np.array(maillage.faces)
    ## Arêtes : ensemble de tuples correspondants aux deux indices des deux sommets de chaque arête
    aretes = maillage.edges

    ## Stockage 
    dict_attribut_base = {}
    dict_attribut_base["faces"] = faces
    dict_attribut_base["aretes"] = aretes
    dict_attribut_base["sommets"] = sommets
    dict_attribut_base['nsommets'] = nsommets

    return maillage, dict_attribut_base

# Objectif : Obtenir les voisins directs de chaque sommet.
# Paramètres :
# - nsommets (int) : Nombre de sommets dans le maillage.
# - aretes (ensemble de tuples d'indices) : Ensemble des arêtes du maillage.
# Retour :
# - neighbors (dictionnaire) : Dictionnaire où chaque clé est l'indice 
# d'un sommet et la valeur correspondante est un ensemble contenant 
# les indices de ses voisins directs.
def get_direct_neighbors(nsommets, aretes):
    neighbors = {i: set() for i in range(nsommets)}

    for a in aretes:
        neighbors[a[0]].add(a[1])
        neighbors[a[1]].add(a[0])

    return neighbors


# Objectif : Calculer les k plus proches voisins pour chaque sommet du maillage.
# Paramètres :
# - profondeur_k (int) : Profondeur pour la recherche des k plus proches voisins.
# - nsommet (int) : Nombre de sommets dans le maillage.
# voisins_directs (dictionnaire) : Dictionnaire contenant les voisins directs de chaque sommet.
# Retour :
# - knn_dict (dictionnaire) : Dictionnaire où chaque clé est l'indice d'un sommet et la valeur 
# correspondante est un ensemble contenant les indices de ses k plus proches voisins.
def compute_knn(profondeur_k, nsommet, voisins_directs):
    knn_dict = {i: get_k_neighbors(voisins_directs, profondeur_k, i, set())
                for i in range(nsommet)}
    return knn_dict


# Objectif : Fonction auxiliaire pour obtenir les k plus proches voisins d'un sommet donné.
# Paramètres :
# - voisins_directs (dictionnaire) : Dictionnaire contenant les voisins directs de chaque sommet.
# - profondeur_k (int) : Profondeur pour la recherche des k plus proches voisins.
# - point_index (int) : Indice du sommet pour lequel on cherche les k plus proches voisins.
# - n_set (ensemble) : Ensemble des indices des k plus proches voisins.
# Retour :
# - n_set (ensemble) : Ensemble des indices des k plus proches voisins.
def get_k_neighbors(voisins_directs, profondeur_k, point_index, n_set):
    if profondeur_k == 1 :
        return voisins_directs[point_index]
    elif profondeur_k > 1 :
        n_set.add(point_index)
        for _ in range(profondeur_k):
            for ptn in n_set:
                n_set = n_set.union(voisins_directs[ptn])
    return n_set


# Objectif : Calculer la courbure moyenne à partir des coefficients de la meilleure quadrique.
# Paramètres :
# - quadrics (tableau numpy 6x1) : Coefficients de la quadrique.
# Retour :
# - curv (float) : Valeur de la courbure moyenne calculée.
def curvature_meynet(quadrics):
    [a, b, c, d, e, f] = quadrics
    num = (1 + d**2)*a + (1 + e**2)*b - 4*a*b*c
    den = (1 + e**2 + d**2)**1.5
    return num/den


# Objectif : Estimer la meilleure quadrique approximant la surface en chaque sommet 
# et approximer la courbure moyenne en chaque point ainsi que l'erreur quadratique associée.
# Paramètres :
# - sommets (tableau numpy nx3) : Coordonnées des sommets du maillage.
# - knn (dictionnaire) : Dictionnaire contenant les k plus proches voisins pour chaque sommet.
# Retour :
# - outputs (tableau numpy nx2) : Tableau contenant la courbure moyenne et l'erreur associée à chaque sommet.
def compute_mean_curvature(sommets, knn):
    outputs = np.zeros((sommets.shape[0], 2))
    ## Pour chaque sommet
    for i in tqdm(knn):
        ## Coordonnées du point i
        current_point_i = sommets[i]
        ## Coordonnées de ses voisins
        neighbors_i = []
        for ptn in knn[i]:
            neighbors_i.append(sommets[ptn])
        ## Projection dans le nouveau repère 
        XYZ = make_pca(neighbors_i, current_point_i, 3)
        ## Calculs des coefficents de la meilleure quadric par moindre carrés
        X, error_origin = lstsq_quadrics_fitting(XYZ)
        ## Courbure et erreur/residus associées au point i
        curv_i = curvature_meynet(X)
        error_i = error_origin
        ## Sauvegarde de la valeur de la courbure et du résidus
        outputs[i,0] = curv_i
        outputs[i,1] = error_i
    return outputs

print('Fin import fonctions_tp2_curvature')