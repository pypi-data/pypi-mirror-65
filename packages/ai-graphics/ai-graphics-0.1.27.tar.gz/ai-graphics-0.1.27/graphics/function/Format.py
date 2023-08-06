"""
Name : Format.py
Author  : Cash
Contact : tkggpdc2007@163.com
Time    : 2020-01-08 10:52
Desc:
"""

import os

__all__ = ['get_random_md5',
           'get_file_md5']


def get_random_md5():
    import uuid
    uid = str(uuid.uuid4())
    md5 = ''.join(uid.split('-'))
    return md5


def get_file_md5(file):
    import hashlib
    m = hashlib.md5()
    with open(file, 'rb') as f:
        for line in f:
            m.update(line)
    return m.hexdigest()


def convert_png2jpg(infile):
    """
    图像格式转换: png转jpg
    :param infile:
    :return:
    """
    from PIL import Image

    outfile = os.path.splitext(infile)[0] + ".jpg"
    image = Image.open(infile)
    try:
        if len(image.split()) == 4:
            r, g, b, a = image.split()
            image = Image.merge("RGB", (r, g, b))
            image.convert('RGB').save(outfile, quality=70)
            os.remove(infile)
        else:
            image.convert('RGB').save(outfile, quality=70)
            os.remove(infile)
        return outfile
    except ValueError:
        pass
