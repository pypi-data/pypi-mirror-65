import cv2
import numpy as np
import os
from .Detection import Detection
from .MtcnnDetector import MtcnnDetector

__all__ = ['ImageCrop']

FEATURE_DETECT_MAX_CORNERS = 50
FEATURE_DETECT_QUALITY_LEVEL = 0.1
FEATURE_DETECT_MIN_DISTANCE = 10


class HCenter:
    def __init__(self, model_dir="models", ctx_id=-1):
        model_name = os.path.join(model_dir, "model-500-326")
        self.net = Detection(model_name, ctx_id)

    def predict(self, image):
        return self.net.predict_center(image)


class VCenter:
    def __init__(self, model_dir="models", ctx_id=-1):
        self.net = MtcnnDetector(model_dir, ctx_id)

    def _face_center(self, image):
        """
        获取图片中最大人脸的中心位置
        :param image: numpy data
        :return: center
        """
        boxes, _ = self.net.detect(image)
        if len(boxes) == 0:
            return -1, -1

        area = [(x2 - x1) * (y2 - y1) for (x1, y1, x2, y2, _) in boxes]
        i = np.argmax(area)
        x = (boxes[i][0] + boxes[i][2]) / 2
        y = (boxes[i][1] + boxes[i][3]) / 2

        return x, y

    @staticmethod
    def _feature_center(image):
        """
        获取图片中特征值中心加权位置
        :param image: numpy data
        :return: center
        """
        if len(image.shape) < 3:
            gray = image
        elif image.shape[-1] == 4:
            gray = cv2.cvtColor(image, cv2.COLOR_RGBA2GRAY)
        else:
            gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        corners = cv2.goodFeaturesToTrack(gray,
                                          FEATURE_DETECT_MAX_CORNERS,
                                          FEATURE_DETECT_QUALITY_LEVEL,
                                          FEATURE_DETECT_MIN_DISTANCE)

        if corners is None or len(corners) == 0:
            return -1, -1

        x, y, weight = 0, 0, 0
        for point in corners:
            weight += 1
            x += point[0][0]
            y += point[0][1]

        return x / weight, y / weight

    @staticmethod
    def to_tensor(image):
        dst = np.zeros((image.shape[0], image.shape[1], 3))
        if len(image.shape) == 2:
            temp = image.reshape(image.shape[0], image.shape[1], 1)
            dst[:, :, 0] = temp[:, :, 0]
            dst[:, :, 1] = temp[:, :, 0]
            dst[:, :, 2] = temp[:, :, 0]
        else:
            dst[:, :, 0] = image[:, :, 0]
            dst[:, :, 1] = image[:, :, 1]
            dst[:, :, 2] = image[:, :, 2]
        return dst

    def predict(self, image):
        """
        获取图片中心位置
        :param image: numpy data
        :return: center
        """
        temp = self.to_tensor(image)
        center = self._face_center(temp)
        return self._feature_center(image) if center == (-1, -1) else center


class ImageCrop:
    def __init__(self, model_dir, ctx_id=-1):
        """
        图像裁剪
        :param ctx_id: 指定GPU，-1表示CPU
        """
        # 初始化HCenter模型
        self._hcenter = HCenter(model_dir, ctx_id=ctx_id)
        # 初始化VCenter模型
        self._vcenter = VCenter(model_dir, ctx_id=ctx_id)

    @staticmethod
    def _cal_size(size1, size2):
        """
        计算目标尺寸
        :param size1: 原尺寸
        :param size2: 目标尺寸
        :return: width, height, scale
        """
        w1, h1 = size1
        w2, h2 = size2
        if w1 / h1 <= w2 / h2:
            w = w1
            h = round(w1 * h2 / w2)
        else:
            h = h1
            w = round(h1 * w2 / h2)
        s = (w2 / w, h2 / h)

        return w, h, s

    @staticmethod
    def _cal_margin(size1, size2, center):
        """
        计算裁剪区域
        :param size1: 原尺寸
        :param size2: 目标尺寸
        :param center: 裁剪中心
        :return: top, down, left, right
        """
        w1, h1 = size1
        w2, h2 = size2
        x, y = center
        assert (w1 == w2 or h1 == h2)
        top, down, left, right = 0, h1 - 1, 0, w1 - 1
        if h1 == h2:
            left = max(int(round(x - (w2 - 1) / 2)), 0)
            offset = left + w2 - 1
            if offset > w1 - 1:
                left = left - (offset - (w1 - 1))
            right = left + w2 - 1
        else:
            top = max(int(round(y - (h2 - 1) / 2)), 0)
            offset = top + h2 - 1
            if offset > h1 - 1:
                top = top - (offset - (h1 - 1))
            down = top + h2 - 1

        return top, down, left, right

    def crop_margin(self, image, size):
        """
        计算图片裁剪边缘大小
        :param image: 输入图像（numpy data）
        :param size: 目标尺寸（w, h）
        :return: 输出边框（up, down, left, right）
        """
        size1 = image.shape[:2][::-1]
        width, height, scale = self._cal_size(size1, size)
        center = self._hcenter.predict(image) if height == size1[1] else self._vcenter.predict(image)

        return self._cal_margin(size1, (width, height), center)

    def crop_image(self, image, size):
        """
        图片裁剪
        :param image: 输入图像（numpy data）
        :param size: 目标尺寸（w, h）
        :return: 输出图像（numpy data）
        """
        bbox = self.crop_margin(image, size)
        dst = image[bbox[0]:bbox[1] + 1, bbox[2]:bbox[3] + 1]

        size1 = image.shape[:2][::-1]
        width, height, scale = self._cal_size(size1, size)
        _size = (int(round(width * scale[0])), int(round(height * scale[1])))

        return dst if scale == (1.0, 1.0) else cv2.resize(dst, _size)
