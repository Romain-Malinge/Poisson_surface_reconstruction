import numpy as np
import plotly.graph_objects as go


# Ajoute un cercle a une figure
def add_circle(point, radius, angle, fig):

    x_center = point[0]
    y_center = point[1]
    z_center = point[2]

    theta_x = angle[0]
    theta_y = angle[1]
    theta_z = angle[2]

    theta = [i for i in range(0, 361, 20)]
    x_circle = [x_center + radius * np.cos(np.deg2rad(angle)) for angle in theta]
    y_circle = [y_center + radius * np.sin(np.deg2rad(angle)) for angle in theta]
    z_circle = [z_center] * len(theta)


    x_rotated_circle = []
    for i in range(len(theta)):
        y_temp = (y_circle[i] - y_center) * np.cos(np.deg2rad(theta_x)) - (z_circle[i] - z_center) * np.sin(np.deg2rad(theta_x)) + y_center
        z_temp = (y_circle[i] - y_center) * np.sin(np.deg2rad(theta_x)) + (z_circle[i] - z_center) * np.cos(np.deg2rad(theta_x)) + z_center
        x_rotated_circle.append(x_circle[i])
        y_circle[i] = y_temp
        z_circle[i] = z_temp

    # Rotation autour de l'axe y
    y_rotated_circle = []
    for i in range(len(theta)):
        x_temp = (x_rotated_circle[i] - x_center) * np.cos(np.deg2rad(theta_y)) + (z_circle[i] - z_center) * np.sin(np.deg2rad(theta_y)) + x_center
        z_temp = -(x_rotated_circle[i] - x_center) * np.sin(np.deg2rad(theta_y)) + (z_circle[i] - z_center) * np.cos(np.deg2rad(theta_y)) + z_center
        y_rotated_circle.append(y_circle[i])
        x_rotated_circle[i] = x_temp
        z_circle[i] = z_temp

    # Rotation autour de l'axe z
    z_rotated_circle = []
    for i in range(len(theta)):
        x_temp = (x_rotated_circle[i] - x_center) * np.cos(np.deg2rad(theta_z)) - (y_rotated_circle[i] - y_center) * np.sin(np.deg2rad(theta_z)) + x_center
        y_temp = (x_rotated_circle[i] - x_center) * np.sin(np.deg2rad(theta_z)) + (y_rotated_circle[i] - y_center) * np.cos(np.deg2rad(theta_z)) + y_center
        z_rotated_circle.append(z_circle[i])
        x_rotated_circle[i] = x_temp
        y_rotated_circle[i] = y_temp

    fig.add_trace(go.Scatter3d(
        x=x_rotated_circle, y=y_rotated_circle, z=z_rotated_circle,
        mode='lines',
        line=dict(color='blue', width=2)
    ))

