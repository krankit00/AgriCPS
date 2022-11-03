#!/usr/bin/env python
import copy
import numpy as np
import open3d as o3d


def pcd_handle(path, rot_angle):
    pcd_load = o3d.io.read_point_cloud(path)
    # Based on the POV, aligning and centering pointcloud
    R = pcd_load.get_rotation_matrix_from_xyz((rot_angle, 0, 0))
    pcd_load_centered = copy.deepcopy(
        pcd_load).translate((0, 0, 0), relative=False)
    pcd_load_rotated = pcd_load_centered.rotate(R, center=(0, 0, 0))
    height_correction = (np.asarray(pcd_load_rotated.points)[:, 2]).min()
    pcd_load_transformed = copy.deepcopy(pcd_load_rotated).translate(
        (0, 0, -height_correction), relative=False)
    xyz_load = np.asarray(pcd_load_transformed.points)

    return xyz_load
