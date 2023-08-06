import cv2
import numpy as np
import torch
import torch.nn as nn
import collections
from ..libs.indexnet.hlmobilenetv2 import hlmobilenetv2

__all__ = ['Matting']


def image_alignment(x, output_stride=32, odd=False):
    imsize = np.asarray(x.shape[:2], dtype=np.float)
    if odd:
        new_imsize = np.ceil(imsize / output_stride) * output_stride + 1
    else:
        new_imsize = np.ceil(imsize / output_stride) * output_stride
    h, w = int(new_imsize[0]), int(new_imsize[1])

    x1 = x[:, :, 0:3]
    x2 = x[:, :, 3]
    new_x1 = cv2.resize(x1, dsize=(w, h), interpolation=cv2.INTER_CUBIC)
    new_x2 = cv2.resize(x2, dsize=(w, h), interpolation=cv2.INTER_NEAREST)

    new_x2 = np.expand_dims(new_x2, axis=2)
    new_x = np.concatenate((new_x1, new_x2), axis=2)

    return new_x


class Matting(object):
    def __init__(self, model_name='indexnet_matting.pth.tar', ctx_id=-1):
        self.model_name = model_name
        self.ctx_id = ctx_id if torch.cuda.is_available() else -1
        self.device = torch.device("cuda:" + str(ctx_id)) if self.ctx_id > -1 else torch.device("cpu")
        self.net = self.load_model()

    def load_model(self):
        net = hlmobilenetv2(pretrained=False,
                            freeze_bn=True,
                            output_stride=32,
                            apply_aspp=True,
                            conv_operator='std_conv',
                            decoder='indexnet',
                            decoder_kernel_size=5,
                            indexnet='depthwise',
                            index_mode='m2o',
                            use_nonlinear=True,
                            use_context=True)
        # net = nn.DataParallel(net)
        # checkpoint = torch.load(self.model_name, map_location=None if self.ctx_id > -1 else 'cpu')
        # net.load_state_dict(checkpoint['state_dict'])
        # GPU模型转CPU
        checkpoint = torch.load(self.model_name, map_location=None if self.ctx_id > -1 else 'cpu')['state_dict']
        dict = collections.OrderedDict()
        for key, value in checkpoint.items():
            _key = key[7:]
            dict[_key] = value
        net.load_state_dict(dict)

        if self.ctx_id > -1:
            net.to(self.device)
        net.eval()
        return net

    def generate_trimap(self, mask):
        mask = cv2.threshold(mask, 127, 255, cv2.THRESH_BINARY)[1]
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (15, 15))
        erode = cv2.erode(mask, kernel)
        dilate = cv2.dilate(mask, kernel)
        trimap = erode + (dilate - erode) / 255. * 128

        return trimap.astype(np.uint8)

    def predict(self, image, trimap):
        scale = 1. / 255
        mean = np.array([0.485, 0.456, 0.406, 0]).reshape((1, 1, 4))
        std = np.array([0.229, 0.224, 0.225, 1]).reshape((1, 1, 4))

        with torch.no_grad():
            trimap = np.expand_dims(trimap if len(trimap.shape) <= 2 else trimap[:, :, 0], -1)
            image = np.concatenate((image[:, :, :3], trimap), axis=2)
            h, w = image.shape[:2]
            image = (scale * image - mean) / std
            image = image.astype('float32')
            image = image_alignment(image)

            inputs = torch.from_numpy(np.expand_dims(image.transpose(2, 0, 1), axis=0))
            if self.ctx_id > -1:
                inputs = inputs.to(self.device)
            outputs = self.net(inputs).squeeze().cpu().data.numpy()
            alpha = cv2.resize(outputs, dsize=(w, h), interpolation=cv2.INTER_CUBIC)
            alpha = np.clip(alpha, 0, 1) * 255.

            trimap = trimap.squeeze()
            mask = np.equal(trimap, 128).astype(np.float32)
            alpha = (1 - mask) * trimap + mask * alpha

        return alpha.astype(np.uint8)

    @staticmethod
    def save_png(image, alpha):
        if len(image.shape) < 3:
            return image

        new = np.zeros((image.shape[0], image.shape[1], 4), np.uint8)
        new[:, :, :-1] = image[:, :, :3]
        new[:, :, -1] = alpha

        return new
