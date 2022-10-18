from modules.boundary_estimation import detect_boundary, cubic_interpolate, local_extrapolate
import numpy as np
import matplotlib.pyplot as plt


def proximal_map_cluster(cluster_pts, r, R, alpha_fac):
    xy_points = [[point[0], point[1]] for point in cluster_pts]
    hull_pts, hull_area = detect_boundary(xy_points, alpha_factor=alpha_fac)
    boundary_pts = np.column_stack((hull_pts[0], hull_pts[1]))

    # CubicSpline Interpolation
    boundary_cubic = cubic_interpolate(boundary_pts)
    boundary_cubic = np.column_stack((boundary_cubic[0], boundary_cubic[1]))

    # # Concave Hull Envelope
    inner_hull_pts = local_extrapolate(boundary_cubic, r)
    outer_hull_pts = local_extrapolate(boundary_cubic, R)
    # plt.scatter(hull_pts_2[:,0], hull_pts_2[:,1], s=150, facecolor='none', edgecolors='red')
    # plt.scatter(hull_pts_2[:,0], hull_pts_2[:,1], s=700, facecolor='none', edgecolors='green')
    # plt.plot(hull_pts_1[:,0], hull_pts_1[:,1], c='red')
    plt.plot(outer_hull_pts[:, 0], outer_hull_pts[:, 1], c='green')
    return outer_hull_pts, hull_area
