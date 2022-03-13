import os
import subprocess
import time


class ProcessLauncher:
    def __init__(self, configs_path, exp_name, log_dir, pretrain_weights=None):
        super().__init__()
        self.exp_name = exp_name
        self.configs_path = configs_path
        self.pretrain_weights = pretrain_weights
        self.log_dir = log_dir
        os.makedirs(log_dir, exist_ok=True)

        self.command_list = self.format_command()

        self.process = None

    def format_command(self):
        pretrain_weights = f"{self.pretrain_weights}" if self.pretrain_weights else \
            "https://paddledet.bj.bcebos.com/models/yolov3_darknet53_270e_coco.pdparams"
        others = " finetune_exclude_pretrained_params=['cls_score','bbox_pred']"

        command_list = [f"python", "-u", "tools/train.py", "-c", f"{self.configs_path}", "-o",
                        f"pretrain_weights={pretrain_weights}", f"{others}"]

        return command_list

    def run(self):
        with open(f"{self.log_dir}/log.txt", "w") as f:
            self.process = subprocess.Popen(self.command_list, shell=False,
                                            stdout=f, stderr=f
                                            )

    def stop(self):
        if self.process:
            self.process.kill()
            print("stop training")
