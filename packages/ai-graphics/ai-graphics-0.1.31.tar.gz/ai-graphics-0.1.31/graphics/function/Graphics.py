"""
Name : Graphics.py
Author  : Cash
Contact : tkggpdc2007@163.com
Time    : 2020-01-08 10:52
Desc:
"""

import math

import cv2
import numpy as np

__all__ = ['resize',
           'convert_heatmap',
           'composite',
           'alpha_to_white',
           'alpha_to_mask',
           'alpha_compose',
           'crop_margin',
           'add_border',
           'erase_border',
           'margin_nonzero',
           'alpha_nonzero',
           'hash_similarity',
           'histogram_similarity',
           'orb_similarity',
           'variance_similarity',
           'layer_mask',
           'layer_reflection',
           'layer_shadow',
           'get_contours']

# 初始化ORB检测器
_orb = cv2.ORB_create()
# 提取并计算特征点
_bf = cv2.BFMatcher(cv2.NORM_HAMMING)


def resize(image, max_size=640):
    """
    批量缩放图像
    :param image: numpy data
    :param max_size: max size of width, height
    :return: numpy data
    """
    r = 1.0
    if max(image.shape) > max_size:
        h, w, _ = image.shape
        r = max_size / max(w, h)
        image = cv2.resize(image, (int(w * r), int(h * r)))
    return image, r


def convert_heatmap(image):
    """
    转换成热力图
    :param image: 输入图片（numpy data）
    :return: 输出图片
    """
    image = (np.clip(image, 0, 1) * 255).astype(np.uint8)
    image = cv2.applyColorMap(image, cv2.COLORMAP_JET)

    return image


def composite(fg, bg):
    if len(fg.shape) < 3 or fg.shape[2] < 4:
        return fg

    h, w = fg.shape[:2]
    bg_h, bg_w = bg.shape[:2]

    w_r, h_r = w / bg_w, h / bg_h
    ratio = w_r if w_r > h_r else h_r
    if ratio > 1:
        bg = cv2.resize(src=bg, dsize=(math.ceil(bg_w * ratio), math.ceil(bg_h * ratio)), interpolation=cv2.INTER_CUBIC)
        bg_h, bg_w = bg.shape[:2]

    x = np.random.randint(0, bg_w - w) if bg_w > w else 0
    y = np.random.randint(0, bg_h - h) if bg_h > h else 0
    fg = np.array(fg, np.float32)
    bg = np.array(bg[y:y + h, x:x + w], np.float32)

    alpha = np.zeros((h, w, 1), np.float32)
    alpha[:, :, 0] = fg[:, :, 3] / 255.
    im = alpha * fg[:, :, :3] + (1 - alpha) * bg

    return im.astype(np.uint8)


def alpha_to_white(src):
    """
    透明图转白底图
    :param src: numpy data with 4 channels
    :return: numpy data with 3 channels
    """
    try:
        if len(src.shape) < 3 or src.shape[-1] < 4:
            return src

        h, w = src.shape[:2]
        alpha = np.expand_dims(src[:, :, 3] / 255.0, -1)
        new = np.ones((h, w, 3), np.uint8) * 255
        new[:, :] = src[:, :, :3] * alpha + new * (1 - alpha)

    except ValueError:
        return src

    return new


def alpha_to_mask(src):
    """
    透明图转白底图
    :param src: numpy data with 4 channels
    :return: numpy data with 3 channels
    """
    try:
        if len(src.shape) < 3 or src.shape[-1] < 4:
            return src
        new = cv2.threshold(src[:, :, -1], 255 * 0.05, 255, cv2.THRESH_BINARY)[-1]
    except ValueError:
        return src

    return new


def alpha_compose(image, src, x, y):
    """
    图像alpha通道融合
    :param image: numpy data with 3\4 channels
    :param src: numpy data with 4 channels
    :param x: col
    :param y: row
    :return: numpy data with 4 channels
    """
    try:
        if len(image.shape) < 3:
            return image

        if len(src.shape) < 3 or src.shape[-1] < 4:
            return src

        new = image.copy()
        if new.shape[-1] == 3:
            new = cv2.cvtColor(new, cv2.COLOR_RGB2RGBA)

        width, height = new.shape[:2][::-1]
        w, h = src.shape[:2][::-1]

        x1, y1 = max(-x, 0), max(-y, 0)
        x2, y2 = min(width - x, w), min(height - y, h)
        src = src[y1:y2, x1:x2]
        alpha = np.expand_dims(src[:, :, 3] / 255.0, -1)

        x, y = max(x, 0), max(y, 0)
        w, h = src.shape[:2][::-1]
        new[y:y + h, x:x + w] = src * alpha + new[y:y + h, x:x + w] * (1 - alpha)

    except ValueError:
        return image

    return new


