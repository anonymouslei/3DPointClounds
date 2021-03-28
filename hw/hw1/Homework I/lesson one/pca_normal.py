# 实现PCA分析和法向量计算，并加载数据集中的文件进行验证

import open3d as o3d 
import os
import numpy as np
from pyntcloud import PyntCloud

# 功能：计算PCA的函数
# 输入：
#     data：点云，NX3的矩阵
#     correlation：区分np的cov和corrcoef，不输入时默认为False
#     sort: 特征值排序，排序是为了其他功能方便使用，不输入时默认为True
# 输出：
#     eigenvalues：特征值
#     eigenvectors：特征向量


def PCA(data, correlation=False, sort=True):
    # 作业1
    # 屏蔽开始
    data = data - data.mean(axis=0)
    u, s, vh = np.linalg.svd(data.T @ data)
    eigenvectors = u
    eigenvalues = s
    # 屏蔽结束

    if sort:
        sort = eigenvalues.argsort()[::-1]
        eigenvalues = eigenvalues[sort]
        eigenvectors = eigenvectors[:, sort]

    return eigenvalues, eigenvectors


def main():
    # 指定点云路径
    cat_index = 13 # 物体编号，范围是0-39，即对应数据集中40个物体
    # root_dir = '/Users/renqian/cloud_lesson/ModelNet40/ply_data_points' # 数据集路径
    root_dir = '/media/sf_VirtualShared/01_PointCloud/dataset/modelnet40_normal_resampled' # 数据集路径
    cat = os.listdir(root_dir)
    filename = os.path.join(root_dir, cat[cat_index], cat[cat_index]+'_0002.txt') # 默认使用第一个点云

    # 加载原始点云
    pc = np.loadtxt(filename, delimiter=',', dtype=np.float32)
    point_cloud_o3d = o3d.geometry.PointCloud()
    point_cloud_o3d.points = o3d.utility.Vector3dVector(pc[:, 0:3])

    o3d.visualization.draw_geometries([point_cloud_o3d])  # 显示原始点云

    # 从点云中获取点，只对点进行处理
    # points = point_cloud_pynt.points
    # print('total points number is:', points.shape[0])

    # 用PCA分析点云主方向
    points = pc[:, :3]
    points_mean = points.mean(axis=0)
    w, v = PCA(points)
    point_cloud_vector = v[:, 2] #点云主方向对应的向量
    print('the main orientation of this pointcloud is: ', point_cloud_vector)
    # TODO: 此处只显示了点云，还没有显示PCA
    points = [points_mean.tolist(), point_cloud_vector]
    lines = [[0, 1]]
    colors = [[1, 0, 0] for i in range(len(lines))]
    line_set = o3d.geometry.LineSet(points=o3d.utility.Vector3dVector(points), lines=o3d.utility.Vector2iVector(lines),)
    line_set.colors = o3d.utility.Vector3dVector(colors)
    # o3d.visualization.draw_geometries([point_cloud_o3d] + [line_set])

    # 循环计算每个点的法向量
    pcd_tree = o3d.geometry.KDTreeFlann(point_cloud_o3d)
    normals = []
    # 作业2
    # 屏蔽开始
    for i in range(np.array(point_cloud_o3d.points).shape[0]):
        [k, idx, _] = pcd_tree.search_knn_vector_3d(point_cloud_o3d.points[i], 20)
        points_nn = np.asarray(point_cloud_o3d.points)[idx]
        w, v = PCA(points_nn)
        point_cloud_vector = v[:, 2]
        normals.append(point_cloud_vector)

    # 由于最近邻搜索是第二章的内容，所以此处允许直接调用open3d中的函数

    # 屏蔽结束
    normals = np.array(normals, dtype=np.float64)
    # TODO: 此处把法向量存放在了normals中
    point_cloud_o3d.normals = o3d.utility.Vector3dVector(normals)
    o3d.visualization.draw_geometries([point_cloud_o3d])


if __name__ == '__main__':
    main()
