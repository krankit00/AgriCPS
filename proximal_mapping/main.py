#!/usr/bin/env python

import matplotlib.pyplot as plt
import numpy as np
from modules.slicing import slice, plot_grid
from modules.pcd_handler import pcd_handle
from modules.clustering import cluster
from modules.proximal_coverage import proximal_map_cluster
from data.old_farm.parameters import thickness, uav_size, pcd_path, alpha_factor, eps, min_samples, operating_height

isPlotting = True


def main():
    global path, operating_height, thickness

    ### Point Cloud Loaded ###
    xyz_load = pcd_handle(pcd_path)  # Returns Numpy Array
    print('PointCloud loaded with', len(xyz_load), 'points')

    # Respective points
    height_biomass = round(xyz_load[:, 2].max() - xyz_load[:, 2].min(), 2)
    print("Maximum Height of Biomass Recorded", height_biomass, "meters")

    hull_points = []
    hull_areas = []

    # Slicing
    sliced_pts = slice(operating_height, thickness, xyz_load)

    grid = plot_grid(sliced_pts)
    # Clustering using DBSCAN

    clusters = cluster(sliced_pts, eps, min_samples)

    uav_size = 0.1
    obstacle_map = []
    for label in np.unique(clusters.labels_):
        if (label == -1):
            print("Ignoring Noise")
        elif (label != -1):
            test_pts = np.array(sliced_pts)[clusters.labels_ == label]
            print("Cluster No: ", label+1)
            hull_pts, hull_area = proximal_map_cluster(
                test_pts, uav_size, 2*uav_size, alpha_fac=alpha_factor)  # Farm_meshed_Downsampled
            hull_points.append(hull_pts)  # Hull points = [x, y, angle]
            hull_areas.append(hull_area)  # Proximal Mapping
            obstacle_map += [(x, y, uav_size) for x, y, z in test_pts]

    # Plot Labels
    if isPlotting:
        plt.xlabel('X(m)', fontsize=12)
        plt.ylabel('Y(m)', fontsize=12)
        title = 'Proximal Map of Clusters'
        filename = title.lower().replace(" ", "_")
        plt.grid()
        plt.title(title, fontsize=12)
        plt.gca().set_aspect('equal', adjustable='box')
        plt.draw()
        plt.scatter(0, 0, marker='x', color='black')
        ax = plt.axes()
        ax.set(facecolor="lightcoral")
        path = './'
        plt.savefig(path+filename + '.png', dpi=500)
        plt.show()


if __name__ == "__main__":
    main()
