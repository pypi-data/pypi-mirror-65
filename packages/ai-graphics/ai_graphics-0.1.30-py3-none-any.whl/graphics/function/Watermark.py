import os

import cv2
import numpy as np


class Watermark:
    """
    去除图片/视频中的水印
    """

    def __init__(self):
        pass

    @staticmethod
    def _threshold(image, threshold=0.2):
        """
        Threshold the images to make all its elements greater than threshold*MAX = 1
        :param image:
        :param threshold:
        :return:
        """
        im = image.astype(np.float32)
        im = (im - np.min(im)) / (np.max(im) - np.min(im))
        im[im >= threshold] = 1
        im[im < 1] = 0
        return im.astype(np.uint8)

    def _compute_watermark(self, images, threshold=0.2):
        """
        计算水印图片水平、垂直方向梯度
        :param images: 输入图片list
        :return: 水平、垂直梯度
        """
        temp = np.max(np.array(images), axis=0) - np.min(np.array(images), axis=0)
        temp = 1 - self._threshold(np.average(temp, axis=2), threshold)
        _w, _h = temp.shape[:2][::-1]
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (int(_w * 0.02), int(_h * 0.02)))
        temp = cv2.morphologyEx(temp, cv2.MORPH_CLOSE, kernel) * 255
        _contours = cv2.findContours(temp, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[-2]
        contours = []
        for c in _contours:
            if c.size < 8:
                continue
            x, y, w, h = cv2.boundingRect(c)
            if w >= _w / 2 and h >= _h / 2:
                continue
            contours.append(c)
        return temp, contours

    @staticmethod
    def _detect(image, gx, gy, thresh_low=200, thresh_high=220):
        """
        检测图片中的水印位置
        :param image: 输入图片
        :param thresh_low: 最小阈值
        :param thresh_high: 最大阈值
        :return: 水印区域：top, down, left, right
        """
        grad = np.average(np.sqrt(np.square(gx) + np.square(gy)), axis=2)
        edge = cv2.Canny(image, thresh_low, thresh_high)
        res = cv2.matchTemplate(edge, grad.astype(np.uint8), cv2.TM_CCOEFF_NORMED)

        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        print(max_val)
        if max_val <= 0.1:
            return []
        x, y = max_loc
        w, h = grad.shape[::-1]
        top, down, left, right = y, y + h - 1, x, x + w - 1

        return top, down, left, right

    def remove_with_images(self, images, threshold=0.2):
        if len(images) <= 0:
            return images

        _, contours = self._compute_watermark(images, threshold)
        if len(contours) <= 0:
            return images

        return [self._inpainting(image, contours) for image in images]

    @staticmethod
    def _inpainting(image, contours):
        cv2.drawContours(image, contours, -1, (0, 0, 0), cv2.FILLED)

        return image

    def remove_with_video(self, video_path, threshold=0.2):
        from .VideoProcess import extract_frames
        from moviepy.editor import VideoFileClip, ImageSequenceClip

        images = extract_frames(video_path)
        if len(images) <= 0:
            return

        temp, contours = self._compute_watermark(images[0], threshold)
        if len(contours) <= 0:
            return

        clip = VideoFileClip(video_path)
        frames = [self._inpainting(frame, contours) for frame in clip.iter_frames()]
        fps, num_frames = clip.fps, min(clip.reader.nframes, len(frames))
        audio = clip.audio.subclip(0 / fps, num_frames / fps)
        clip = ImageSequenceClip(frames, fps=fps).set_audio(audio)
        clip.write_videofile(video_path, fps=fps, audio_codec="aac", threads=5)
        audio.close()
        clip.close()

        return
