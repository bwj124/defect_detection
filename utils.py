import glob
import os
import random
import re
import xml.etree.cElementTree as ET

import yaml


def reformat_xml(dataset_dir):
    """
    替换导出xml文件中的undefined
    :param xml_paths:
    :return:
    """
    xml_list = glob.glob(f"{dataset_dir}/annotations/*.xml")

    for xml_file in xml_list:

        tree = ET.parse(xml_file)
        root = tree.getroot()
        # print(root.text)

        for row in root.iter('object'):
            row[2].text = "0"
            row[3].text = "0"
            row[4].text = "0"
        tree.write(xml_file, 'UTF-8')  # 保存


def split_dataset(dataset_dir, ratio=0.9):
    """
    生成train.txt和val.txt
    :param dataset_dir: 数据集路径
    :param ratio: 训练集比例
    :return:
    """

    xml_dir = f'{dataset_dir}/annotations'  # 标签文件地址
    img_dir = f'{dataset_dir}/images'  # 图像文件地址
    path_list = list()
    for img in os.listdir(img_dir):
        img_path = os.path.join(img_dir, img)
        xml_path = os.path.join(xml_dir, img.replace('jpg', 'xml'))
        path_list.append((img_path, xml_path))
    random.shuffle(path_list)

    train_f = open(f'{dataset_dir}/train.txt', 'w')  # 生成训练文件
    val_f = open(f'{dataset_dir}/valid.txt', 'w')  # 生成验证文件

    for i, content in enumerate(path_list):
        img, xml = content
        pos = img.find("images")

        text = img[pos:] + ' ' + xml[pos:] + '\n'
        if i < len(path_list) * ratio:
            train_f.write(text)
        else:
            val_f.write(text)

    train_f.close()
    val_f.close()


def reformat_optimizer_config(config_path):
    """
    添加optimizer_config文件中缺少的tag
    :param config_path:
    :return:
    """
    with open(config_path) as f:
        lines = f.readlines()
    PiecewiseDecay_idx = [i for i, item in enumerate(lines) if re.search('schedulers.*', item)]
    lines.insert(PiecewiseDecay_idx[0] + 1, "  - !PiecewiseDecay\n")
    LinearWarmup_idx = [i for i, item in enumerate(lines) if re.search('start_factor.*', item)]
    lines.insert(LinearWarmup_idx[0], "  - !LinearWarmup\n")

    with open(config_path, "w") as f:
        for line in lines:
            f.write(line)


def reformat_dataset_config(config_path):
    """
    添加dataset_config文件中缺少的tag
    :param config_path:
    :return:
    """
    with open(config_path) as f:
        lines = f.readlines()
    EvalDataset_idx = [i for i, item in enumerate(lines) if re.search('EvalDataset.*', item)]
    lines.insert(EvalDataset_idx[0] + 1, "  !VOCDataSet\n")
    TestDataset_idx = [i for i, item in enumerate(lines) if re.search('TestDataset.*', item)]
    lines.insert(TestDataset_idx[0] + 1, "  !ImageFolder\n")
    TrainDataset_idx = [i for i, item in enumerate(lines) if re.search('TrainDataset.*', item)]
    lines.insert(TrainDataset_idx[0] + 1, "  !VOCDataSet\n")

    with open(config_path, "w") as f:
        for line in lines:
            f.write(line)


def update_yaml(base_path: str, save_path: str, **kwargs):
    """
    将更行的超参数写入yaml文件中
    :param base_path: baseline配置
    :param save_path: 保存路径
    :param kwargs: 更新的参数列表
    :return:
    """

    def update_dict(old_dict, key, value):
        # 递归更新字典
        if isinstance(value, dict):
            for k, v in value.items():
                update_dict(old_dict[key], k, v)
        else:
            old_dict[key] = value

    # 读取数据，获取文件
    with open(base_path) as f:
        yaml_data = yaml.load(f, Loader=yaml.SafeLoader)
    # 更新配置
    for k, v in kwargs.items():
        update_dict(yaml_data, k, v)

    # 写入数据
    with open(save_path, "w") as fw:
        yaml.dump(yaml_data, fw)


if __name__ == '__main__':
    # ud = {"snapshot_epoch" : 200,
    #       "_BASE_":['../datasets/defect_voc_fa9ke.yml',
    #                 '../runtim9e.yml', '_base_/opt9imizer_270e.yml', '_base_/yolov3_dark999net53.yml', '_base_/yolov3_reader.yml']}
    # ud = {"TrainDataset": {"dataset_dir": "test"}, "num_classes": 100}
    # update_yaml(yamlPath, yamlPath, **ud)

    reformat_optimizer_config("configs/yolov3/_base_/optimizer_270e_base.yml")
