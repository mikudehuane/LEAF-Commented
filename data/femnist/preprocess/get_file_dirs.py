'''
Creates .pkl files for:
1. list of directories of every image in 'by_class'
2. list of directories of every image in 'by_write'
the hierarchal structure of the data is as follows:
- by_class -> classes -> folders containing images -> images
- by_write -> folders containing writers -> writer -> types of images -> images
the directories written into the files are of the form 'raw_data/...'
'''

import os
import sys

utils_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
utils_dir = os.path.join(utils_dir, 'utils')
sys.path.append(utils_dir)

import util

parent_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))  # LEAF/data/femnist/

class_files = []  # (class, file directory)
write_files = []  # (writer, file directory)

class_dir = os.path.join(parent_path, 'data', 'raw_data', 'by_class')  # 绝对路径
rel_class_dir = os.path.join('data', 'raw_data', 'by_class')  # 相对 LEAF/ 的路径
classes = os.listdir(class_dir)
classes = [c for c in classes if len(c) == 2]

for cl in classes:
    cldir = os.path.join(class_dir, cl)  # 该类别 cl 数据的绝对路径
    rel_cldir = os.path.join(rel_class_dir, cl)  # 该类别 cl 数据 相对 LEAF/ 的路径
    subcls = os.listdir(cldir)
    # 文件夹内容为：
    #   hsf_0  hsf_0.mit  hsf_1  hsf_1.mit  hsf_2  hsf_2.mit  hsf_3  hsf_3.mit  hsf_4  hsf_4.mit
    #   hsf_6  hsf_6.mit  hsf_7  hsf_7.mit  train_30
    # 从中选取 hsf_\d/ 的文件夹（存放了一些图片文件）
    subcls = [s for s in subcls if (('hsf' in s) and ('mit' not in s))]

    for subcl in subcls:
        subcldir = os.path.join(cldir, subcl)  # 子文件夹绝对路径
        rel_subcldir = os.path.join(rel_cldir, subcl)  # 子文件夹相对路径
        images = os.listdir(subcldir)
        image_dirs = [os.path.join(rel_subcldir, i) for i in images]  # 子文件夹中各个图片的相对路径

        for image_dir in image_dirs:
            class_files.append((cl, image_dir))  # 类别与相对路径的对应关系

write_dir = os.path.join(parent_path, 'data', 'raw_data', 'by_write')
rel_write_dir = os.path.join('data', 'raw_data', 'by_write')
write_parts = os.listdir(write_dir)

for write_part in write_parts:
    writers_dir = os.path.join(write_dir, write_part)
    rel_writers_dir = os.path.join(rel_write_dir, write_part)
    writers = os.listdir(writers_dir)

    for writer in writers:
        writer_dir = os.path.join(writers_dir, writer)
        rel_writer_dir = os.path.join(rel_writers_dir, writer)
        wtypes = os.listdir(writer_dir)

        for wtype in wtypes:
            type_dir = os.path.join(writer_dir, wtype)
            rel_type_dir = os.path.join(rel_writer_dir, wtype)
            images = os.listdir(type_dir)
            image_dirs = [os.path.join(rel_type_dir, i) for i in images]

            for image_dir in image_dirs:
                write_files.append((writer, image_dir))

util.save_obj(
    class_files,
    os.path.join(parent_path, 'data', 'intermediate', 'class_file_dirs'))
util.save_obj(
    write_files,
    os.path.join(parent_path, 'data', 'intermediate', 'write_file_dirs'))