def crop_margin(image, threshold1=15, threshold2=55):
    """
    计算图片裁剪（白底/透明）边缘大小
    :param image: 输入图像（numpy data）
    :param threshold1: first threshold for the hysteresis procedure
    :param threshold2: second threshold for the hysteresis procedure
    :return: 输出边框（up, down, left, right）
    """

    w, h = image.shape[:2][::-1]
    if len(image.shape) < 3:
        new = cv2.Canny(image, threshold1, threshold2)
        points = np.argwhere(new[:, :] > 0)[:, ::-1]
    elif image.shape[-1] == 3:
        new = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        new = cv2.Canny(new, threshold1, threshold2)
        points = np.argwhere(new[:, :] > 0)[:, ::-1]
    else:
        points = np.argwhere(image[:, :, -1] > 255 * 0.05)[:, ::-1]
        if points.size > 0:
            _, _, _w, _h = cv2.boundingRect(points)
            if _w == w and _h == h:
                new = cv2.cvtColor(image[:, :, :-1], cv2.COLOR_RGB2GRAY)
                new = cv2.Canny(new, threshold1, threshold2)
                points = np.argwhere(new[:, :] > 0)[:, ::-1]

    x, y = 0, 0
    if points.size > 0:
        x, y, w, h = cv2.boundingRect(points)

    top, down, left, right = y, y + h - 1, x, x + w - 1

    return top, down, left, right


def margin_nonzero(image, thres=220):
    """
    计算图片（白底/透明）非零边缘大小
    :param image: 输入图像（numpy data）
    :param thres: 阈值
    :return: 输出边框（up, down, left, right）
    """

    w, h = image.shape[:2][::-1]
    if len(image.shape) < 3:
        new = 255 - image
    elif image.shape[-1] == 3:
        new = 255 - image
        new = new[:, :, 0] + new[:, :, 1] + new[:, :, 2]
    else:
        new = image[:, :, -1]
        points = np.argwhere(new > thres)[:, ::-1]
        if points.size > 0:
            _, _, _w, _h = cv2.boundingRect(points)
            if _w == w and _h == h:
                new = 255 - image[:, :, :-1]
                new = new[:, :, 0] + new[:, :, 1] + new[:, :, 2]

    x, y = 0, 0
    points = np.argwhere(new > 0)[:, ::-1]
    if points.size > 0:
        x, y, w, h = cv2.boundingRect(points)

    top, down, left, right = y, y + h - 1, x, x + w - 1

    return top, down, left, right


def add_border(image, border, color=255):
    """
    添加边框
    :param image: numpy data with 3 channers
    :param border: [up, down, left, right]
    :param color: int, (r, g, b) or (r, g, b, a)
    :return:
    """
    up, down, left, right = border
    if up < 0 or down < 0 or left < 0 or right < 0:
        return image

    if len(image.shape) < 3:
        h, w = image.shape
        height, width = h + up + down, w + left + right
        new = np.empty((height, width), np.uint8)
        if isinstance(color, int):
            value = color
        elif len(color) > 0:
            value = color[0]
        else:
            value = 255
    elif image.shape[-1] == 3:
        h, w, c = image.shape
        height, width, channel = h + up + down, w + left + right, c
        new = np.empty((height, width, channel), np.uint8)
        if isinstance(color, int):
            value = (color, color, color)
        elif len(color) >= 3:
            value = (color[0], color[1], color[2])
        else:
            value = (255, 255, 255)
    else:
        h, w, c = image.shape
        height, width, channel = h + up + down, w + left + right, c
        new = np.empty((height, width, channel), np.uint8)
        if isinstance(color, int):
            value = (color, color, color, color)
        elif len(color) == 3:
            value = (color[0], color[1], color[2], 0 if image[0, 0, -1] < 128 else 255)
        elif len(color) == 4:
            value = (color[0], color[1], color[2], color[3])
        else:
            value = (255, 255, 255, 0)

    new[:, :] = value
    new[up:height - down, left:width - right] = image

    return new


def erase_border(image, border, color):
    """
    添加边框
    :param image: numpy data with 3 channels
    :param border: [up, down, left, right]
    :param color: (r, g, b)
    :return:
    """
    if len(image.shape) < 3:
        return image

    height, width, _ = image.shape
    up, down, left, right = border
    if up < 0 or down < 0 or left < 0 or right < 0:
        return image
    new = np.empty((height, width, 3))
    new[:, :] = color
    new[up:height - down, left:width - right] = image[up:height - down, left:width - right]
    return new.astype(np.uint8)


