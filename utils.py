import numpy as np
import os
from sklearn.decomposition import PCA
import numpy as np
from matplotlib import cm

def make_pca(data: np.ndarray, origin: np.ndarray, n_components: int):
    """
    Compute the PCA on the data provided
    :param n_components: n_components for the PCA
    :param data: Array containing data
    :return: projection of data 
    """
    x = np.vstack((np.array(data), origin))
    xc = x - origin
    #xc = xc.to_numpy()
    pca = PCA(n_components=n_components)
    pca.fit(xc)
    w = pca.components_
    new_coord = xc @ np.transpose(w)
    return new_coord

def lstsq_quadrics_fitting(pos_xyz):
    """
    Fit a given set of 3D points (x, y, z) to a quadrics of equation ax^2 + by^2 + cxy + dx + ey + f = z
    :param pos_xyz: A two-dimensional numpy array, containing the coordinates of the points
    :return:
    """
    ## Quadric equation
    A = np.ones((pos_xyz.shape[0], 6))
    A[:, 0:2] = np.square(pos_xyz[:, 0:2], pos_xyz[:, 0:2])
    A[:, 2] = np.multiply(pos_xyz[:, 0], pos_xyz[:, 1])
    A[:, 3:5] = pos_xyz[:, 0:2]
    ## Z-axis
    Z = pos_xyz[:, 2]
    ## coefficents of the quatrics equation
    X, _, _, _ = np.linalg.lstsq(A, Z, rcond=None)
    ## error
    residuals = Z - A @ X
    ## Erreur associée à l'origine est âr construction en dernière position
    error_origin = residuals[-1]
    return X, error_origin


def generate_colormap(distances: np.ndarray, c_type: str):
    """
    Generates a colormap according to the values contained in distances
    :param distances: a numpy.ndarray containing data from which create a colormap
    :param c_type: the type of colormap, it's a matplotlib colormap type
    :return:
    """
    colormap = []
    q25 = np.percentile(distances, 25)
    q75 = np.percentile(distances, 75)
    iqr = q75-q25

    min_dist = np.min(distances)
    max_dist = np.max(distances)
    normed_dist = distances / (q75 + 1.5*iqr)
    col = cm.get_cmap(c_type, 256)
    if min_dist != max_dist:
        for dist in normed_dist:
            if dist < (q25-1.5*iqr)/(q75 + 1.5*iqr) or dist > 1:
                #colormap.append([255, 0, 255])
                colormap.append([1, 0, 1])
            else:
                #colormap.append([255 * i for i in col(float(dist))])
                colormap.append([i for i in col(float(dist))])
    else:
        print("Error")
        n = len(distances)
        #colormap = n * [[0, 255, 0]]
        colormap = n * [[0, 1, 0]]
    return colormap

def generate_colormap2(distances: np.ndarray, c_type: str = 'jet'):
    """
    Generates a colormap according to the values contained in distances
    :param distances: a numpy.ndarray containing data from which create a colormap
    :param c_type: the type of colormap, it's a matplotlib colormap type
    :return:
    """
    colormap = []
    min_dist = np.min(distances)
    max_dist = np.max(distances)
    normed_dist = (distances - min_dist) / (max_dist - min_dist)
    col = cm.get_cmap(c_type, 256)
    if min_dist != max_dist:
        for dist in normed_dist:
            #colormap.append([255 * i for i in col(float(dist))])
            colormap.append([i for i in col(float(dist))])
    return colormap

def save(filename, obj_path, sommets, colormap):
    with open(filename, 'w+') as f:
        for i in range(sommets.shape[0]):
            x,y,z = sommets[i,:]
            color = colormap[i]
            f.writelines(f"v {x} {y} {z} {color[0]} {color[1]} {color[2]}\n")

        f_faces = open(obj_path, "r")
        lines = f_faces.readlines()
        for line in lines:
            if line[0] == 'f': f.writelines(line) 
        f_faces.close()
        f.close()


print('Fin import utils_tp2_curvature')