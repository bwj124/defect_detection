from tmux_launcher import Options, TmuxLauncher
from utils import update_yaml, reformat_optimizer_config, reformat_dataset_config, reformat_xml, split_dataset
from processLauuncher import ProcessLauncher
import time


class Launcher(TmuxLauncher):
    def __init__(self, configs_path, exp_name, pretrain_weights=None):
        super().__init__(exp_name)
        self.configs_path = configs_path
        self.pretrain_weights = pretrain_weights

    def options(self):
        opt = Options()
        pretrain_weights = f"{self.pretrain_weights}" if self.pretrain_weights else \
            "https://paddledet.bj.bcebos.com/models/yolov3_darknet53_270e_coco.pdparams"
        opt.set(
            c=self.configs_path,
            o=f"pretrain_weights={pretrain_weights} finetune_exclude_pretrained_params=['cls_score','bbox_pred']",
            eval=""

        )
        return [opt.specify()]

    def train_options(self):
        common_options = self.options()
        return [opt.specify() for opt in common_options]

    def test_options(self):
        opts = self.options()
        return [opt.specify() for opt in opts]


def create_task(
        exp_name,
        dataset_dir,
        model_weights,
        epoch=200,
        snapshot_epoch=100,
        learning_rate=0.000125,
        num_classes=6,
        ratio=0.9
):
    """
    生成模型训练需要的相关配置文件
    :param exp_name: 实验名
    :param dataset_dir: 训练数据路径
    :param model_weights: 模型保存路径
    :param epoch: 训练轮数
    :param snapshot_epoch: 权重保存轮数
    :param learning_rate: 学习率
    :param num_classes: 缺陷类别数
    :param ratio: 训练集比例
    :return: 任务启动配置文件路径
    """

    DATASET_CONFIG_BASE = "configs/datasets/dataset_base.yml"
    OPTIMIZER_CONFIG_BASE = "configs/yolov3/_base_/optimizer_270e_base.yml"
    NET_CONFIG_BASE = "configs/yolov3/_base_/yolov3_darknet53_base.yml"
    READER_CONFIG_BASE = "configs/yolov3/_base_/yolov3_reader_base.yml"
    TASK_CONFIG_BASE = "configs/yolov3/yolov3_darknet53_270e_base.yml"

    # 生成新的配置文件
    dataset_config_exp = f"configs/datasets/dataset_{exp_name}.yml"
    optimizer_config_exp = f"configs/yolov3/_base_/optimizer_270e_{exp_name}.yml"
    net_config_exp = f"configs/yolov3/_base_/yolov3_darknet53_{exp_name}.yml"
    reader_config_exp = f"configs/yolov3/_base_/yolov3_reader_{exp_name}.yml"
    task_config_exp = f"configs/yolov3/yolov3_darknet53_270e_{exp_name}.yml"

    # 分割训练集和测试集
    split_dataset(dataset_dir, ratio)
    # 替换导出xml文件中的undefined
    reformat_xml(dataset_dir)

    update_yaml(base_path=DATASET_CONFIG_BASE,
                save_path=dataset_config_exp,
                **{"num_classes": num_classes,
                   "TrainDataset": {"dataset_dir": dataset_dir},
                   "EvalDataset": {"dataset_dir": dataset_dir},
                   "TestDataset": {"dataset_dir": dataset_dir},
                   }
                )

    # 添加丢失的tag
    reformat_dataset_config(dataset_config_exp)

    update_yaml(base_path=OPTIMIZER_CONFIG_BASE,
                save_path=optimizer_config_exp,
                **{"epoch": epoch, "LearningRate": {'base_lr': learning_rate}}
                )
    # 添加丢失的tag
    reformat_optimizer_config(optimizer_config_exp)

    update_yaml(base_path=READER_CONFIG_BASE,
                save_path=reader_config_exp
                )
    update_yaml(base_path=NET_CONFIG_BASE,
                save_path=net_config_exp
                )
    update_yaml(base_path=TASK_CONFIG_BASE,
                save_path=task_config_exp,
                **{
                    "snapshot_epoch": snapshot_epoch,
                    "weights": model_weights,
                    "_BASE_": [
                        f'../datasets/dataset_{exp_name}.yml',
                        '../runtime.yml',
                        f'_base_/optimizer_270e_{exp_name}.yml',
                        f'_base_/yolov3_darknet53_{exp_name}.yml',
                        f'_base_/yolov3_reader_{exp_name}.yml',
                    ],
                }
                )
    return task_config_exp


if __name__ == '__main__':
    exp_name = "test_interface"
    # 数据集路径
    dataset_dir = "dataset/merge_dataset_fake"
    # 模型保存路径
    model_weights = f"output/yolov3_darknet53_270e_{exp_name}/model_final"
    # 日志路径
    log_dir = f"output/yolov3_darknet53_270e_{exp_name}"

    # 创建训练所需的配置文件
    task_config_path = create_task(exp_name, dataset_dir, model_weights)

    # pretrain_weights=None 从头开始训练，设置权重路径则为继续训练
    pretrain_weights = None
    # pretrain_weights = "output/yolov3_darknet53_270e_test_interface/6.pdparams"
    # task = Launcher(configs_path=task_config_path, exp_name=exp_name, pretrain_weights=pretrain_weights)
    task = ProcessLauncher(configs_path=task_config_path, exp_name=exp_name, log_dir=log_dir,
                           pretrain_weights=pretrain_weights)

    # 开始训练任务
    task.run()

    # 停止训练任务
    # task.stop()


def retrain_task(exp_name, dataset_dir="dataset/merge_dataset_fake", pretrain_weights = None):
    model_weights = f"output/yolov3_darknet53_270e_{exp_name}/model_final"
    log_dir = f"output/yolov3_darknet53_270e_{exp_name}"
    task_config_path = create_task(exp_name, dataset_dir, model_weights)

    # pretrain_weights=None 从头开始训练，设置权重路径则为继续训练
    # pretrain_weights = "output/yolov3_darknet53_270e_test_interface/6.pdparams"
    # task = Launcher(configs_path=task_config_path, exp_name=exp_name, pretrain_weights=pretrain_weights)
    task = ProcessLauncher(configs_path=task_config_path, exp_name=exp_name, log_dir=log_dir,
                           pretrain_weights=pretrain_weights)
    return task
