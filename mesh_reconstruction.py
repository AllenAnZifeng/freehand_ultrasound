import copy
import open3d as o3d
import numpy as np
from open3d.cpu.pybind.geometry import PointCloud

POINT_CLOUD_PATH = '3d_coordinate.xyz'


def scale(geometry_obj, scale_x: float = 1, scale_y: float = 1, scale_z: float = 1):
    T = np.eye(4)
    T[0, 0] = scale_x
    T[1, 1] = scale_y
    T[2, 2] = scale_z
    return copy.deepcopy(geometry_obj).transform(T)


if __name__ == '__main__':
    pcd = o3d.io.read_point_cloud(POINT_CLOUD_PATH)  # type:PointCloud
    pcd = scale(pcd,0.077,0.077,0.21)
    # 37mm/480px = 0.077 mm/px
    # 0.21 mm/px
    # estimate surface normals
    pcd.estimate_normals()
    # pcd.orient_normals_consistent_tangent_plane(100)
    o3d.visualization.draw_geometries([pcd], mesh_show_back_face=True, point_show_normal=True)

    # Enable one of following algorithms

    # Use Ball pivoting
    # radii = [1,2,3,4,5]
    # mesh = o3d.geometry.TriangleMesh().create_from_point_cloud_ball_pivoting(
    # pcd, o3d.utility.DoubleVector(radii))

    # Use Poisson surface reconstruction
    depth = 9
    min_density_percentile = 0.1
    mesh, densities = o3d.geometry.TriangleMesh().create_from_point_cloud_poisson(pcd, depth=depth)
    vertices_to_remove = densities < np.quantile(densities, min_density_percentile)
    mesh.remove_vertices_by_mask(vertices_to_remove)

    # Show result
    mesh.compute_vertex_normals()
    mesh.paint_uniform_color([0.5, 0.5, 0.5])
    o3d.visualization.draw_geometries([mesh], mesh_show_back_face=True, point_show_normal=True)

    # triangle_clusters, cluster_n_triangles, cluster_area = (
    #     mesh.cluster_connected_triangles())
    # triangle_clusters = np.asarray(triangle_clusters)
    # cluster_n_triangles = np.asarray(cluster_n_triangles)
    # cluster_area = np.asarray(cluster_area)
    #
    # print("Show largest cluster")
    # mesh_1 = copy.deepcopy(mesh)
    # largest_cluster_idx = cluster_n_triangles.argmax()
    # triangles_to_remove = triangle_clusters != largest_cluster_idx
    # mesh_1.remove_triangles_by_mask(triangles_to_remove)
    # o3d.visualization.draw_geometries([mesh_1])


    # # average filter
    # mesh_out = mesh.filter_smooth_simple(number_of_iterations=10)
    # mesh_out.compute_vertex_normals()
    # mesh.paint_uniform_color([0.5, 0.5, 0.5])
    # o3d.visualization.draw_geometries([mesh_out])

    # # laplacian filter
    # mesh_out = mesh.filter_smooth_laplacian(number_of_iterations=10)
    # mesh_out.compute_vertex_normals()
    # o3d.visualization.draw_geometries([mesh_out])

    # # Taubin filter
    # mesh_out = mesh.filter_smooth_taubin(number_of_iterations=100)
    # mesh_out.compute_vertex_normals()
    # o3d.visualization.draw_geometries([mesh_out])

    # output stl,ply
    # o3d.io.write_triangle_mesh("mesh.ply", mesh)

