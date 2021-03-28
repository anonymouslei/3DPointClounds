# 实现voxel滤波，并加载数据集中的文件进行验证

import open3d as o3d 
import os
import numpy as np

# 功能：对点云进行voxel滤波
# 输入：
#     point_cloud：输入点云
#     leaf_size: voxel尺寸
def voxel_filter(point_cloud, leaf_size):
    filtered_points = []
    # 作业3
    # 屏蔽开始
    dx, dy, dz = np.ceil((point_cloud.max(axis=0) - point_cloud.min(axis=0))/leaf_size)
    h_xyz = np.floor((point_cloud - point_cloud.min(axis=0))/leaf_size)
    h = h_xyz[:, 0] + h_xyz[:, 1] * dx + h_xyz[:, 2]*dy*dz

    ind = np.argsort(h)
    point_cloud = point_cloud[ind]
    h = h[ind]

    (unique, counts) = np.unique(h, return_counts=True)

    start, end = 0, 0
    for i in range(unique.shape[0]):
        start = end
        end = start + counts[i]
        # centroid
        centroid = np.mean(point_cloud[start:end, :], axis=0)
        filtered_points.append(centroid)
        # random
        # random_ind = np.random(counts[i], size=1, replace=False)
        # random_point = np.squeeze(point_cloud[start:end][random_ind])
        # filtered_points.append(random_point)

    # 屏蔽结束

    # 把点云格式改成array，并对外返回
    filtered_points = np.array(filtered_points, dtype=np.float64)
    return filtered_points

def main():
    # # 从ModelNet数据集文件夹中自动索引路径，加载点云
    cat_index = 18 # 物体编号，范围是0-39，即对应数据集中40个物体
    root_dir = '/media/sf_VirtualShared/01_PointCloud/dataset/modelnet40_normal_resampled' # 数据集路径
    cat = os.listdir(root_dir)
    filename = os.path.join(root_dir, cat[cat_index], cat[cat_index]+'_0001.txt') # 默认使用第一个点云

    # 加载自己的点云文件
    pc = np.loadtxt(filename, delimiter=',', dtype=np.float32)

    # 转成open3d能识别的格式
    point_cloud_o3d = o3d.geometry.PointCloud()
    point_cloud_o3d.points = o3d.utility.Vector3dVector(pc[:, 0:3])
    o3d.visualization.draw_geometries([point_cloud_o3d]) # 显示原始点云

    # 调用voxel滤波函数，实现滤波
    filtered_cloud = voxel_filter(np.array(point_cloud_o3d.points), 0.04)
    point_cloud_o3d.points = o3d.utility.Vector3dVector(filtered_cloud)
    # 显示滤波后的点云
    o3d.visualization.draw_geometries([point_cloud_o3d])

if __name__ == '__main__':
    main()
