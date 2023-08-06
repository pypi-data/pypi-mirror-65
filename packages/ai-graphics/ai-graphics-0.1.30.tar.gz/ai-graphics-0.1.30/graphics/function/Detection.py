"""
Name : Detection.py
Author  : Cash
Contact : chenghong@tezign.com
Time    : 2019-11-29 10:52
Desc:
"""

import os
import cv2
import numpy as np
import torch
from ..libs.f3net import F3Net

__all__ = ['Detection']


class Detection(object):
    def __init__(self, model_name='model-32', ctx_id=-1):
        self.model_name = model_name
        self.device = torch.device("cuda:" + str(ctx_id)) if ctx_id > -1 else torch.device("cpu")
        self.model = self.load_model()

    def load_model(self):
        net = F3Net()
        net.load_state_dict(torch.load(self.model_name, map_location=None if torch.cuda.is_available() else 'cpu'))
        if torch.cuda.is_available():
            net.to(self.device)
        net.eval()

        return net

    @staticmethod
    def to_tensor(image):
        temp = np.zeros((image.shape[0], image.shape[1], 3))
        if len(image.shape) == 2:
            image = image.reshape(image.shape[0], image.shape[1], 1)
            temp[:, :, 0] = (image[:, :, 0] - 124.55) / 56.77
            temp[:, :, 1] = (image[:, :, 0] - 124.55) / 56.77
            temp[:, :, 2] = (image[:, :, 0] - 124.55) / 56.77
        else:
            temp[:, :, 0] = (image[:, :, 0] - 124.55) / 56.77
            temp[:, :, 1] = (image[:, :, 1] - 118.90) / 55.97
            temp[:, :, 2] = (image[:, :, 2] - 102.94) / 57.50
        temp = temp.transpose((2, 0, 1))
        return torch.from_numpy(temp)

    def predict(self, image):
        w, h = image.shape[:2][::-1]
        temp = cv2.resize(image, (352, 352), interpolation=cv2.INTER_LINEAR)
        temp = self.to_tensor(temp)
        temp = temp.type(torch.FloatTensor).unsqueeze(0)

        if torch.cuda.is_available():
            temp = temp.to(self.device)

        pred = self.model(temp.float())[1]
        pred = (torch.sigmoid(pred[0, 0, :, :]) * 255).cpu().data.numpy()
        pred = cv2.resize(np.round(pred), (w, h), interpolation=cv2.INTER_LINEAR)

        return pred.astype(np.uint8)

    def predict_center(self, image):
        width, height = image.shape[:2][::-1]
        temp = cv2.resize(image, (352, 352), interpolation=cv2.INTER_LINEAR)
        temp = self.to_tensor(temp)
        temp = temp.type(torch.FloatTensor).unsqueeze(0)

        if torch.cuda.is_available():
            temp = temp.to(self.device)

        pred = self.model(temp.float())[1]
        pred = (torch.sigmoid(pred[0, 0, :, :]) * 255).cpu().data.numpy()
        pred = pred.astype(np.uint8)
        w, h = pred.shape[1], pred.shape[0]
        pred = cv2.threshold(pred, 127, 255, cv2.THRESH_BINARY)[-1]
        contours = cv2.findContours(pred, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
        if len(contours) == 0:
            return (width - 1) / 2, (height - 1) / 2

        max_i = np.argmax([contour.size for contour in contours])
        if contours[max_i].size <= 8:
            return (width - 1) / 2, (height - 1) / 2

        M = cv2.moments(contours[max_i])
        if M["m00"] == 0.0:
            return (width - 1) / 2, (height - 1) / 2

        return (M["m10"] / M["m00"]) * (width / w), (M["m01"] / M["m00"]) * (height / h)
