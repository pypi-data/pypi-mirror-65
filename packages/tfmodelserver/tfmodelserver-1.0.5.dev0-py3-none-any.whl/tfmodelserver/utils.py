""" Utils """
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import base64

import numpy as np
from io import BytesIO
from PIL import Image

def dict_map(fn: callable, d: dict) -> dict:
    return dict(map(lambda t: fn(*t), d.items()))


def dict_filter(fn: callable, d: dict) -> dict:
    return dict(filter(lambda t: fn(*t), d.items()))


def b64encode(img) -> str:
    if isinstance(img, np.ndarray):
        buffered = BytesIO()
        Image.fromarray(img).save(buffered, format="JPEG")
        img = base64.b64encode(buffered.getvalue())
    elif not isinstance(img, (bytes, str)):
        raise ValueError('`img` should be an instance of either `np.ndarray` or `bytes`')

    return base64.b64encode(img).decode('utf-8')
