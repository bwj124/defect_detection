# Copyright (c) 2020 PaddlePaddle Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import sys

# add python path of PadleDetection to sys.path
parent_path = os.path.abspath(os.path.join(__file__, *(['..'] * 2)))
sys.path.insert(0, parent_path)

# ignore warning log
import warnings

warnings.filterwarnings('ignore')

import paddle
from ppdet.core.workspace import load_config
from ppdet.engine import Trainer


def inference_wrapper(config_path, model_weight, output_dir="output/"):
    cfg = load_config(config_path)
    cfg["weights"] = model_weight
    cfg["output_dir"] = output_dir

    paddle.set_device('gpu')

    trainer = Trainer(cfg, mode='test')

    # load weights
    trainer.load_weights(cfg.weights)

    def inference(input_image):
        # inference
        bbox_list = trainer.predict(
            [input_image],
            draw_threshold=0.5,
            output_dir=cfg.output_dir,
            save_txt=False,
            return_json=True)
        return bbox_list

    return inference


# if __name__ == '__main__':
#     config_path = "configs/yolov3/yolov3_darknet53_270e_voc_defect.yml"
#     model_weights = "output/yolov3_darknet53_270e_voc_defect/best_model.pdparams"
#
#     infer_img = "dataset/merge_dataset_fake/valid_image/IMG_20220117_101624_3.jpg"
#
#     inference = inference_wrapper(config_path, model_weights)
#
#     bbox_list = inference(infer_img)
#
#     print("bbox_list: ", bbox_list)


def predict(infer_img, config_path="configs/yolov3/yolov3_darknet53_270e_voc_defect.yml",
            model_weights="output/yolov3_darknet53_270e_voc_defect/best_model.pdparams"):
    inference = inference_wrapper(config_path, model_weights)
    bbox_list = inference(infer_img)
    return bbox_list
