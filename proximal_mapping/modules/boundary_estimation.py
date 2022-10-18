#!/usr/bin/env python
import imp
from scipy.interpolate import splprep, splev
import alphashape
import matplotlib.pyplot as plt
import numpy as np
import math


def detect_boundary(points2D, alpha_factor):
    # alpha_factor = alphashape.optimizealpha(points2D)
    hull = alphashape.alphashape(points2D, alpha=alpha_factor)
    hull_pts = hull.exterior.coords.xy
    hull_area = hull.area
    print("Alpha Optimized: ", alpha_factor)
    print("Boundary Points: ", len(hull_pts[0]))
    print("Area of the cluster: ", hull.area)
    return hull_pts, hull_area


def cubic_interpolate(boundary_pts):
    xp = boundary_pts[:, 0]
    yp = boundary_pts[:, 1]
    okay = np.where(np.abs(np.diff(xp)) + np.abs(np.diff(yp)) > 0)
    xp = np.r_[xp[okay], xp[-1], xp[0]]
    yp = np.r_[yp[okay], yp[-1], yp[0]]
    tck, u = splprep([xp[:-2], yp[:-2]], s=0.01, k=3)
    xnew = np.arange(0, 1.01, 0.01)
    out = splev(xnew, tck)
    plt.plot(out[0], out[1], color='purple',
             linewidth=2.0,  label='_nolegend_')
    plt.scatter(xp, yp, color='black',  label='_nolegend_')
    return out


def local_extrapolate(points, distance):
    projected_pts = []
    center_cluster = np.array(points).mean(axis=0)
    plt.scatter(center_cluster[0], center_cluster[1],
                color='Black', marker="*", label="_nolegend_")

    def myatan(x, y): return math.atan2(y, x)
    angle_pts = []
    for i, pt in enumerate(points):
        if (i-1) < 0:
            angle_pt = myatan(points[i+1][0]-points[-1]
                              [0], points[i+1][1]-points[-1][1])
        elif (i+1 >= len(points)):
            angle_pt = myatan(points[0][0]-points[-1]
                              [0], points[0][1]-points[-1][1])
        else:
            angle_pt = myatan(points[i+1][0]-points[i-1]
                              [0], points[i+1][1]-points[i-1][1])
        angle_pt = angle_pt*180.0/np.pi + 90  # Converting into  degrees
        angle_pts.append([pt[0], pt[1], angle_pt])
    for pt in angle_pts:
        new_pt = [0.0, 0.0, 0.0]
        new_pt[0] = pt[0] + distance*(np.cos(pt[2]*np.pi/180))
        new_pt[1] = pt[1] + distance*(np.sin(pt[2]*np.pi/180))
        new_pt[2] = pt[2]*np.pi/180 + np.pi

        projected_pts.append(new_pt)
    return np.array(projected_pts)
