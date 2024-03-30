import numpy as np
import math
import plotly.graph_objects as go


# Ajoute un cercle a une figure en 3D
def add_circle(point, radius, normal, fig):
    x_center, y_center, z_center = point

    normal = np.array(normal) / np.linalg.norm(normal)

    T1 = np.array([0, -normal[2], normal[1]])
    T1 /= np.linalg.norm(T1)

    T2 = np.cross(normal, T1)

    theta = np.linspace(0, 2*np.pi, 100)
    x_circle = x_center + radius * (np.cos(theta) * T1[0] + np.sin(theta) * T2[0])
    y_circle = y_center + radius * (np.cos(theta) * T1[1] + np.sin(theta) * T2[1])
    z_circle = z_center + radius * (np.cos(theta) * T1[2] + np.sin(theta) * T2[2])

    fig.add_trace(go.Scatter3d(
        x=x_circle, y=y_circle, z=z_circle,
        mode='lines',
        line=dict(color='blue', width=2)
    ))