def alpha_nonzero(image):
    """
    处理图层图像，裁剪空白区域，保留最小凸包
    :param image:
    :return:
    """
    if len(image.shape) != 3 and image.shape[-1] != 4:
        return image
    x = np.nonzero(image[:, :, 3])
    c_min = min(x[1])
    c_max = max(x[1])
    r_min = min(x[0])
    r_max = max(x[0])
    return image[r_min:r_max + 1, c_min:c_max + 1]


def hash_similarity(image1, image2, type='dHash'):
    def a_hash(img):
        img = cv2.resize(img, (8, 8), interpolation=cv2.INTER_CUBIC)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        np_mean = np.mean(gray)
        value = (gray >= np_mean) + 0  # 大于平均值=1，否则=0
        value_list = value.reshape(1, -1)[0].tolist()  # 展平->转成列表
        value_str = ''.join([str(x) for x in value_list])
        return value_str

    def p_hash(img):
        img = cv2.resize(img, (32, 32))
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray = cv2.dct(np.float32(gray))
        gray = gray[0:8, 0:8]  # opencv实现的掩码操作
        np_mean = np.mean(gray)
        value = (gray > np_mean) + 0
        value_list = value.reshape(1, -1)[0].tolist()
        value_str = ''.join([str(x) for x in value_list])
        return value_str

    def d_hash(img):
        img = cv2.resize(img, (9, 8), interpolation=cv2.INTER_CUBIC)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # 每行前一个像素大于后一个像素为1，相反为0，生成哈希
        hash_str = []
        for i in range(8):
            hash_str.append(gray[:, i] > gray[:, i + 1])
        hash_str = np.array(hash_str) + 0
        hash_str = hash_str.T
        hash_str = hash_str.reshape(1, -1)[0].tolist()
        hash_str = ''.join([str(x) for x in hash_str])
        return hash_str

    if type == 'aHash':
        s1, s2 = a_hash(image1), a_hash(image2)
    elif type == 'pHash':
        s1, s2 = p_hash(image1), p_hash(image2)
    else:
        s1, s2 = d_hash(image1), d_hash(image2)

    return sum([ch1 != ch2 for ch1, ch2 in zip(s1, s2)])


def histogram_similarity(image1, image2, size=(256, 256)):
    def calculate(image1, image2):
        hist1 = cv2.calcHist([image1], [0], None, [256], [0.0, 255.0])
        hist2 = cv2.calcHist([image2], [0], None, [256], [0.0, 255.0])
        # 计算直方图的重合度
        degree = 0
        for i in range(len(hist1)):
            if hist1[i] != hist2[i]:
                degree = degree + (1 - abs(hist1[i] - hist2[i]) / max(hist1[i], hist2[i]))
            else:
                degree = degree + 1
        degree = degree / len(hist1)
        return degree

    # 将图像resize后，分离为RGB三个通道，再计算每个通道的相似值
    image1 = cv2.resize(image1, size)
    image2 = cv2.resize(image2, size)
    sub_image1 = cv2.split(image1)
    sub_image2 = cv2.split(image2)
    sub_data = 0
    for im1, im2 in zip(sub_image1, sub_image2):
        sub_data += calculate(im1, im2)
    sub_data = sub_data / 3
    return sub_data


def orb_similarity(image1, image2):
    """
    :param image1: 图片1
    :param image2: 图片2
    :return: 图片相似度
    """
    try:
        h1, w1 = image1.shape[:2]
        h2, w2 = image2.shape[:2]
        r1 = min(min(h2 / h1, 1.), min(w2 / w1, 1.))
        r2 = min(min(h1 / h2, 1.), min(w1 / w2, 1.))
        image1 = cv2.resize(image1, (int(image1.shape[1] * r1), int(image1.shape[0] * r1)))
        image2 = cv2.resize(image2, (int(image2.shape[1] * r2), int(image2.shape[0] * r2)))

        kp1, des1 = _orb.detectAndCompute(image1, None)
        kp2, des2 = _orb.detectAndCompute(image2, None)
        # knn筛选结果
        matches = _bf.knnMatch(des1, des2, k=2)
        # 查看最大匹配点数目
        good = [[m] for (m, n) in matches if m.distance < 0.75 * n.distance]

        # _img1 = cv2.drawKeypoints(image1, kp1, None, color=(0, 255, 0), flags=0)
        # _img2 = cv2.drawKeypoints(image2, kp2, None, color=(0, 255, 0), flags=0)
        # _img3 = cv2.drawMatchesKnn(image1, kp1, image2, kp2, good, None, flags=2)
        # cv2.imwrite("1.png", _img1)
        # cv2.imwrite("2.png", _img2)
        # cv2.imwrite("3.png", _img3)

        return len(good) / len(matches)

    except ValueError:
        return 0


