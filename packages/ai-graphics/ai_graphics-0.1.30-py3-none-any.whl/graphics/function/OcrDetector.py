import os
from collections import OrderedDict

import cv2
import numpy as np
import torch

from ..libs.craft.craft import CRAFT
from ..libs.craft.craft_utils import getDetBoxes, adjustResultCoordinates
from ..libs.craft.refinenet import RefineNet


def copy_state_dict(state_dict):
    if list(state_dict.keys())[0].startswith("module"):
        start_idx = 1
    else:
        start_idx = 0
    new_state_dict = OrderedDict()
    for k, v in state_dict.items():
        name = ".".join(k.split(".")[start_idx:])
        new_state_dict[name] = v

    return new_state_dict


def normalize(img, mean=(0.485, 0.456, 0.406), variance=(0.229, 0.224, 0.225)):
    # should be RGB order
    img = img.astype(np.float32)
    img -= np.array([mean[0] * 255.0, mean[1] * 255.0, mean[2] * 255.0], dtype=np.float32)
    img /= np.array([variance[0] * 255.0, variance[1] * 255.0, variance[2] * 255.0], dtype=np.float32)

    return img


def resize_aspect_ratio(img, max_size=1280, mag_ratio=1):
    height, width, channel = img.shape
    # magnify image size
    target_size = mag_ratio * max(height, width)
    # set original image size
    if target_size > max_size:
        target_size = max_size

    ratio = target_size / max(height, width)
    target_h, target_w = int(height * ratio), int(width * ratio)
    proc = cv2.resize(img, (target_w, target_h), interpolation=cv2.INTER_LINEAR)

    # make canvas and paste image
    target_h32, target_w32 = target_h, target_w
    if target_h % 32 != 0:
        target_h32 = target_h + (32 - target_h % 32)
    if target_w % 32 != 0:
        target_w32 = target_w + (32 - target_w % 32)
    resized = np.zeros((target_h32, target_w32, channel), dtype=np.float32)
    resized[0:target_h, 0:target_w, :] = proc

    return resized, ratio


class OcrDetector:
    def __init__(self, model_dir="models", ctx_id=-1):
        self.device = torch.device("cuda:" + str(ctx_id)) if ctx_id > -1 else torch.device("cpu")
        self.net, self.refinenet = None, None
        self.load_models(model_dir)

    def load_models(self, model_dir):
        self.net = CRAFT()
        model_path = os.path.join(model_dir, "craft_mlt_25k.pth")
        state_dict = torch.load(model_path, map_location=None if torch.cuda.is_available() else 'cpu')
        self.net.load_state_dict(copy_state_dict(state_dict))
        if torch.cuda.is_available():
            self.net.to(self.device)
        self.net.eval()

        self.refinenet = RefineNet()
        model_path = os.path.join(model_dir, "craft_refiner_CTW1500.pth")
        state_dict = torch.load(model_path, map_location=None if torch.cuda.is_available() else 'cpu')
        self.refinenet.load_state_dict(copy_state_dict(state_dict))
        if torch.cuda.is_available():
            self.refinenet.to(self.device)
            self.refinenet = torch.nn.DataParallel(self.refinenet)
        self.refinenet.eval()

    def detect(self, image, max_size=1280):
        img_resized, target_ratio = resize_aspect_ratio(image, max_size=max_size, mag_ratio=1.5)
        ratio_h = ratio_w = 1 / target_ratio
        x = normalize(img_resized)
        x = torch.from_numpy(x).permute(2, 0, 1)  # [h, w, c] to [c, h, w]
        x = x.unsqueeze(0)  # [c, h, w] to [b, c, h, w]
        if torch.cuda.is_available():
            x = x.to(self.device)
        with torch.no_grad():
            y, feature = self.net(x)

        # make score and link map
        score_text = y[0, :, :, 0].cpu().data.numpy()
        score_link = y[0, :, :, 1].cpu().data.numpy()
        if self.refinenet is not None:
            with torch.no_grad():
                y_refine = self.refinenet(y, feature)
            score_link = y_refine[0, :, :, 0].cpu().data.numpy()

        # Post-processing
        boxes, polys = getDetBoxes(score_text, score_link, 0.7, 0.4, 0.4)
        # coordinate adjustment
        boxes = adjustResultCoordinates(boxes, ratio_w, ratio_h)
        polys = adjustResultCoordinates(polys, ratio_w, ratio_h)
        for k in range(len(polys)):
            if polys[k] is None:
                polys[k] = boxes[k]
        return polys
