#!/usr/bin/env python

import matplotlib.pyplot as plt


def slice(height, width, pcd):
    sliced_pts = []
    for point in pcd:
        if (point[2] <= height+width and point[2] >= height-width):
            sliced_pts.append([point[0], point[1], point[2]])
    print("Sampled points from slicing: ", len(sliced_pts))
    return sliced_pts


def plot_grid(points):
    x_pts = [point[0] for point in points]
    y_pts = [point[1] for point in points]
    plt.figure()
    plt.scatter(x_pts, y_pts, color='green')