def variance_similarity(image1, image2, confident=0.8):
    def calculate(img):
        img = cv2.resize(img, (32, 32))
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        mses = []
        for i in range(32):
            avg = np.mean(gray[i, :])
            mse = np.square(gray[i, :] - avg)
            mses.append(mse)
        return np.array(mses)

    mses1, mses2 = calculate(image1), calculate(image2)
    diffs = np.abs(mses1, mses2)
    fingle = np.array(diffs < (1 - confident) * np.max(diffs)) + 0
    similar = fingle.reshape(1, -1)[0].tolist()
    similar = 1 if similar == 0.0 else sum(similar) / len(similar)

    return similar


def layer_mask(image, top=0.82, down=0.98):
    """
    :param image: numpy data
    :param top: top percent of image
    :param down: bottom percent of image
    :return: mask numpy data
    """
    if len(image.shape) < 3:
        return image

    if image.shape[-1] == 3:
        image = cv2.cvtColor(image, cv2.COLOR_RGB2RGBA)

    w, h = image.shape[:2][::-1]
    s_row, e_row = int(h * top), int(h * down)
    theta = np.pi / (e_row - s_row)
    image = np.asarray(image, np.float32)
    for i in range(s_row, e_row):
        image[i, :, -1] *= ((np.cos(theta * (i - s_row)) + 1) / 2)

    image[e_row:h, :, -1] = 0
    return np.asarray(image, np.uint8)


def layer_reflection(image, top=0, down=0.3, transparency=0.15):
    """
    图片倒影
    :param image: 输入图片（numpy data）
    :param top: 原图起始比例
    :param down: 原图终止比例
    :param transparency: 不透明度
    :return: 输出图片（numpy data）
    """
    if len(image.shape) < 3:
        return image

    if image.shape[-1] == 3:
        image = cv2.cvtColor(image, cv2.COLOR_RGB2RGBA)

    w, h = image.shape[:2][::-1]
    # 1、图片镜像
    flip = cv2.flip(image, 0).astype(np.float32)
    flip = flip[int(top * h):int(down * h), :]
    # 2、镜像后的图片透明通道不透明度设为20%
    flip[:, :, -1] *= transparency
    # 3、蒙版处理
    _mask = layer_mask(flip, 0, 1)
    return _mask


def layer_shadow(image, kernel=(100, 100), direction=(-1, -1)):
    """
    图片倒影
    :param image: 输入图片（numpy data）
    :param kernel: 阴影（宽，高）
    :param direction: 阴影方向
    :return: 输出图片（numpy data）
    """
    if len(image.shape) < 3:
        return image

    if image.shape[-1] == 3:
        image = cv2.cvtColor(image, cv2.COLOR_RGB2RGBA)

    if direction == (-1, -1):
        anchor = direction
    else:
        left, up = direction
        anchor = (0 if left > 0 else kernel[0] - 1, 0 if up > 0 else kernel[1] - 1)
    gray = cv2.blur(image[:, :, 3], kernel, anchor=anchor)  # 第一个0:左边，kernel[0] - 1:右边; 第二个0:上边，kernel[1] - 1:下边
    gray = cv2.GaussianBlur(gray, (5, 5), 3)
    new = np.zeros(image.shape, np.uint8)
    for i in range(0, 3):
        new[:, :, i] = max(kernel)
    new[:, :, 3] = gray

    # alpha 决定主体区域
    alpha = np.expand_dims(image[:, :, 3], axis=-1) / 255
    new = image * alpha + new * (1 - alpha)

    return new.astype("uint8")


def get_contours(image, thre=250, threshold1=15, threshold2=55):
    """
    获取白底图物体轮廓
    :param image: 输入图像
    :param thre: 二值化阈值
    :param threshold1: 滞后阈值 min
    :param threshold2: 滞后阈值 max
    :return: 轮廓信息
    """
    w, h = image.shape[:2][::-1]
    if len(image.shape) < 3:
        new = image
    elif image.shape[-1] == 3:
        new = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    else:
        new = cv2.cvtColor(image[:, :, :-1], cv2.COLOR_RGB2GRAY)
        points = np.argwhere(image[:, :, -1] > 255 * 0.05)[:, ::-1]
        if points.size > 0:
            _, _, _w, _h = cv2.boundingRect(points)
            if _w < w or _h < h:
                # 透明图
                new = image[:, :, -1]

    inner = cv2.threshold(new, thre, 255, cv2.THRESH_BINARY_INV)[1]
    k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (15, 15))
    inner = cv2.morphologyEx(inner, cv2.MORPH_OPEN, k)

    new = cv2.Canny(new, threshold1, threshold2)
    new = new + inner
    new = cv2.morphologyEx(new, cv2.MORPH_CLOSE, k)

    contours, hierarchy = cv2.findContours(new, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[-2:]

    return contours, hierarchy
