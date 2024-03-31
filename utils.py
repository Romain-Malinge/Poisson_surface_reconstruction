import numpy as np
import math
import plotly.graph_objects as go


# Créer une nouvelle figure
def new_fig():
    fig = go.Figure()
    fig.update_layout(scene=dict(
        xaxis_title='X',
        yaxis_title='Y',
        zaxis_title='Z'),
        showlegend=False)
    return fig


# Ajoute un point à une figure en 3D
def add_point(point, fig, color):
    fig.add_trace(go.Scatter3d(
        x=[point[0]],
        y=[point[1]],
        z=[point[2]],
        mode='markers',
        marker=dict(color=color, size=3)
    ))

# Ajoute un groupe de points à une figure en 3D
def add_points(points, fig, color):
    for point in points:
        add_point(point, fig, color)


# Ajouter une ligne a une figure en 3D
def add_line(a, b, fig, color):
    fig.add_trace(go.Scatter3d(
        x=[a[0], b[0]],
        y=[a[1], b[1]],
        z=[a[2], b[2]],
        mode='lines',
        line=dict(color=color, width=2)
    ))


# Ajoute un cercle a une figure en 3D
def add_circle(point, radius, normal, fig, color):

    x_center, y_center, z_center = point

    normal = np.array(normal) / np.linalg.norm(normal)

    T1 = np.array([0, -normal[2], normal[1]])
    T1 /= np.linalg.norm(T1)

    T2 = np.cross(normal, T1)

    theta = np.linspace(0, 2*np.pi, 100)

    x_circle = x_center + radius * (np.cos(theta) * T1[0] + np.sin(theta) * T2[0])
    y_circle = y_center + radius * (np.cos(theta) * T1[1] + np.sin(theta) * T2[1])
    z_circle = z_center + radius * (np.cos(theta) * T1[2] + np.sin(theta) * T2[2])

    fig.add_trace(go.Mesh3d(
        x=x_circle,
        y=y_circle,
        z=z_circle,
        color=color
    ))



